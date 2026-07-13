//go:build libmodsecurity

package main

import (
	"fmt"
	"strings"

	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/processor"
)

func configuredEngine(runtimeConfigPath string) (engineRuntime, error) {
	if strings.TrimSpace(runtimeConfigPath) == "" {
		return engineRuntime{}, fmt.Errorf("--runtime-config is required by the libmodsecurity ext_proc bridge")
	}
	engine, err := processor.NewCommonRuntimeEngine(runtimeConfigPath)
	if err != nil {
		return engineRuntime{}, err
	}
	return engineRuntime{
		engine:         engine,
		evaluationMode: "common_libmodsecurity_nonpromoted",
		ruleEvaluation: "libmodsecurity",
		description:    "common_libmodsecurity",
	}, nil
}
