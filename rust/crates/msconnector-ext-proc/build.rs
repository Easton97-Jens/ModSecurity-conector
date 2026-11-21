fn main() -> Result<(), Box<dyn std::error::Error>> {
    let root = std::env::var("MODSECURITY_ROOT")
        .unwrap_or_else(|_| "/var/tmp/codex/git/modsecurity-v3.0.17-prefix".to_string());
    println!("cargo:rerun-if-env-changed=MODSECURITY_ROOT");
    println!("cargo:rustc-link-search=native={root}/lib");
    println!("cargo:rustc-link-arg={root}/lib/libmodsecurity.so");
    let root = "/var/tmp/codex/git/envoy";
    tonic_prost_build::configure()
        .build_server(true)
        .build_client(false)
        .compile_protos(
            &[
                format!("{root}/api/envoy/service/ext_proc/v3/external_processor.proto"),
            ],
            &[
                format!("{root}/api"),
                format!("{root}/bazel-bin"),
                "/usr/include".to_string(),
                "/var/tmp/codex/git/xds".to_string(),
                "/var/tmp/codex/git/protoc-gen-validate".to_string(),
            ],
        )?;
    Ok(())
}
