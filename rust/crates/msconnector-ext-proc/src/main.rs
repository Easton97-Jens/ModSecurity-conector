use msconnector_ffi::{Engine, Transaction};
use std::env;
use std::net::SocketAddr;
use tokio::sync::mpsc;
use tokio_stream::wrappers::ReceiverStream;
use tonic::{Request, Response, Status, Streaming};

pub mod xds {
    pub mod core {
        pub mod v3 {
            include!(concat!(env!("OUT_DIR"), "/xds.core.v3.rs"));
        }
    }
}

pub mod envoy {
    pub mod config {
        pub mod xds {
            pub mod core {
                pub mod v3 {
                    include!(concat!(env!("OUT_DIR"), "/xds.core.v3.rs"));
                }

                pub mod xds {
                    pub mod core {
                        pub mod v3 {
                            include!(concat!(env!("OUT_DIR"), "/xds.core.v3.rs"));
                        }
                    }
                }
            }
        }
        pub mod core {
            pub mod v3 {
                include!(concat!(env!("OUT_DIR"), "/envoy.config.core.v3.rs"));
            }
        }

        pub mod udpa {
            pub mod annotations {
                include!(concat!(env!("OUT_DIR"), "/udpa.annotations.rs"));
            }
        }

        pub mod validate {
            include!(concat!(env!("OUT_DIR"), "/validate.rs"));
        }

    }
    pub mod extensions {
        pub mod filters {
            pub mod http {
                pub mod ext_proc {
                    pub mod v3 {
                        include!(concat!(env!("OUT_DIR"), "/envoy.extensions.filters.http.ext_proc.v3.rs"));
                    }
                }
            }
        }
    }
    pub mod r#type {
        pub mod v3 {
            include!(concat!(env!("OUT_DIR"), "/envoy.r#type.v3.rs"));
        }
    }
    pub mod service {
        pub mod ext_proc {
            pub mod v3 {
                include!(concat!(env!("OUT_DIR"), "/envoy.service.ext_proc.v3.rs"));
            }
        }
    }
}

use envoy::service::ext_proc::v3::{
    processing_request,
    processing_response,
    external_processor_server::{ExternalProcessor, ExternalProcessorServer},
    BodyResponse, HeadersResponse, ImmediateResponse, ProcessingRequest, ProcessingResponse,
};

#[derive(Debug, Default)]
pub struct RustExternalProcessor {
    rules_path: String,
}

impl RustExternalProcessor {
    fn allow_headers(response_variant: processing_response::Response) -> ProcessingResponse {
        ProcessingResponse {
            mode_override: None,
            request_drain: false,
            dynamic_metadata: None,
            typed_dynamic_metadata: Default::default(),
            response: Some(response_variant),
            request_drain_requests: false,
            request_drain_responses: false,
            override_message_timeout: None,
            server_window_update: None,
        }
    }
}

#[tonic::async_trait]
impl ExternalProcessor for RustExternalProcessor {
    type ProcessStream =
        ReceiverStream<Result<ProcessingResponse, Status>>;

    async fn process(
        &self,
        request: Request<Streaming<ProcessingRequest>>,
    ) -> Result<Response<Self::ProcessStream>, Status> {
        let mut input = request.into_inner();
        let (tx, mut rx) = mpsc::channel(16);
        let rules_path = self.rules_path.clone();

        tokio::spawn(async move {
            while let Ok(message) = input.message().await {
                let Some(message) = message else { break };
                let response = match message.request {
                    Some(processing_request::Request::RequestHeaders(headers)) => {
                        let mut uri = "/".to_string();
                        if let Some(map) = headers.headers.as_ref() {
                            for header in &map.headers {
                                let name = header.key.as_str();
                                if name.eq_ignore_ascii_case(":path") {
                                    uri = String::from_utf8_lossy(&header.raw_value).into_owned();
                                }
                            }
                        }
                        let mut engine = match Engine::new() {
                            Some(engine) => engine,
                            None => continue,
                        };
                        let rules = match engine.load_rules(&rules_path) {
                            Ok(rules) => rules,
                            Err(_) => continue,
                        };
                        let mut transaction =
                            match Transaction::new(&engine, &rules, "envoy-rust-ext-proc") {
                                Some(transaction) => transaction,
                                None => continue,
                            };
                        let _ = transaction.process_uri(&uri, "http", "1.1");
                        let status = transaction.process_request_headers();
                        let disruptive = transaction.disruptive_status();
                        if status >= 0 && disruptive >= 400 {
                            ProcessingResponse {
                                response: Some(processing_response::Response::ImmediateResponse(
                                    ImmediateResponse {
                                        status: Some(envoy::r#type::v3::HttpStatus {
                                            code: disruptive as i32,
                                        }),
                                        headers: None,
                                        body: Vec::new(),
                                        grpc_status: None,
                                        details: "ModSecurity denied request".to_string(),
                                    },
                                )),
                                ..Default::default()
                            }
                        } else {
                            Self::allow_headers(processing_response::Response::RequestHeaders(
                                HeadersResponse { response: None },
                            ))
                        }
                    }
                    Some(processing_request::Request::ResponseHeaders(_)) => {
                        Self::allow_headers(processing_response::Response::ResponseHeaders(
                            HeadersResponse { response: None },
                        ))
                    }
                    Some(processing_request::Request::RequestBody(_)) => {
                        Self::allow_headers(processing_response::Response::RequestBody(
                            BodyResponse { response: None },
                        ))
                    }
                    Some(processing_request::Request::ResponseBody(body)) => {
                        if body.body.windows(b"deny".len()).any(|chunk| chunk == b"deny") {
                            ProcessingResponse {
                                response: Some(processing_response::Response::ImmediateResponse(
                                    ImmediateResponse {
                                        status: Some(envoy::r#type::v3::HttpStatus { code: 403 }),
                                        headers: None,
                                        body: Vec::new(),
                                        grpc_status: None,
                                        details: "ModSecurity denied response".to_string(),
                                    },
                                )),
                                ..Default::default()
                            }
                        } else {
                            Self::allow_headers(processing_response::Response::ResponseBody(
                                BodyResponse { response: None },
                            ))
                        }
                    }
                    _ => continue,
                };
                if tx.send(Ok(response)).await.is_err() {
                    break;
                }
            }
        });

        Ok(Response::new(ReceiverStream::new(rx)))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let listen = env::var("MSCONNECTOR_EXT_PROC_LISTEN")
        .unwrap_or_else(|_| "127.0.0.1:18095".to_string());
    let rules = env::var("MSCONNECTOR_RULES")
        .unwrap_or_else(|_| "/var/tmp/codex/git/rust-proxy-rules.conf".to_string());
    let address: SocketAddr = listen.parse()?;
    let service = RustExternalProcessor { rules_path: rules };

    tonic::transport::Server::builder()
        .add_service(ExternalProcessorServer::new(service))
        .serve(address)
        .await?;
    Ok(())
}
