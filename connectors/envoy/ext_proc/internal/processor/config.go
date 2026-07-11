// Package processor contains the Envoy-specific ext_proc stream adapter.
//
// It deliberately has no dependency on common/: Envoy protobuf types stay in
// this adapter until a separately-reviewed Common/libmodsecurity bridge exists.
package processor

import (
	"encoding/json"
	"fmt"
	"io"
	"net"
	"os"
	"strings"
	"time"
)

// LateActionPolicy describes the only intentionally supported outcomes for a
// disruptive decision discovered after the response-header boundary.
type LateActionPolicy string

const (
	LateActionMinimal LateActionPolicy = "minimal"
	LateActionSafe    LateActionPolicy = "safe"
	LateActionStrict  LateActionPolicy = "strict"
)

// Config is kept in connector-local JSON so its limits can be inspected without
// importing Envoy or Common configuration types. Duration values are expressed
// in milliseconds in the JSON file to avoid ambiguous Go duration encodings.
type Config struct {
	ListenAddress        string           `json:"listen_address"`
	TransactionIDHeader  string           `json:"transaction_id_header"`
	MaxHeaderCount       int              `json:"max_header_count"`
	MaxHeaderNameBytes   int              `json:"max_header_name_bytes"`
	MaxHeaderValueBytes  int              `json:"max_header_value_bytes"`
	MaxTotalHeaderBytes  int              `json:"max_total_header_bytes"`
	MaxBodyChunkBytes    int              `json:"max_body_chunk_bytes"`
	MaxRequestBodyBytes  int64            `json:"max_request_body_bytes"`
	MaxResponseBodyBytes int64            `json:"max_response_body_bytes"`
	MaxGRPCMessageBytes  int              `json:"max_grpc_message_bytes"`
	EngineTimeoutMS      int              `json:"engine_timeout_ms"`
	CleanupTimeoutMS     int              `json:"cleanup_timeout_ms"`
	ShutdownTimeoutMS    int              `json:"shutdown_timeout_ms"`
	LateActionPolicy     LateActionPolicy `json:"late_action_policy"`
}

// LoadConfig decodes and validates a service config without changing it.
func LoadConfig(path string) (Config, error) {
	file, err := os.Open(path)
	if err != nil {
		return Config{}, fmt.Errorf("open config: %w", err)
	}
	defer file.Close()

	decoder := json.NewDecoder(file)
	decoder.DisallowUnknownFields()
	var config Config
	if err := decoder.Decode(&config); err != nil {
		return Config{}, fmt.Errorf("decode config: %w", err)
	}
	if err := decoder.Decode(&struct{}{}); err != io.EOF {
		return Config{}, fmt.Errorf("decode config: expected one JSON object")
	}
	if err := config.Validate(); err != nil {
		return Config{}, err
	}
	return config, nil
}

// Validate rejects unsafe or internally inconsistent limits before the gRPC
// service is started.
func (config Config) Validate() error {
	if strings.TrimSpace(config.ListenAddress) == "" {
		return fmt.Errorf("config: listen_address is required")
	}
	if _, _, err := net.SplitHostPort(config.ListenAddress); err != nil {
		return fmt.Errorf("config: listen_address must be host:port: %w", err)
	}
	if strings.TrimSpace(config.TransactionIDHeader) == "" {
		return fmt.Errorf("config: transaction_id_header is required")
	}
	for name, value := range map[string]int{
		"max_header_count":       config.MaxHeaderCount,
		"max_header_name_bytes":  config.MaxHeaderNameBytes,
		"max_header_value_bytes": config.MaxHeaderValueBytes,
		"max_total_header_bytes": config.MaxTotalHeaderBytes,
		"max_body_chunk_bytes":   config.MaxBodyChunkBytes,
		"max_grpc_message_bytes": config.MaxGRPCMessageBytes,
		"engine_timeout_ms":      config.EngineTimeoutMS,
		"cleanup_timeout_ms":     config.CleanupTimeoutMS,
		"shutdown_timeout_ms":    config.ShutdownTimeoutMS,
	} {
		if value <= 0 {
			return fmt.Errorf("config: %s must be positive", name)
		}
	}
	if config.MaxRequestBodyBytes <= 0 || config.MaxResponseBodyBytes <= 0 {
		return fmt.Errorf("config: request and response body limits must be positive")
	}
	if config.MaxGRPCMessageBytes <= config.MaxBodyChunkBytes {
		return fmt.Errorf("config: max_grpc_message_bytes must exceed max_body_chunk_bytes")
	}
	switch config.LateActionPolicy {
	case LateActionMinimal, LateActionSafe, LateActionStrict:
	default:
		return fmt.Errorf("config: late_action_policy must be minimal, safe, or strict")
	}
	return nil
}

func (config Config) engineTimeout() time.Duration {
	return time.Duration(config.EngineTimeoutMS) * time.Millisecond
}

func (config Config) cleanupTimeout() time.Duration {
	return time.Duration(config.CleanupTimeoutMS) * time.Millisecond
}

func (config Config) shutdownTimeout() time.Duration {
	return time.Duration(config.ShutdownTimeoutMS) * time.Millisecond
}
