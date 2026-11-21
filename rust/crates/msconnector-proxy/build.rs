fn main() {
    let root = std::env::var("MODSECURITY_ROOT").unwrap_or_else(|_| "/usr".to_string());
    let lib = format!("{root}/lib");
    let library = format!("{lib}/libmodsecurity.so");
    println!("cargo:rerun-if-env-changed=MODSECURITY_ROOT");
    println!("cargo:rustc-link-search=native={lib}");
    println!("cargo:rustc-link-arg={library}");
}
