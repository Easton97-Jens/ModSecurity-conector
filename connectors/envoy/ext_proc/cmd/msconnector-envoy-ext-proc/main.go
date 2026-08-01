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
	engine         processor.TransactionOpener
	evaluationMode string
	ruleEvaluation string
	description    string
}

type engineCloser interface {
	Close() error
}

func main() {
	exitCode, err := run()
	if err != nil {
		if _, ok := err.(usageError); ok {
			fmt.Fprintln(os.Stderr, err)
		} else {
			fmt.Fprintf(os.Stderr, "envoy_ext_proc: %v\n", err)
		}
		os.Exit(exitCode)
	}
}

type usageError struct{}

func (usageError) Error() string {
	return "usage: msconnector_envoy_ext_proc --config PATH [--runtime-config PATH] [--listen HOST:PORT] [--event-log PATH] [--check-config]"
}

type commandLineOptions struct {
	configPath        string
	listenOverride    string
	eventLogPath      string
	runtimeConfigPath string
	checkConfig       bool
}

func run() (int, error) {
	options, err := parseCommandLine()
	if err != nil {
		return 2, err
	}
	config, err := loadServiceConfig(options)
	if err != nil {
		return 2, err
	}
	if options.checkConfig && options.runtimeConfigPath == "" {
		fmt.Printf("envoy_ext_proc: config-check-pass config=%s listen=%s\n", options.configPath, config.ListenAddress)
		return 0, nil
	}
	runtime, err := configuredEngine(options.runtimeConfigPath)
	if err != nil {
		return 2, fmt.Errorf("engine setup: %w", err)
	}
	defer closeEngine(runtime)
	if options.checkConfig {
		fmt.Printf("envoy_ext_proc: config-check-pass config=%s runtime_config=%s engine=%s listen=%s\n", options.configPath, options.runtimeConfigPath, runtime.description, config.ListenAddress)
		return 0, nil
	}
	return serve(config, runtime, options.eventLogPath)
}

func parseCommandLine() (commandLineOptions, error) {
	var options commandLineOptions
	flag.StringVar(&options.configPath, "config", "", "path to ext_proc JSON config")
	flag.StringVar(&options.listenOverride, "listen", "", "optional host:port override")
	flag.StringVar(&options.eventLogPath, "event-log", "", "optional absolute metadata-only JSONL evidence path")
	flag.StringVar(&options.runtimeConfigPath, "runtime-config", "", "path to Common/libmodsecurity runtime config")
	flag.BoolVar(&options.checkConfig, "check-config", false, "validate config and exit")
	flag.Parse()
	if options.configPath == "" {
		return commandLineOptions{}, usageError{}
	}
	return options, nil
}

func loadServiceConfig(options commandLineOptions) (processor.Config, error) {
	config, err := processor.LoadConfig(options.configPath)
	if err != nil {
		return processor.Config{}, fmt.Errorf("invalid config: %w", err)
	}
	if options.listenOverride != "" {
		config.ListenAddress = options.listenOverride
		if err := config.Validate(); err != nil {
			return processor.Config{}, fmt.Errorf("invalid listen override: %w", err)
		}
	}
	return config, nil
}

func closeEngine(runtime engineRuntime) {
	if closer, ok := runtime.engine.(engineCloser); ok {
		if err := closer.Close(); err != nil {
			fmt.Fprintf(os.Stderr, "envoy_ext_proc: Common runtime cleanup: %v\n", err)
		}
	}
}

func serve(config processor.Config, runtime engineRuntime, eventLogPath string) (int, error) {
	listener, err := net.Listen("tcp", config.ListenAddress)
	if err != nil {
		return 1, fmt.Errorf("listen %s: %w", config.ListenAddress, err)
	}
	defer listener.Close()
	observer, observerCloser, err := newObserver(eventLogPath, runtime)
	if err != nil {
		return 2, fmt.Errorf("event log: %w", err)
	}
	if observerCloser != nil {
		defer observerCloser.Close()
	}
	service, err := processor.NewServiceWithObserver(config, runtime.engine, observer)
	if err != nil {
		return 1, fmt.Errorf("service setup: %w", err)
	}
	grpcServer := grpc.NewServer(
		grpc.MaxRecvMsgSize(config.MaxGRPCMessageBytes),
		grpc.MaxSendMsgSize(config.MaxGRPCMessageBytes),
	)
	extprocv3.RegisterExternalProcessorServer(grpcServer, service)
	fmt.Printf("envoy_ext_proc: serving integration_mode=ext_proc evaluation_mode=%s rule_evaluation=%s engine=%s listen=%s\n", runtime.evaluationMode, runtime.ruleEvaluation, runtime.description, config.ListenAddress)
	return waitForServerTermination(grpcServer, listener, config.ShutdownTimeoutMS)
}

func newObserver(eventLogPath string, runtime engineRuntime) (processor.Observer, *processor.JSONLObserver, error) {
	if eventLogPath == "" {
		return nil, nil, nil
	}
	observer, err := processor.NewJSONLObserverWithMode(eventLogPath, runtime.evaluationMode, runtime.ruleEvaluation)
	if err != nil {
		return nil, nil, err
	}
	return observer, observer, nil
}

func waitForServerTermination(grpcServer *grpc.Server, listener net.Listener, shutdownTimeoutMS int) (int, error) {
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
			return 1, fmt.Errorf("serve: %w", err)
		}
		return 0, nil
	case <-signals:
	}

	stopped := make(chan struct{})
	go func() {
		grpcServer.GracefulStop()
		close(stopped)
	}()
	select {
	case <-stopped:
	case <-time.After(time.Duration(shutdownTimeoutMS) * time.Millisecond):
		grpcServer.Stop()
		<-stopped
	}
	return 0, nil
}
