<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# libmodsecurity v3 bauen

**Sprache:** [English](libmodsecurity.md) | Deutsch

## Offizielle Quellen

Die aktuelle [ModSecurity-README](https://github.com/owasp-modsecurity/ModSecurity) ist die primäre Buildquelle. Die [Compilation Recipes für v3.x](https://github.com/owasp-modsecurity/ModSecurity/wiki/Compilation-recipes-for-v3.x) dienen nur als ergänzender Hinweis für distributionsspezifische Abhängigkeiten. Historische CentOS-, Ubuntu- oder andere Beispiele daraus sind kein aktueller Standard.

## Voraussetzungen

Benötigt werden unter anderem:

- Git
- C- und C++-Compiler
- GNU Make
- Autoconf und Automake
- libtool
- Flex und Bison
- YAJL
- PCRE2

Die aktuelle README nennt YAJL als Pflichtabhängigkeit und PCRE2 als Standard für reguläre Ausdrücke. Für einen kompakten Einstieg sind diese gegen aktuelle Paketquellen geprüften Namen geeignet; nur den Block der eigenen Distribution ausführen.

```sh
# Debian / Ubuntu
sudo apt update
sudo apt install build-essential git autoconf automake libtool flex bison pkg-config libyajl-dev libpcre2-dev
```

```sh
# Fedora / RHEL
sudo dnf install gcc gcc-c++ make git autoconf automake libtool flex bison pkgconf-pkg-config yajl-devel pcre2-devel
```

## Einfacher offizieller Build

Wenn die benötigten Entwicklungspakete bereits installiert sind, verwendet der Standardweg diesen überprüften, im Repository dokumentierten Release. Er ist eine Reproduzierbarkeitsbasis und keine Aussage über den neuesten oder von Upstream unterstützten Release. Die GPG-Tag-Prüfung setzt einen vertrauenswürdigen Maintainer-Schlüssel voraus.

```sh
MODSECURITY_REF="v3.0.16"
MODSECURITY_COMMIT="7ea9fefbe0ba409d8733b4d682c8c4c059cd028d"
git clone --branch "$MODSECURITY_REF" --single-branch https://github.com/owasp-modsecurity/ModSecurity.git ModSecurity
cd ModSecurity
git fetch --tags origin
git verify-tag "$MODSECURITY_REF"
git checkout --detach "$MODSECURITY_REF"
test "$(git rev-parse HEAD)" = "$MODSECURITY_COMMIT"
git submodule update --init --recursive
git submodule status
./build.sh
./configure
make
make check
sudo make install
```

## Bedeutung der Befehle

| Befehl | Bedeutung |
| --- | --- |
| `MODSECURITY_REF="v3.0.16"` | Wählt den im Repository dokumentierten unveränderlichen Release-Tag aus. |
| `MODSECURITY_COMMIT="7ea9fefbe0ba409d8733b4d682c8c4c059cd028d"` | Hält den erwarteten unveränderlichen Commit für den ausgewählten Release fest. |
| `git clone --branch "$MODSECURITY_REF" --single-branch https://github.com/owasp-modsecurity/ModSecurity.git ModSecurity` | Lädt nur den ausgewählten ModSecurity-v3-Release in das lokale Source-Verzeichnis herunter. |
| `cd ModSecurity` | Wechselt in das heruntergeladene Verzeichnis. |
| `git fetch --tags origin` | Lädt Release-Tags vor der Signaturprüfung nach. |
| `git verify-tag "$MODSECURITY_REF"` | Prüft den ausgewählten signierten Release-Tag mit einem vertrauenswürdigen Maintainer-Schlüssel. |
| `git checkout --detach "$MODSECURITY_REF"` | Checkt den ausgewählten Tag im Detached-HEAD-Modus aus. |
| `test "$(git rev-parse HEAD)" = "$MODSECURITY_COMMIT"` | Bricht ab, wenn der ausgecheckte Commit nicht dem dokumentierten Release-Commit entspricht. |
| `git submodule update --init --recursive` | Lädt die zusätzlich benötigten Unterprojekte. |
| `git submodule status` | Prüft, ob die Unterprojekte vollständig vorhanden sind. |
| `./build.sh` | Erzeugt die benötigten Autotools-Builddateien. |
| `./configure` | Prüft Compiler und Bibliotheken und erstellt die Makefiles. |
| `make` | Kompiliert libmodsecurity. |
| `make check` | Führt die Upstream-Testsuite vor der Installation aus. |
| `sudo make install` | Installiert Header und Bibliothek systemweit. |

`build.sh` kompiliert die Bibliothek noch nicht. `configure` prüft die Umgebung. `make` kompiliert. `make install` installiert das Ergebnis.

## Erfolg prüfen

Der Standardprefix des offiziellen einfachen Builds ist `/usr/local/modsecurity`. Die Library liegt normalerweise darunter in `lib`; bewusst gewählte Plattformlayouts können `lib64` verwenden.

```sh
ls /usr/local/modsecurity/include/modsecurity
find /usr/local/modsecurity -maxdepth 2 -type f -name 'libmodsecurity.so*' -print
```

## Optional: Installation nur für den eigenen Benutzer

Nur diese Abweichung vom einfachen Ablauf verwenden:

```sh
./configure --prefix="$HOME/.local/modsecurity"
make
make install
```

Dabei wird nicht systemweit installiert und `sudo` ist nicht erforderlich.

## Fortgeschrittene und reproduzierbare Builds

Dieser Abschnitt ist für bewusst gepinnte oder lokale Entwicklungsbuilds. Ein fester Release-Tag und der erwartete Commit machen die Eingabe nachvollziehbar. Eine GPG-Tag-Prüfung setzt einen vertrauenswürdigen Maintainer-Schlüssel voraus; bei Releasearchiven zusätzlich die veröffentlichte SHA-Prüfsumme vor dem Entpacken prüfen.

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

Hier gehören eigener Installationsprefix, `PKG_CONFIG_PATH`, `LD_LIBRARY_PATH`, parallele Buildjobs, `CFLAGS`, `CXXFLAGS`, `LDFLAGS`, `make check` und die Build-Provenienz hin. Bei `lib64` statt `lib` die Pfadangaben bewusst anpassen; `LD_LIBRARY_PATH` nur für lokale Entwicklung und Tests verwenden, nicht als globale Loader-Konfiguration.
