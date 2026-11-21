fn main() {
    let root = std::env::var("MODSECURITY_ROOT")
        .unwrap_or_else(|_| "/var/tmp/codex/git/modsecurity-v3.0.17-prefix".to_string());
    println!("cargo:rerun-if-env-changed=MODSECURITY_ROOT");
    println!("cargo:rustc-link-search=native={root}/lib");
    println!("cargo:rustc-link-arg={root}/lib/libmodsecurity.so");
}
