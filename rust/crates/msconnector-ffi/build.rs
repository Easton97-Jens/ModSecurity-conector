fn main() {
    println!("cargo:rerun-if-changed=shim/modsecurity_shim.cpp");
    println!("cargo:rerun-if-changed=shim/modsecurity_shim.h");
    println!("cargo:rustc-link-search=native=/var/tmp/codex/git/modsecurity-v3.0.17-prefix/lib");
    println!("cargo:rustc-link-arg=/var/tmp/codex/git/modsecurity-v3.0.17-prefix/lib/libmodsecurity.so.3.0.17");
    cc::Build::new()
        .cpp(true)
        .std("c++17")
        .include("/var/tmp/codex/git/modsecurity-v3.0.17-prefix/include")
        .file("shim/modsecurity_shim.cpp")
        .compile("msconnector_modsecurity_shim");
}
