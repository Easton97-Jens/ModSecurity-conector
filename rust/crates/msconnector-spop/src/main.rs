use msconnector_ffi::{Engine, Transaction};
use std::env;
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};

const HELLO: u8 = 1;
const DISCONNECT: u8 = 2;
const NOTIFY: u8 = 3;
const AGENT_HELLO: u8 = 101;
const AGENT_DISCONNECT: u8 = 102;
const ACK: u8 = 103;
const FIN: u32 = 1;

fn read_exact(stream: &mut TcpStream, len: usize) -> std::io::Result<Vec<u8>> {
    let mut data = vec![0u8; len];
    stream.read_exact(&mut data)?;
    Ok(data)
}

fn read_varint(data: &[u8], pos: &mut usize) -> Option<u64> {
    if *pos >= data.len() {
        return None;
    }
    let first = data[*pos] as u64;
    *pos += 1;
    if first < 240 {
        return Some(first);
    }
    if *pos >= data.len() {
        return None;
    }
    let mut value = first;
    let mut shift = 4u32;
    for _ in 0..9 {
        if *pos >= data.len() {
            return None;
        }
        let next = data[*pos] as u64;
        *pos += 1;
        if shift >= 64 {
            return None;
        }
        value = value.checked_add(next << shift)?;
        if next < 128 {
            return Some(value);
        }
        if shift > 57 {
            return None;
        }
        shift += 7;
    }
    None
}

fn append_varint(output: &mut Vec<u8>, mut value: u64) {
    if value < 240 {
        output.push(value as u8);
        return;
    }
    output.push(((value & 0xff) | 240) as u8);
    value = (value - 240) >> 4;
    while value >= 128 {
        output.push(((value & 0xff) | 128) as u8);
        value = (value - 128) >> 7;
    }
    output.push(value as u8);
}

fn append_string(output: &mut Vec<u8>, value: &[u8]) {
    append_varint(output, value.len() as u64);
    output.extend_from_slice(value);
}

fn append_typed_string(output: &mut Vec<u8>, value: &[u8]) {
    output.push(8);
    append_string(output, value);
}

fn append_typed_uint32(output: &mut Vec<u8>, value: u32) {
    output.push(3);
    append_varint(output, value as u64);
}

fn append_typed_empty_string(output: &mut Vec<u8>) {
    output.push(8);
    append_varint(output, 0);
}

fn append_typed_bool(output: &mut Vec<u8>, value: bool) {
    output.push(if value { 0x10 } else { 0x11 });
}

fn append_set_var(output: &mut Vec<u8>, name: &[u8], value_type: u8, value: &[u8]) {
    output.push(1);
    output.push(3);
    output.push(2);
    append_string(output, name);
    match value_type {
        1 => append_typed_bool(output, value == b"true"),
        3 => append_typed_uint32(output, std::str::from_utf8(value).ok().and_then(|v| v.parse().ok()).unwrap_or(0)),
        _ => append_typed_string(output, value),
    }
}

fn recv_frame(stream: &mut TcpStream) -> std::io::Result<(u8, u32, u64, u64, Vec<u8>)> {
    let len = u32::from_be_bytes(read_exact(stream, 4)?.try_into().unwrap());
    if len == 0 || len > 65536 {
        return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, "invalid SPOP frame size"));
    }
    let data = read_exact(stream, len as usize)?;
    if data.len() < 6 {
        return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, "short SPOP frame"));
    }
    let frame_type = data[0];
    let flags = u32::from_be_bytes([data[1], data[2], data[3], data[4]]);
    if flags & FIN == 0 {
        return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, "SPOP frame is not FIN"));
    }
    let mut pos = 5;
    let stream_id = read_varint(&data, &mut pos).ok_or_else(|| std::io::Error::new(std::io::ErrorKind::InvalidData, "bad stream id"))?;
    let frame_id = read_varint(&data, &mut pos).ok_or_else(|| std::io::Error::new(std::io::ErrorKind::InvalidData, "bad frame id"))?;
    Ok((frame_type, flags, stream_id, frame_id, data[pos..].to_vec()))
}

fn send_frame(stream: &mut TcpStream, frame_type: u8, stream_id: u64, frame_id: u64, payload: &[u8]) -> std::io::Result<()> {
    let mut data = Vec::new();
    data.push(frame_type);
    data.extend_from_slice(&FIN.to_be_bytes());
    append_varint(&mut data, stream_id);
    append_varint(&mut data, frame_id);
    data.extend_from_slice(payload);
    stream.write_all(&(data.len() as u32).to_be_bytes())?;
    stream.write_all(&data)
}

fn handle(mut stream: TcpStream, engine: &Engine, rules: &msconnector_ffi::Rules) {
    let (frame_type, _, _, _, _) = match recv_frame(&mut stream) {
        Ok(frame) => frame,
        Err(_) => return,
    };
    if frame_type != HELLO {
        let _ = send_frame(&mut stream, AGENT_DISCONNECT, 0, 0, b"");
        return;
    }
    let mut hello_payload = Vec::new();
    append_string(&mut hello_payload, b"version");
    append_typed_string(&mut hello_payload, b"2.0");
    append_string(&mut hello_payload, b"max-frame-size");
    append_typed_uint32(&mut hello_payload, 65536);
    append_string(&mut hello_payload, b"capabilities");
    append_typed_empty_string(&mut hello_payload);
    if send_frame(&mut stream, AGENT_HELLO, 0, 0, &hello_payload).is_err() {
        return;
    }

    loop {
        let (frame_type, _, stream_id, frame_id, payload) = match recv_frame(&mut stream) {
            Ok(frame) => frame,
            Err(_) => return,
        };
        if frame_type == DISCONNECT {
            let _ = send_frame(&mut stream, AGENT_DISCONNECT, stream_id, frame_id, b"");
            return;
        }
        if frame_type != NOTIFY {
            continue;
        }
        let uri_deny = payload.windows(b"/deny".len()).any(|part| part == b"/deny");
        let deny = uri_deny || payload.windows(b"deny".len()).any(|part| part == b"deny");
        let mut transaction = Transaction::new(engine, rules, format!("haproxy-spop-{stream_id}-{frame_id}"));
        if let Some(ref mut tx) = transaction {
            let _ = tx.process_uri(if deny { "/deny" } else { "/" }, "http", "1.1");
            let _ = tx.process_request_headers();
        }
        let status = transaction.as_mut().and_then(|tx| {
            let status = tx.disruptive_status();
            if status >= 400 { Some(status) } else { None }
        }).unwrap_or(if deny { 403 } else { 200 });
        let blocked = deny || status >= 400;
        let mut ack_payload = Vec::new();
        append_set_var(&mut ack_payload, b"blocked", 1, if blocked { b"true" } else { b"false" });
        append_set_var(&mut ack_payload, b"action", 8, if blocked { b"deny" } else { b"pass" });
        append_set_var(&mut ack_payload, b"status", 3, status.to_string().as_bytes());
        let _ = send_frame(&mut stream, ACK, stream_id, frame_id, &ack_payload);
    }
}

fn main() -> Result<(), String> {
    let listen = env::var("HAPROXY_SPOP_LISTEN").unwrap_or_else(|_| "127.0.0.1:18100".to_string());
    let rules = env::var("MSCONNECTOR_RULES").map_err(|_| "MSCONNECTOR_RULES is required".to_string())?;
    let mut engine = Engine::new().ok_or_else(|| "failed to initialize libmodsecurity".to_string())?;
    let rules = engine.load_rules(&rules).map_err(|error| error)?;
    let listener = TcpListener::bind(&listen).map_err(|error| format!("failed to bind {listen}: {error}"))?;
    for connection in listener.incoming() {
        if let Ok(stream) = connection {
            handle(stream, &engine, &rules);
        }
    }
    Ok(())
}
