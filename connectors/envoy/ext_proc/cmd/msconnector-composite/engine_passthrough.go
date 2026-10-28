//go:build !libmodsecurity

package main

import (
	"fmt"
)

// A source-only build must never expose a serving connector. In particular,
// do not substitute PassthroughEngine here: it is allow-all by design and is
// appropriate only for isolated transport unit tests, never this executable.
func configuredEngine(_ string) (engineRuntime, error) {
	return engineRuntime{}, fmt.Errorf("msconnector-composite requires a libmodsecurity build and an explicit --runtime-config")
}
