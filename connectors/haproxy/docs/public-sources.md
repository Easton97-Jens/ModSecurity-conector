# HAProxy Public Sources

**Language:** English | [Deutsch](public-sources.de.md)

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
`modules/ModSecurity-test-Framework/ci/lib/common.sh`. The standard compile and
runtime flow is documented in `docs/build/compilers/haproxy.md`. The separate
full-lifecycle HTX observer is pinned to HAProxy 3.2.21 and copied into a
disposable worktree; that source selection does not turn the observer into an
enforcement or capability-promotion path.
