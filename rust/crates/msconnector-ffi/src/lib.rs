use msconnector_core::TransactionLifecycle;
use std::ffi::{c_char, c_int, CStr, CString};

#[repr(C)]
struct MsShimEngine {
    _private: [u8; 0],
}
#[repr(C)]
struct MsShimRules {
    _private: [u8; 0],
}
#[repr(C)]
struct MsShimTransaction {
    _private: [u8; 0],
}

extern "C" {
    fn msc_shim_engine_new() -> *mut MsShimEngine;
    fn msc_shim_engine_free(engine: *mut MsShimEngine);
    fn msc_shim_rules_load(
        engine: *mut MsShimEngine,
        path: *const c_char,
        error: *mut c_char,
        error_len: usize,
    ) -> *mut MsShimRules;
    fn msc_shim_rules_free(rules: *mut MsShimRules);
    fn msc_shim_transaction_new(
        engine: *mut MsShimEngine,
        rules: *mut MsShimRules,
    ) -> *mut MsShimTransaction;
    fn msc_shim_transaction_free(transaction: *mut MsShimTransaction);
    fn msc_shim_process_connection(
        transaction: *mut MsShimTransaction,
        client_ip: *const c_char,
    ) -> c_int;
    fn msc_shim_process_uri(
        transaction: *mut MsShimTransaction,
        uri: *const c_char,
        protocol: *const c_char,
        http_version: *const c_char,
    ) -> c_int;
    fn msc_shim_add_request_header(
        transaction: *mut MsShimTransaction,
        name: *const c_char,
        value: *const c_char,
    ) -> c_int;
    fn msc_shim_process_request_headers(transaction: *mut MsShimTransaction) -> c_int;
    fn msc_shim_append_request_body(
        transaction: *mut MsShimTransaction,
        data: *const u8,
        len: usize,
    ) -> c_int;
    fn msc_shim_finish_request_body(transaction: *mut MsShimTransaction) -> c_int;
    fn msc_shim_process_response_headers(
        transaction: *mut MsShimTransaction,
        status: c_int,
    ) -> c_int;
    fn msc_shim_add_response_header(
        transaction: *mut MsShimTransaction,
        name: *const c_char,
        value: *const c_char,
    ) -> c_int;
    fn msc_shim_append_response_body(
        transaction: *mut MsShimTransaction,
        data: *const u8,
        len: usize,
    ) -> c_int;
    fn msc_shim_finish_response_body(transaction: *mut MsShimTransaction) -> c_int;
    fn msc_shim_process_logging(transaction: *mut MsShimTransaction) -> c_int;
    fn msc_shim_disruptive_status(transaction: *mut MsShimTransaction) -> c_int;
}

pub struct Engine {
    raw: *mut MsShimEngine,
}
impl Engine {
    pub fn new() -> Option<Self> {
        let raw = unsafe { msc_shim_engine_new() };
        (!raw.is_null()).then_some(Self { raw })
    }
    pub fn load_rules(&mut self, path: &str) -> Result<Rules, String> {
        let path = CString::new(path).map_err(|_| "NUL in rules path".to_string())?;
        let mut error = [0 as c_char; 512];
        let raw = unsafe {
            msc_shim_rules_load(self.raw, path.as_ptr(), error.as_mut_ptr(), error.len())
        };
        if raw.is_null() {
            let message = unsafe { CStr::from_ptr(error.as_ptr()) }
                .to_string_lossy()
                .into_owned();
            return Err(if message.is_empty() {
                "libmodsecurity rules load failed".to_string()
            } else {
                message
            });
        }
        Ok(Rules { raw })
    }
}
impl Drop for Engine {
    fn drop(&mut self) {
        unsafe { msc_shim_engine_free(self.raw) }
    }
}

pub struct Rules {
    raw: *mut MsShimRules,
}
impl Drop for Rules {
    fn drop(&mut self) {
        unsafe { msc_shim_rules_free(self.raw) }
    }
}

pub struct Transaction {
    raw: *mut MsShimTransaction,
    lifecycle: TransactionLifecycle,
}

impl Transaction {
    pub fn new(engine: &Engine, rules: &Rules, id: impl Into<String>) -> Option<Self> {
        let lifecycle = TransactionLifecycle::new(id);
        let raw = unsafe { msc_shim_transaction_new(engine.raw, rules.raw) };
        (!raw.is_null()).then_some(Self { raw, lifecycle })
    }
    pub fn process_connection(&mut self, client_ip: &str) -> i32 {
        let ip = match CString::new(client_ip) {
            Ok(value) => value,
            Err(_) => return -1,
        };
        unsafe { msc_shim_process_connection(self.raw, ip.as_ptr()) }
    }
    pub fn process_uri(&mut self, uri: &str, protocol: &str, http_version: &str) -> i32 {
        let uri = match CString::new(uri) {
            Ok(value) => value,
            Err(_) => return -1,
        };
        let protocol = match CString::new(protocol) {
            Ok(value) => value,
            Err(_) => return -1,
        };
        let http_version = match CString::new(http_version) {
            Ok(value) => value,
            Err(_) => return -1,
        };
        unsafe {
            msc_shim_process_uri(
                self.raw,
                uri.as_ptr(),
                protocol.as_ptr(),
                http_version.as_ptr(),
            )
        }
    }
    pub fn add_request_header(&mut self, name: &str, value: &str) -> i32 {
        let name = match CString::new(name) {
            Ok(value) => value,
            Err(_) => return -1,
        };
        let value = match CString::new(value) {
            Ok(value) => value,
            Err(_) => return -1,
        };
        unsafe { msc_shim_add_request_header(self.raw, name.as_ptr(), value.as_ptr()) }
    }
    pub fn process_request_headers(&mut self) -> i32 {
        unsafe { msc_shim_process_request_headers(self.raw) }
    }
    pub fn append_request_body(&mut self, data: &[u8]) -> i32 {
        if self
            .lifecycle
            .request_body()
            .append(data, usize::MAX)
            .is_err()
        {
            return -1;
        }
        unsafe { msc_shim_append_request_body(self.raw, data.as_ptr(), data.len()) }
    }
    pub fn finish_request_body(&mut self) -> i32 {
        if self.lifecycle.request_body().finish().is_err() {
            return -1;
        }
        unsafe { msc_shim_finish_request_body(self.raw) }
    }
    pub fn process_response_headers(&mut self, status: u16) -> i32 {
        unsafe { msc_shim_process_response_headers(self.raw, status as c_int) }
    }
    pub fn add_response_header(&mut self, name: &str, value: &str) -> i32 {
        let name = match CString::new(name) {
            Ok(value) => value,
            Err(_) => return -1,
        };
        let value = match CString::new(value) {
            Ok(value) => value,
            Err(_) => return -1,
        };
        unsafe { msc_shim_add_response_header(self.raw, name.as_ptr(), value.as_ptr()) }
    }
    pub fn append_response_body(&mut self, data: &[u8]) -> i32 {
        if self
            .lifecycle
            .response_body()
            .append(data, usize::MAX)
            .is_err()
        {
            return -1;
        }
        unsafe { msc_shim_append_response_body(self.raw, data.as_ptr(), data.len()) }
    }
    pub fn finish_response_body(&mut self) -> i32 {
        if self.lifecycle.response_body().finish().is_err() {
            return -1;
        }
        unsafe { msc_shim_finish_response_body(self.raw) }
    }
    pub fn process_logging(&mut self) -> i32 {
        unsafe { msc_shim_process_logging(self.raw) }
    }
    pub fn disruptive_status(&mut self) -> u16 {
        unsafe { msc_shim_disruptive_status(self.raw).clamp(0, 599) as u16 }
    }
}
impl Drop for Transaction {
    fn drop(&mut self) {
        unsafe { msc_shim_transaction_free(self.raw) }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn engine_initializes() {
        assert!(Engine::new().is_some());
    }
}
