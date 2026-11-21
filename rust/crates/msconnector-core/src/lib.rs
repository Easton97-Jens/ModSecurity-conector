#![forbid(unsafe_code)]

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Phase {
    P1,
    P2,
    P3,
    P4,
    Logging,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Intervention {
    pub disruptive: bool,
    pub status: u16,
}

impl Intervention {
    pub fn allow() -> Self {
        Self {
            disruptive: false,
            status: 200,
        }
    }
}

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct BodyLimits {
    pub transport_buffer_bytes: usize,
    pub working_buffer_bytes: usize,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum BodyDirection {
    Request,
    Response,
}

#[derive(Debug)]
pub struct BodyPhase {
    direction: BodyDirection,
    started: bool,
    finished: bool,
    seen: usize,
}

impl BodyPhase {
    pub fn new(direction: BodyDirection) -> Self {
        Self {
            direction,
            started: false,
            finished: false,
            seen: 0,
        }
    }
    pub fn append(&mut self, data: &[u8], transport_limit: usize) -> Result<(), &'static str> {
        if self.finished {
            return Err("body phase already finished");
        }
        if data.len() > transport_limit.saturating_sub(self.seen) {
            return Err("transport buffer limit exceeded");
        }
        self.started = true;
        self.seen = self.seen.saturating_add(data.len());
        Ok(())
    }
    pub fn finish(&mut self) -> Result<(), &'static str> {
        if self.finished {
            return Err("body phase finished more than once");
        }
        self.finished = true;
        Ok(())
    }
    pub fn direction(&self) -> BodyDirection {
        self.direction
    }
    pub fn started(&self) -> bool {
        self.started
    }
    pub fn finished(&self) -> bool {
        self.finished
    }
    pub fn seen(&self) -> usize {
        self.seen
    }
}

#[derive(Debug)]
pub struct TransactionLifecycle {
    pub id: String,
    request_body: BodyPhase,
    response_body: BodyPhase,
}

impl TransactionLifecycle {
    pub fn new(id: impl Into<String>) -> Self {
        Self {
            id: id.into(),
            request_body: BodyPhase::new(BodyDirection::Request),
            response_body: BodyPhase::new(BodyDirection::Response),
        }
    }
    pub fn request_body(&mut self) -> &mut BodyPhase {
        &mut self.request_body
    }
    pub fn response_body(&mut self) -> &mut BodyPhase {
        &mut self.response_body
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Header {
    pub name: String,
    pub value: Vec<u8>,
}

#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct RequestData {
    pub client_ip: Option<String>,
    pub method: Option<String>,
    pub uri: Option<String>,
    pub protocol: Option<String>,
    pub headers: Vec<Header>,
    pub body: Vec<u8>,
}

#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct ResponseData {
    pub status: u16,
    pub protocol: String,
    pub headers: Vec<Header>,
    pub body: Vec<u8>,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum EngineDecision {
    Allow,
    Deny { status: u16 },
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct EngineResult {
    pub phase: Phase,
    pub decision: EngineDecision,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn body_finish_is_exactly_once() {
        let mut body = BodyPhase::new(BodyDirection::Request);
        assert!(body.finish().is_ok());
        assert_eq!(body.finish(), Err("body phase finished more than once"));
    }

    #[test]
    fn append_respects_transport_limit() {
        let mut body = BodyPhase::new(BodyDirection::Response);
        assert!(body.append(&[1, 2, 3], 4).is_ok());
        assert_eq!(
            body.append(&[4, 5], 4),
            Err("transport buffer limit exceeded")
        );
    }
}
