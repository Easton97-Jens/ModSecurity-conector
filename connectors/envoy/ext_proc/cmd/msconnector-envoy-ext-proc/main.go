package main

import (
	"errors"
	"flag"
	"fmt"
	"net"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/processor"
	extprocv3 "github.com/envoyproxy/go-control-plane/envoy/service/ext_proc/v3"
	"google.golang.org/grpc"
)

type engineRuntime struct {
	engine         processor.Engine
	evaluationMode string
	ruleEvaluation string
	description    string
}

type engineCloser interface {
	Close() error
}

func main() {
	var configPath string
	var listenOverride string
	var eventLogPath string
	var runtimeConfigPath string
	var checkConfig bool
	flag.StringVar(&configPath, "config", "", "path to ext_proc JSON config")
	flag.StringVar(&listenOverride, "listen", "", "optional host:port override")
	flag.StringVar(&eventLogPath, "event-log", "", "optional absolute metadata-only JSONL evidence path")
	flag.StringVar(&runtimeConfigPath, "runtime-config", "", "path to Common/libmodsecurity runtime config")
	flag.BoolVar(&checkConfig, "check-config", false, "validate config and exit")
	flag.Parse()
	if configPath == "" {
		fmt.Fprintln(os.Stderr, "usage: msconnector_envoy_ext_proc --config PATH [--runtime-config PATH] [--listen HOST:PORT] [--event-log PATH] [--check-config]")
		os.Exit(2)
	}

	config, err := processor.LoadConfig(configPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "envoy_ext_proc: invalid config: %v\n", err)
		os.Exit(2)
	}
	if listenOverride != "" {
		config.ListenAddress = listenOverride
		if err := config.Validate(); err != nil {
			fmt.Fprintf(os.Stderr, "envoy_ext_proc: invalid listen override: %v\n", err)
			os.Exit(2)
		}
	}
	if checkConfig && runtimeConfigPath == "" {
		fmt.Printf("envoy_ext_proc: config-check-pass config=%s listen=%s\n", configPath, config.ListenAddress)
		return
	}

	runtime, err := configuredEngine(runtimeConfigPath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "envoy_ext_proc: engine setup: %v\n", err)
		os.Exit(2)
	}
	if closer, ok := runtime.engine.(engineCloser); ok {
		defer func() {
			if err := closer.Close(); err != nil {
				fmt.Fprintf(os.Stderr, "envoy_ext_proc: Common runtime cleanup: %v\n", err)
			}
		}()
	}
	if checkConfig {
		fmt.Printf("envoy_ext_proc: config-check-pass config=%s runtime_config=%s engine=%s listen=%s\n", configPath, runtimeConfigPath, runtime.description, config.ListenAddress)
		return
	}

	listener, err := net.Listen("tcp", config.ListenAddress)
	if err != nil {
		fmt.Fprintf(os.Stderr, "envoy_ext_proc: listen %s: %v\n", config.ListenAddress, err)
		os.Exit(1)
	}
	defer listener.Close()

	var observer processor.Observer
	var jsonlObserver *processor.JSONLObserver
	if eventLogPath != "" {
		jsonlObserver, err = processor.NewJSONLObserverWithMode(eventLogPath, runtime.evaluationMode, runtime.ruleEvaluation)
		if err != nil {
			fmt.Fprintf(os.Stderr, "envoy_ext_proc: event log: %v\n", err)
			os.Exit(2)
		}
		defer jsonlObserver.Close()
		observer = jsonlObserver
	}
	service, err := processor.NewServiceWithObserver(config, runtime.engine, observer)
	if err != nil {
		fmt.Fprintf(os.Stderr, "envoy_ext_proc: service setup: %v\n", err)
		os.Exit(1)
	}
	grpcServer := grpc.NewServer(
		grpc.MaxRecvMsgSize(config.MaxGRPCMessageBytes),
		grpc.MaxSendMsgSize(config.MaxGRPCMessageBytes),
	)
	extprocv3.RegisterExternalProcessorServer(grpcServer, service)
	fmt.Printf("envoy_ext_proc: serving integration_mode=ext_proc evaluation_mode=%s rule_evaluation=%s engine=%s listen=%s\n", runtime.evaluationMode, runtime.ruleEvaluation, runtime.description, config.ListenAddress)

	serveResult := make(chan error, 1)
	go func() {
		serveResult <- grpcServer.Serve(listener)
	}()

	signals := make(chan os.Signal, 1)
	signal.Notify(signals, syscall.SIGINT, syscall.SIGTERM)
	defer signal.Stop(signals)
	select {
	case err := <-serveResult:
		if err != nil && !errors.Is(err, grpc.ErrServerStopped) {
			fmt.Fprintf(os.Stderr, "envoy_ext_proc: serve: %v\n", err)
			os.Exit(1)
		}
		return
	case <-signals:
	}

	stopped := make(chan struct{})
	go func() {
		grpcServer.GracefulStop()
		close(stopped)
	}()
	select {
	case <-stopped:
	case <-time.After(time.Duration(config.ShutdownTimeoutMS) * time.Millisecond):
		grpcServer.Stop()
		<-stopped
	}
}
