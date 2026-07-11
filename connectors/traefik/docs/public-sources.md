# Traefik Public Sources

Status: reference-only
Runtime status: not-verified

The links below were previously recorded as public Traefik reference material
for candidate integration research. They are not imported source, build
evidence, or runtime evidence and do not prove that a ModSecurity connector is
implemented here.

- https://doc.traefik.io/traefik/extend/extend-traefik/
- https://doc.traefik.io/traefik/master/reference/install-configuration/experimental/plugins/
- https://doc.traefik.io/traefik/v3.7/reference/routing-configuration/http/middlewares/forwardauth/
- https://plugins.traefik.io/create

The selected implemented Traefik path remains the repo-owned local
decision-service starter plus metadata build starter. The separately
repo-owned `native_middleware/` package follows the documented Go middleware
entry-point shape and includes a local `.traefik.yml`, but it is source/build
groundwork only. Any selection of that or another path must be tied to
repository-backed origin, license, configuration, build, and runtime evidence.
