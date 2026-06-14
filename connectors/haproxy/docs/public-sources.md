# HAProxy Public Sources

Status: current references

External sources document the HAProxy mechanisms used by the repository. They
do not by themselves promote connector behavior; promotion comes only from live
runtime evidence.

- HAProxy documentation: https://docs.haproxy.org/
- HAProxy configuration manual:
  https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/
- HAProxy SPOE/SPOP reference:
  https://raw.githubusercontent.com/haproxy/haproxy/master/doc/SPOE.txt
- HAProxy source: https://github.com/haproxy/haproxy

Repository source pins for clean-clone builds are centralized in
`modules/ModSecurity-test-Framework/ci/common.sh`. The current compile and
runtime flow is documented in `COMPILE_HAPROXY.md`.
