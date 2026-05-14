# Apache Build

Status: scaffolded

Observed local source uses Autotools and `apxs`:

- `configure.ac`
- `Makefile.am`
- `build/apxs-wrapper.in`

No Apache build is implemented in this repository.

TODO:

- Verify minimum Apache and APR requirements.
- Decide whether to reuse Autotools concepts or provide a new build wrapper.
- Add CI only after a local build is reproducible.
