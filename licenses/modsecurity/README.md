# ModSecurity Engine Reference Sources

Status: implemented

The ModSecurity engine repositories are read-only reference inputs for this
monorepo. Engine source files are not imported here.

## Observed Local References

| Source | Branch | Commit | Describe | Role |
| --- | --- | --- | --- | --- |
| `/root/conecter/ModSecurity_V2` | `v2/master` | `02eed22d74667b32091eece088a8ebdf64b6ba67` | `v2.9.13` | Regression, semantic, and compatibility reference |
| `/root/conecter/ModSecurity_V3` | `v3/master` | `0fb4aff98b4980cf6426697d5605c424e3d5bb60` | `v3.0.15` | Primary libmodsecurity v3 architecture/API reference |

## License Observation

Both local reference repositories contain an Apache License 2.0 `LICENSE` file.
This monorepo does not copy ModSecurity engine source files into `common/` or
connector source trees. Any future engine-source import must add a file-level
origin map before code is copied.

## Boundary

- V3 is the primary API and architecture reference.
- V2 is used for regression, semantic, compatibility, and historical reference.
- Neither reference repository may be modified by this monorepo's build,
  smoke, or documentation workflows.
