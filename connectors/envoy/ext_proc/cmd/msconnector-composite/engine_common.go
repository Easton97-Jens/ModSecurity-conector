//go:build libmodsecurity

package main

import (
	"context"
	"fmt"
	"strings"

	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/processor"
)

func configuredEngine(runtimeConfigPath, mode string) (engineRuntime, error) {
	var compositeMode processor.CompositeMode
	switch mode {
	case "envoy":
		compositeMode = processor.CompositeModeEnvoy
	case "traefik":
		compositeMode = processor.CompositeModeTraefik
	default:
		return engineRuntime{}, fmt.Errorf("unsupported composite mode %q", mode)
	}
	if strings.TrimSpace(runtimeConfigPath) == "" {
		return engineRuntime{}, fmt.Errorf("--runtime-config is required by the libmodsecurity bridge")
	}
	engine, err := processor.NewCompositeRuntimeEngine(runtimeConfigPath, compositeMode)
	if err != nil {
		return engineRuntime{}, err
	}
	return engineRuntime{
		engine: engine,
		close: func(ctx context.Context) error {
			return engine.Close(ctx)
		},
	}, nil
}
