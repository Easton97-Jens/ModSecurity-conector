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
