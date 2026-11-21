use msconnector_ffi::{Engine, Transaction};
use std::env;
use std::fs;
use std::io::{Read, Write};
use std::os::unix::net::{UnixListener, UnixStream};
use std::path::Path;

const MAGIC: &[u8; 4] = b"MSE1";
const VERSION: u8 = 1;
const BEGIN: u8 = 1;
const REQUEST_CHUNK: u8 = 2;
const REQUEST_EOS: u8 = 3;
const RESPONSE_HEADERS: u8 = 4;
const RESPONSE_CHUNK: u8 = 5;
const RESPONSE_EOS: u8 = 6;
const FINISH: u8 = 8;
const DESTROY: u8 = 9;
const RESULT: u8 = 128;

fn read_exact(stream: &mut UnixStream, len: usize) -> std::io::Result<Vec<u8>> {
    let mut bytes = vec![0u8; len];
    stream.read_exact(&mut bytes)?;
    Ok(bytes)
}

fn read_frame(stream: &mut UnixStream) -> std::io::Result<(u8, Vec<u8>)> {
    let header = read_exact(stream, 12)?;
    if &header[0..4] != MAGIC || header[4] != VERSION {
        return Err(std::io::Error::new(
            std::io::ErrorKind::InvalidData,
            "invalid MSE1 frame",
        ));
    }
    let flags = u16::from_be_bytes([header[6], header[7]]);
    if flags != 0 {
        return Err(std::io::Error::new(
            std::io::ErrorKind::InvalidData,
            "reserved flags",
        ));
    }
    let len = u32::from_be_bytes([header[8], header[9], header[10], header[11]]) as usize;
    if len > 65_536 {
        return Err(std::io::Error::new(
            std::io::ErrorKind::InvalidData,
            "frame too large",
        ));
    }
    Ok((header[5], read_exact(stream, len)?))
}

fn write_frame(stream: &mut UnixStream, opcode: u8, payload: &[u8]) -> std::io::Result<()> {
    let mut header = vec![0u8; 12];
    header[0..4].copy_from_slice(MAGIC);
    header[4] = VERSION;
    header[5] = opcode;
    header[8..12].copy_from_slice(&(payload.len() as u32).to_be_bytes());
    stream.write_all(&header)?;
    stream.write_all(payload)
}

fn read_u16(payload: &[u8], offset: &mut usize) -> Option<u16> {
    if *offset + 2 > payload.len() {
        return None;
    }
    let value = u16::from_be_bytes([payload[*offset], payload[*offset + 1]]);
    *offset += 2;
    Some(value)
}

fn read_text(payload: &[u8], offset: &mut usize) -> Option<String> {
    let len = read_u16(payload, offset)? as usize;
    if *offset + len > payload.len() {
        return None;
    }
    let text = String::from_utf8(payload[*offset..*offset + len].to_vec()).ok()?;
    *offset += len;
    Some(text)
}

fn parse_begin(payload: &[u8]) -> Option<(String, String, String, Vec<(String, String)>)> {
    let mut offset = 0;
    let _method = read_text(payload, &mut offset)?;
    let uri = read_text(payload, &mut offset)?;
    let http_version = read_text(payload, &mut offset)?;
    let _hostname = read_text(payload, &mut offset)?;
    let client_address = read_text(payload, &mut offset)?;
    let _client_port = read_u16(payload, &mut offset)?;
    let _server_address = read_text(payload, &mut offset)?;
    let _server_port = read_u16(payload, &mut offset)?;
    let _host_request_id = read_text(payload, &mut offset)?;
    let header_count = read_u16(payload, &mut offset)? as usize;
    let mut headers = Vec::new();
    for _ in 0..header_count.min(128) {
        let name = read_text(payload, &mut offset)?;
        let value = read_text(payload, &mut offset)?;
        headers.push((name, value));
    }
    Some((uri, http_version, client_address, headers))
}

fn parse_response_headers(payload: &[u8]) -> Option<(u16, Vec<(String, String)>)> {
    let mut offset = 0;
    let status = read_u16(payload, &mut offset)?;
    let _http_version = read_text(payload, &mut offset)?;
    let header_count = read_u16(payload, &mut offset)? as usize;
    let mut headers = Vec::new();
    for _ in 0..header_count.min(128) {
        let name = read_text(payload, &mut offset)?;
        let value = read_text(payload, &mut offset)?;
        headers.push((name, value));
    }
    Some((status, headers))
}

fn result_payload(status: u16, action: u8, phase: u8, flags: u16) -> Vec<u8> {
    let mut payload = vec![0u8; 14];
    payload[0] = RESULT;
    payload[1] = 0;
    payload[2] = action;
    payload[3] = phase;
    payload[4..6].copy_from_slice(&status.to_be_bytes());
    payload[6..8].copy_from_slice(&flags.to_be_bytes());
    payload
}

fn handle_connection(mut stream: UnixStream, engine: &Engine, rules: &msconnector_ffi::Rules) {
    let mut transaction: Option<Transaction> = None;
    let mut begun = false;
    loop {
        let (opcode, payload) = match read_frame(&mut stream) {
            Ok(frame) => frame,
            Err(_) => break,
        };
        match opcode {
            BEGIN if !begun => {
                let Some((uri, http_version, client_address, headers)) = parse_begin(&payload)
                else {
                    let _ = write_frame(&mut stream, RESULT, &result_payload(400, 2, 1, 0));
                    break;
                };
                let id = format!("traefik-{}", std::process::id());
                let Some(mut tx) = Transaction::new(engine, rules, id) else {
                    let _ = write_frame(&mut stream, RESULT, &result_payload(500, 2, 1, 0));
                    break;
                };
                let _ = tx.process_connection(&client_address);
                let _ = tx.process_uri(&uri, "http", &http_version);
                for (name, value) in headers {
                    let _ = tx.add_request_header(&name, &value);
                }
                let _status = tx.process_request_headers();
                let disruptive = tx.disruptive_status();
                begun = true;
                transaction = Some(tx);
                let action = if disruptive >= 400 { 2 } else { 0 };
                let status = if disruptive >= 100 { disruptive } else { 200 };
                let _ = write_frame(&mut stream, RESULT, &result_payload(status, action, 1, 0));
            }
            REQUEST_CHUNK => {
                if let Some(tx) = transaction.as_mut() {
                    let _status = tx.append_request_body(&payload);
                    let disruptive = tx.disruptive_status();
                    let action = if disruptive >= 400 { 2 } else { 0 };
                    let status = if disruptive >= 100 { disruptive } else { 200 };
                    let _ = write_frame(&mut stream, RESULT, &result_payload(status, action, 2, 0));
                    let _ = status;
                }
            }
            REQUEST_EOS => {
                if let Some(tx) = transaction.as_mut() {
                    let result = tx.finish_request_body();
                    let disruptive = tx.disruptive_status();
                    let action = if disruptive >= 400 { 2 } else { 0 };
                    let status = if disruptive >= 100 { disruptive } else { 200 };
                    let flags = if result >= 0 { 1 << 2 } else { 0 };
                    let _ = write_frame(
                        &mut stream,
                        RESULT,
                        &result_payload(status, action, 2, flags),
                    );
                }
            }
            RESPONSE_HEADERS => {
                if let Some(tx) = transaction.as_mut() {
                    if let Some((status, headers)) = parse_response_headers(&payload) {
                        for (name, value) in headers {
                            let _ = tx.add_response_header(&name, &value);
                        }
                        let result = tx.process_response_headers(status);
                        let disruptive = tx.disruptive_status();
                        let action = if disruptive >= 400 { 2 } else { 0 };
                        let status = if disruptive >= 100 {
                            disruptive
                        } else {
                            status
                        };
                        let flags = if result >= 0 { 1 << 3 } else { 0 };
                        let _ = write_frame(
                            &mut stream,
                            RESULT,
                            &result_payload(status, action, 3, flags),
                        );
                    }
                }
            }
            RESPONSE_CHUNK => {
                if let Some(tx) = transaction.as_mut() {
                    let result = tx.append_response_body(&payload);
                    let disruptive = tx.disruptive_status();
                    let action = if disruptive >= 400 { 2 } else { 0 };
                    let status = if disruptive >= 100 { disruptive } else { 200 };
                    let _ = write_frame(
                        &mut stream,
                        RESULT,
                        &result_payload(status, action, 4, if result >= 0 { 1 << 4 } else { 0 }),
                    );
                }
            }
            RESPONSE_EOS => {
                if let Some(tx) = transaction.as_mut() {
                    let result = tx.finish_response_body();
                    let disruptive = tx.disruptive_status();
                    let action = if disruptive >= 400 { 2 } else { 0 };
                    let status = if disruptive >= 100 { disruptive } else { 200 };
                    let flags = if result >= 0 { 1 << 4 } else { 0 };
                    let _ = write_frame(
                        &mut stream,
                        RESULT,
                        &result_payload(status, action, 4, flags),
                    );
                }
            }
            FINISH => {
                if let Some(tx) = transaction.as_mut() {
                    let _ = tx.process_logging();
                }
                let _ = write_frame(&mut stream, RESULT, &result_payload(200, 0, 4, 1 << 5));
            }
            DESTROY => {
                let _ = write_frame(&mut stream, RESULT, &result_payload(200, 0, 4, 1 << 6));
                break;
            }
            _ => break,
        }
    }
}

fn main() -> Result<(), String> {
    let socket_path = env::var("TRAEFIK_ENGINE_SOCKET")
        .unwrap_or_else(|_| "/var/tmp/codex/git/traefik-engine.sock".to_string());
    let rules_path =
        env::var("MSCONNECTOR_RULES").map_err(|_| "MSCONNECTOR_RULES is required".to_string())?;
    let mut engine =
        Engine::new().ok_or_else(|| "failed to initialize libmodsecurity".to_string())?;
    let rules = engine.load_rules(&rules_path).map_err(|error| error)?;
    let path = Path::new(&socket_path);
    if path.exists() {
        fs::remove_file(path).map_err(|error| format!("failed to remove stale socket: {error}"))?;
    }
    let listener =
        UnixListener::bind(path).map_err(|error| format!("failed to bind UDS: {error}"))?;

    for connection in listener.incoming() {
        match connection {
            Ok(stream) => handle_connection(stream, &engine, &rules),
            Err(error) => eprintln!("accept failed: {error}"),
        }
    }
    Ok(())
}
