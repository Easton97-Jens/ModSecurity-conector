use msconnector_ffi::{Engine, Rules, Transaction};
use std::ffi::{c_char, CStr};
use std::panic::{catch_unwind, AssertUnwindSafe};
use std::ptr;

#[repr(C)]
pub struct MscRustEngine {
    engine: Engine,
    rules: Rules,
}

#[unsafe(no_mangle)]
pub extern "C" fn msc_rust_engine_new(rules_path: *const c_char) -> *mut MscRustEngine {
    if rules_path.is_null() {
        return ptr::null_mut();
    }
    let result = catch_unwind(AssertUnwindSafe(|| {
        let path = unsafe { CStr::from_ptr(rules_path) }.to_string_lossy();
        let mut engine = Engine::new()?;
        let rules = engine.load_rules(path.as_ref()).ok()?;
        Some(MscRustEngine { engine, rules })
    }));
    match result {
        Ok(Some(engine)) => Box::into_raw(Box::new(engine)),
        _ => ptr::null_mut(),
    }
}

#[unsafe(no_mangle)]
pub extern "C" fn msc_rust_engine_free(engine: *mut MscRustEngine) {
    let _ = catch_unwind(AssertUnwindSafe(|| {
        if !engine.is_null() {
            unsafe { drop(Box::from_raw(engine)) };
        }
    }));
}

#[unsafe(no_mangle)]
pub extern "C" fn msc_rust_transaction_new(
    engine: *mut MscRustEngine,
    id: *const c_char,
) -> *mut Transaction {
    if engine.is_null() || id.is_null() {
        return ptr::null_mut();
    }
    let result = catch_unwind(AssertUnwindSafe(|| {
        let engine = unsafe { &mut *engine };
        let id = unsafe { CStr::from_ptr(id) }.to_string_lossy().into_owned();
        Transaction::new(&engine.engine, &engine.rules, id)
    }));
    match result {
        Ok(Some(transaction)) => Box::into_raw(Box::new(transaction)),
        _ => ptr::null_mut(),
    }
}

#[unsafe(no_mangle)]
pub extern "C" fn msc_rust_transaction_free(transaction: *mut Transaction) {
    let _ = catch_unwind(AssertUnwindSafe(|| {
        if !transaction.is_null() {
            unsafe { drop(Box::from_raw(transaction)) };
        }
    }));
}

#[unsafe(no_mangle)]
pub extern "C" fn msc_rust_process_connection(
    transaction: *mut Transaction,
    client_ip: *const c_char,
) -> i32 {
    if transaction.is_null() || client_ip.is_null() {
        return -1;
    }
    catch_unwind(AssertUnwindSafe(|| {
        let transaction = unsafe { &mut *transaction };
        let client_ip = unsafe { CStr::from_ptr(client_ip) }.to_string_lossy();
        transaction.process_connection(client_ip.as_ref())
    }))
    .unwrap_or(-1)
}

#[unsafe(no_mangle)]
pub extern "C" fn msc_rust_process_uri(
    transaction: *mut Transaction,
    uri: *const c_char,
    protocol: *const c_char,
    http_version: *const c_char,
) -> i32 {
    if transaction.is_null() || uri.is_null() {
        return -1;
    }
    catch_unwind(AssertUnwindSafe(|| {
        let transaction = unsafe { &mut *transaction };
        let uri = unsafe { CStr::from_ptr(uri) }.to_string_lossy();
        let protocol = if protocol.is_null() {
            "http"
        } else {
            unsafe { CStr::from_ptr(protocol) }
                .to_str()
                .unwrap_or("http")
        };
        let http_version = if http_version.is_null() {
            "1.1"
        } else {
            unsafe { CStr::from_ptr(http_version) }
                .to_str()
                .unwrap_or("1.1")
        };
        transaction.process_uri(uri.as_ref(), protocol, http_version)
    }))
    .unwrap_or(-1)
}

#[unsafe(no_mangle)]
pub extern "C" fn msc_rust_process_request_headers(transaction: *mut Transaction) -> i32 {
    if transaction.is_null() {
        return -1;
    }
    catch_unwind(AssertUnwindSafe(|| {
        unsafe { &mut *transaction }.process_request_headers()
    }))
    .unwrap_or(-1)
}

#[unsafe(no_mangle)]
pub extern "C" fn msc_rust_append_request_body(
    transaction: *mut Transaction,
    data: *const u8,
    len: usize,
) -> i32 {
    if transaction.is_null() || (len > 0 && data.is_null()) {
        return -1;
    }
    catch_unwind(AssertUnwindSafe(|| {
        let bytes = if len == 0 {
            &[][..]
        } else {
            unsafe { std::slice::from_raw_parts(data, len) }
        };
        unsafe { &mut *transaction }.append_request_body(bytes)
    }))
    .unwrap_or(-1)
}

#[unsafe(no_mangle)]
pub extern "C" fn msc_rust_finish_request_body(transaction: *mut Transaction) -> i32 {
    if transaction.is_null() {
        return -1;
    }
    catch_unwind(AssertUnwindSafe(|| {
        unsafe { &mut *transaction }.finish_request_body()
    }))
    .unwrap_or(-1)
}

#[unsafe(no_mangle)]
pub extern "C" fn msc_rust_disruptive_status(transaction: *mut Transaction) -> i32 {
    if transaction.is_null() {
        return 0;
    }
    catch_unwind(AssertUnwindSafe(|| {
        unsafe { &mut *transaction }.disruptive_status() as i32
    }))
    .unwrap_or(0)
}
