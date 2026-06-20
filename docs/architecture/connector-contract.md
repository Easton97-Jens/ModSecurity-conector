# Connector Contract

Connector implementations must preserve the evidence gates in
[new connector onboarding](new-connector-onboarding.md). New connectors start as
roadmap-only candidates or skeletons and become runtime connectors only after
real runtime artifacts prove the behavior being claimed.

This contract is intentionally evidence-first:

- connector-neutral code stays in `common/`;
- adapter-owned code stays in `connectors/<name>/`;
- generated reports must be produced by generators, not edited manually;
- runtime claims require `result.json` plus logs/evidence;
- full-matrix claims require generated Full-Matrix evidence;
- OpenResty is covered by NGINX unless a future decision explicitly changes that.

See [new connector onboarding](new-connector-onboarding.md) for lifecycle stages,
acceptance criteria, Envoy first proof requirements, LiteSpeed planned proof, and
claims that are forbidden before Full-Matrix evidence exists.
