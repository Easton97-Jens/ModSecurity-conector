fn main() {
    println!("cargo:rerun-if-changed=shim/modsecurity_shim.cpp");
    println!("cargo:rerun-if-changed=shim/modsecurity_shim.h");
    let root = std::env::var("MODSECURITY_ROOT").unwrap_or_else(|_| "/usr".to_string());
    let include = format!("{root}/include");
    let lib = format!("{root}/lib");
    let library = format!("{lib}/libmodsecurity.so");
    println!("cargo:rerun-if-env-changed=MODSECURITY_ROOT");
    println!("cargo:rustc-link-search=native={lib}");
    println!("cargo:rustc-link-arg={library}");
    cc::Build::new()
        .cpp(true)
        .std("c++17")
        .include(include)
        .file("shim/modsecurity_shim.cpp")
        .compile("msconnector_modsecurity_shim");
}
