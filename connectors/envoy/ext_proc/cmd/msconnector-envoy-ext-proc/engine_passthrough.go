//go:build !libmodsecurity

package main

import (
	"fmt"
	"strings"

	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/processor"
)

// The source-only Go build remains useful for protobuf/unit tests. It must not
// accept a Common runtime config, because it has no C ABI or libmodsecurity
// linkage and therefore cannot imply rule evaluation.
func configuredEngine(runtimeConfigPath string) (engineRuntime, error) {
	if strings.TrimSpace(runtimeConfigPath) != "" {
		return engineRuntime{}, fmt.Errorf("this executable was built without the libmodsecurity bridge")
	}
	return engineRuntime{
		engine:         processor.PassthroughEngine{},
		evaluationMode: "passthrough_nonpromoted",
		ruleEvaluation: "not_wired",
		description:    "passthrough",
	}, nil
}
