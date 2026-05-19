#!/bin/sh
set -eu

VENV_DIR="${VENV_DIR:-.venv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
REQ_FILE="${REQ_FILE:-requirements-dev.txt}"

if [ ! -f "$REQ_FILE" ]; then
    echo "blocked: missing dependency file: $REQ_FILE" >&2
    exit 2
fi

"$PYTHON_BIN" -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install -r "$REQ_FILE"

echo "ok: created virtual environment at $VENV_DIR"
echo "hint: source $VENV_DIR/bin/activate"
