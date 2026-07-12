# Traefik Public Sources

**Language:** English | [Deutsch](public-sources.de.md)

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

The standard compatibility path remains the repo-owned local decision-service
starter plus metadata build starter. The separately repo-owned
`native_middleware/` package follows the documented Go middleware entry-point
shape and includes a local `.traefik.yml`. The full-lifecycle host probe stages
it in a pinned Traefik local-plugin workspace, selects a private persistent UDS
Common/libmodsecurity engine, and records targeted metadata-only P1--P4-safe
host outcomes. That evidence does not promote any rule capability.
