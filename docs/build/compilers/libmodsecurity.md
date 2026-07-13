<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Build libmodsecurity v3

**Language:** English | [Deutsch](libmodsecurity.de.md)

## Official sources

The current [ModSecurity README](https://github.com/owasp-modsecurity/ModSecurity) is the primary build source. The [v3.x compilation recipes](https://github.com/owasp-modsecurity/ModSecurity/wiki/Compilation-recipes-for-v3.x) are only supplementary context for distribution-specific dependencies. Historical CentOS, Ubuntu, or other examples there are not a current default.

## Prerequisites

Among the required tools and development packages are:

- Git
- C and C++ compilers
- GNU Make
- Autoconf and Automake
- libtool
- Flex and Bison
- YAJL
- PCRE2

The current README identifies YAJL as mandatory and PCRE2 as the default regex engine. These compact package names were checked against current package sources; run only the block for the distribution in use.

```sh
# Debian / Ubuntu
sudo apt update
sudo apt install build-essential git autoconf automake libtool flex bison pkg-config libyajl-dev libpcre2-dev
```

```sh
# Fedora / RHEL
sudo dnf install gcc gcc-c++ make git autoconf automake libtool flex bison pkgconf-pkg-config yajl-devel pcre2-devel
```

## Simple official build

Once the required development packages are installed, the official Unix build is essentially these eight commands:

```sh
git clone https://github.com/owasp-modsecurity/ModSecurity.git
cd ModSecurity
git submodule update --init --recursive
git submodule status
./build.sh
./configure
make
sudo make install
```

## Meaning of the commands

| Command | Meaning |
| --- | --- |
| `git clone https://github.com/owasp-modsecurity/ModSecurity.git` | Downloads the ModSecurity v3 source code. |
| `cd ModSecurity` | Changes into the downloaded directory. |
| `git submodule update --init --recursive` | Downloads the additional required subprojects. |
| `git submodule status` | Checks that the subprojects are present completely. |
| `./build.sh` | Creates the required Autotools build files. |
| `./configure` | Checks compilers and libraries and creates the Makefiles. |
| `make` | Compiles libmodsecurity. |
| `sudo make install` | Installs headers and the library system-wide. |

`build.sh` does not compile the library yet. `configure` checks the environment. `make` compiles. `make install` installs the result.

## Check the result

```sh
ls /usr/local/include/modsecurity
ls /usr/local/lib | grep modsecurity
```

Depending on the system, the library can be under `/usr/local/lib`, `/usr/local/lib64`, or a distribution-specific path.

## Optional: installation for the current user only

Show only this deviation from the simple flow:

```sh
./configure --prefix="$HOME/.local/modsecurity"
make
make install
```

This does not install system-wide and does not require `sudo`.

## Advanced and reproducible builds

Use this section for deliberately pinned or local development builds. A fixed release tag and expected commit make the input traceable. GPG tag verification requires a trusted maintainer key; for release archives, also verify the published SHA checksum before unpacking.

```sh
MODSECURITY_REF="v3.0.16"
MODSECURITY_COMMIT="7ea9fefbe0ba409d8733b4d682c8c4c059cd028d"
git -C ModSecurity fetch --tags origin
git -C ModSecurity checkout --detach "$MODSECURITY_REF"
test "$(git -C ModSecurity rev-parse HEAD)" = "$MODSECURITY_COMMIT"
git -C ModSecurity verify-tag "$MODSECURITY_REF"
git -C ModSecurity submodule status
MODSECURITY_PREFIX="$HOME/.local/modsecurity"
cd ModSecurity
export CFLAGS="-O2 -g"
export CXXFLAGS="-O2 -g"
export LDFLAGS="-Wl,-rpath,$MODSECURITY_PREFIX/lib"
./configure --prefix="$MODSECURITY_PREFIX"
JOBS="$(getconf _NPROCESSORS_ONLN 2>/dev/null || printf 2)"
make -j"$JOBS"
make check
make install
export PKG_CONFIG_PATH="$MODSECURITY_PREFIX/lib/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}"
export LD_LIBRARY_PATH="$MODSECURITY_PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
{ git rev-parse HEAD; git submodule status; cc --version; c++ --version; } > build-provenance.txt
```

This is where an own installation prefix, `PKG_CONFIG_PATH`, `LD_LIBRARY_PATH`, parallel build jobs, `CFLAGS`, `CXXFLAGS`, `LDFLAGS`, `make check`, and build provenance belong. Adjust paths deliberately when the system uses `lib64`; use `LD_LIBRARY_PATH` only for local development and tests, not as global loader configuration.
