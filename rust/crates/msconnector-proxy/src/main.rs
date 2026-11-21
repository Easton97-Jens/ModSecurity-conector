use msconnector_ffi::Engine;
use std::env;
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::atomic::{AtomicU64, Ordering};

static REQUEST_ID: AtomicU64 = AtomicU64::new(1);

fn read_head(stream: &mut TcpStream) -> std::io::Result<(Vec<u8>, Vec<u8>)> {
    let mut buf = [0u8; 4096];
    let mut head = Vec::new();
    let mut remainder = Vec::new();
    loop {
        let n = stream.read(&mut buf)?;
        if n == 0 {
            break;
        }
        let chunk = &buf[..n];
        if let Some(position) = chunk.windows(4).position(|window| window == b"\r\n\r\n") {
            let split = position + 4;
            head.extend_from_slice(&chunk[..split]);
            remainder.extend_from_slice(&chunk[split..]);
            break;
        }
        head.extend_from_slice(chunk);
        if head.len() > 64 * 1024 {
            return Err(std::io::Error::new(
                std::io::ErrorKind::InvalidData,
                "request headers exceed 64 KiB",
            ));
        }
    }
    Ok((head, remainder))
}

fn content_length(head: &[u8]) -> usize {
    let text = String::from_utf8_lossy(head);
    text.lines()
        .skip(1)
        .filter_map(|line| line.split_once(':'))
        .find(|(name, _)| name.eq_ignore_ascii_case("content-length"))
        .and_then(|(_, value)| value.trim().parse().ok())
        .unwrap_or(0)
}

fn request_target(head: &[u8]) -> (String, String) {
    let text = String::from_utf8_lossy(head);
    let mut parts = text.lines().next().unwrap_or("").split_whitespace();
    let _method = parts.next().unwrap_or("");
    let uri = parts.next().unwrap_or("/");
    let version = parts.next().unwrap_or("HTTP/1.1");
    (uri.to_string(), version.to_string())
}

fn request_headers(head: &[u8]) -> Vec<(String, String)> {
    let text = String::from_utf8_lossy(head);
    text.lines()
        .skip(1)
        .filter_map(|line| line.split_once(':'))
        .map(|(name, value)| (name.trim().to_string(), value.trim().to_string()))
        .collect()
}

fn http_status(response: &[u8]) -> u16 {
    let text = String::from_utf8_lossy(response);
    text.split_whitespace()
        .nth(1)
        .and_then(|value| value.parse().ok())
        .unwrap_or(502)
}

fn handle(mut client: TcpStream, upstream: &str, engine: &Engine, rules: &msconnector_ffi::Rules) {
    let (head, mut remainder) = match read_head(&mut client) {
        Ok(parts) => parts,
        Err(error) => {
            let _ = client.write_all(
                format!(
                    "HTTP/1.1 400 Bad Request\r\nContent-Length: {}\r\n\r\n{}",
                    error.to_string().len(),
                    error
                )
                .as_bytes(),
            );
            return;
        }
    };
    let body_len = content_length(&head);
    let mut body = vec![0u8; body_len];
    if body_len > 0 {
        let available = remainder.len().min(body_len);
        body[..available].copy_from_slice(&remainder[..available]);
        remainder.drain(..available);
        if available < body_len && client.read_exact(&mut body[available..]).is_err() {
            let _ = client.write_all(b"HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n");
            return;
        }
    }

    let id = format!("rust-proxy-{}", REQUEST_ID.fetch_add(1, Ordering::Relaxed));
    let mut transaction = match msconnector_ffi::Transaction::new(engine, rules, id) {
        Some(transaction) => transaction,
        None => {
            let _ = client
                .write_all(b"HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n");
            return;
        }
    };
    let (uri, http_version) = request_target(&head);
    if transaction.process_uri(&uri, "http", http_version.trim_start_matches("HTTP/")) < 0 {
        let _ =
            client.write_all(b"HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n");
        return;
    }
    for (name, value) in request_headers(&head) {
        if transaction.add_request_header(&name, &value) < 0 {
            let _ = client
                .write_all(b"HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n");
            return;
        }
    }
    if transaction.process_request_headers() < 0 {
        let _ =
            client.write_all(b"HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n");
        return;
    }
    if !body.is_empty() && transaction.append_request_body(&body) < 0 {
        let _ =
            client.write_all(b"HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n");
        return;
    }
    if body_len > 0 && transaction.finish_request_body() < 0 {
        let _ =
            client.write_all(b"HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n");
        return;
    }
    let status = transaction.disruptive_status();
    if status >= 400 {
        let response = format!("HTTP/1.1 {status} ModSecurity Denied\r\nContent-Length: 0\r\n\r\n");
        let _ = client.write_all(response.as_bytes());
        let _ = transaction.process_logging();
        return;
    }

    let mut upstream_stream = match TcpStream::connect(upstream) {
        Ok(stream) => stream,
        Err(_) => {
            let _ = client.write_all(b"HTTP/1.1 502 Bad Gateway\r\nContent-Length: 0\r\n\r\n");
            return;
        }
    };
    if upstream_stream.write_all(&head).is_err() || upstream_stream.write_all(&body).is_err() {
        let _ = client.write_all(b"HTTP/1.1 502 Bad Gateway\r\nContent-Length: 0\r\n\r\n");
        return;
    }

    let mut response = Vec::new();
    if upstream_stream.read_to_end(&mut response).is_err() {
        let _ = client.write_all(b"HTTP/1.1 502 Bad Gateway\r\nContent-Length: 0\r\n\r\n");
        return;
    }
    if transaction.process_response_headers(http_status(&response)) < 0 {
        let _ =
            client.write_all(b"HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n");
        return;
    }
    if !response.is_empty() && transaction.append_response_body(&response) < 0 {
        let _ =
            client.write_all(b"HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n");
        return;
    }
    if transaction.finish_response_body() < 0 {
        let _ =
            client.write_all(b"HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n");
        return;
    }
    let response_status = transaction.disruptive_status();
    if response_status >= 400 {
        let denied =
            format!("HTTP/1.1 {response_status} ModSecurity Denied\r\nContent-Length: 0\r\n\r\n");
        let _ = client.write_all(denied.as_bytes());
    } else {
        let _ = client.write_all(&response);
    }
    let _ = transaction.process_logging();
}

fn main() -> Result<(), String> {
    let listen =
        env::var("MSCONNECTOR_PROXY_LISTEN").unwrap_or_else(|_| "127.0.0.1:8080".to_string());
    let upstream =
        env::var("MSCONNECTOR_PROXY_UPSTREAM").unwrap_or_else(|_| "127.0.0.1:8081".to_string());
    let rules =
        env::var("MSCONNECTOR_RULES").map_err(|_| "MSCONNECTOR_RULES is required".to_string())?;
    let mut engine =
        Engine::new().ok_or_else(|| "failed to initialize libmodsecurity".to_string())?;
    let rules = engine.load_rules(&rules).map_err(|error| error)?;
    let listener =
        TcpListener::bind(&listen).map_err(|error| format!("failed to bind {listen}: {error}"))?;

    for accepted in listener.incoming() {
        match accepted {
            Ok(client) => handle(client, &upstream, &engine, &rules),
            Err(error) => eprintln!("accept failed: {error}"),
        }
    }
    Ok(())
}
