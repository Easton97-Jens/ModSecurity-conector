package main

import (
	"context"
	"crypto/rand"
	"errors"
	"flag"
	"fmt"
	"net"
	"net/http"
	"os"
	"os/signal"
	"strings"
	"syscall"
	"time"

	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/composite"
	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/compositeenvoy"
	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/compositetraefik"
	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/processor"
	authv3 "github.com/envoyproxy/go-control-plane/envoy/service/auth/v3"
	extprocv3 "github.com/envoyproxy/go-control-plane/envoy/service/ext_proc/v3"
	"google.golang.org/grpc"
)

const (
	shutdownTimeout = 5 * time.Second
	maxGRPCMessage  = 256 << 10
)

type options struct {
	mode          string
	listen        string
	forwardAuth   string
	uds           string
	runtimeConfig string
	eventLog      string
}

type engineRuntime struct {
	engine processor.TransactionOpener
	close  func(context.Context) error
}

func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, "msconnector-composite:", err)
		os.Exit(1)
	}
}

func run() error {
	opts, err := parseOptions()
	if err != nil {
		return err
	}
	runtime, err := configuredEngine(opts.runtimeConfig)
	if err != nil {
		return fmt.Errorf("engine setup: %w", err)
	}
	defer func() {
		ctx, cancel := context.WithTimeout(context.Background(), shutdownTimeout)
		defer cancel()
		_ = runtime.close(ctx)
	}()
	key := make([]byte, 32)
	if _, err := rand.Read(key); err != nil {
		return fmt.Errorf("generate process key: %w", err)
	}
	observer, closeObserver, err := newCompositeObserver(opts.eventLog)
	if err != nil {
		return err
	}
	if closeObserver != nil {
		defer closeObserver.Close()
	}
	coordinator, err := composite.New(opts.mode, key, composite.Limits{
		Capacity:        128,
		TTL:             30 * time.Second,
		IdleTTL:         5 * time.Second,
		MaxRequestBody:  32,
		MaxResponseBody: 1 << 20,
		MaxBodyChunks:   256,
		MaxHeaders:      256,
		MaxHeaderBytes:  64 << 10,
	}, runtime.engine, observer)
	if err != nil {
		return fmt.Errorf("coordinator setup: %w", err)
	}
	defer func() {
		// Drain and close the coordinator before releasing the Common engine;
		// retained transactions must never outlive their native owner.
		coordinator.Close()
	}()

	var serveErr error
	switch opts.mode {
	case "envoy":
		serveErr = serveEnvoy(opts.listen, coordinator)
	case "traefik":
		serveErr = serveTraefik(opts.forwardAuth, opts.uds, coordinator)
	default:
		serveErr = errors.New("unsupported mode")
	}
	// The coordinator dispatches terminal events asynchronously. Explicitly
	// drain it before inspecting or closing the observer, otherwise a final
	// Allow/P4/cleanup record could still be queued and its write failure would
	// be missed. The deferred idempotent cleanup remains for early failures.
	coordinator.Close()
	coordinatorErr := coordinator.Err()
	observerErr := observer.Err()
	observerCloseErr := closeObserver.Close()
	ctx, cancel := context.WithTimeout(context.Background(), shutdownTimeout)
	engineCloseErr := runtime.close(ctx)
	cancel()
	return shutdownResult(serveErr, coordinatorErr, observerErr, observerCloseErr, engineCloseErr)
}

// shutdownResult makes the fail-closed shutdown precedence explicit. A
// coordinator fault indicates that lifecycle evidence may be incomplete, so
// it supersedes serving and dependent observer/cleanup errors.
func shutdownResult(serveErr, coordinatorErr, observerErr, observerCloseErr, engineCloseErr error) error {
	if coordinatorErr != nil {
		return fmt.Errorf("coordinator failed: %w", coordinatorErr)
	}
	if observerErr != nil {
		return fmt.Errorf("metadata event evidence failed: %w", observerErr)
	}
	if observerCloseErr != nil {
		return fmt.Errorf("metadata event close: %w", observerCloseErr)
	}
	if engineCloseErr != nil {
		return fmt.Errorf("engine cleanup: %w", engineCloseErr)
	}
	return serveErr
}

func parseOptions() (options, error) {
	var o options
	flag.StringVar(&o.mode, "mode", "", "connector mode: envoy or traefik")
	flag.StringVar(&o.listen, "listen", "", "loopback TCP address for Envoy gRPC")
	flag.StringVar(&o.forwardAuth, "forwardauth-listen", "", "loopback TCP address for Traefik ForwardAuth")
	flag.StringVar(&o.uds, "uds", "", "private absolute Unix socket path for the Traefik companion")
	flag.StringVar(&o.runtimeConfig, "runtime-config", "", "Common/libmodsecurity runtime configuration")
	flag.StringVar(&o.eventLog, "event-log", "", "absolute metadata-only JSONL event path")
	flag.Parse()
	if o.mode != "envoy" && o.mode != "traefik" {
		return options{}, errors.New("--mode must be exactly envoy or traefik")
	}
	if o.mode == "envoy" {
		if err := validateLoopbackAddress(o.listen); err != nil {
			return options{}, fmt.Errorf("--listen: %w", err)
		}
		if o.forwardAuth != "" || o.uds != "" {
			return options{}, errors.New("Traefik listener options are not valid in Envoy mode")
		}
	} else {
		if o.listen != "" {
			return options{}, errors.New("--listen is not valid in Traefik mode")
		}
		if err := validateLoopbackAddress(o.forwardAuth); err != nil {
			return options{}, fmt.Errorf("--forwardauth-listen: %w", err)
		}
		if o.uds == "" {
			return options{}, errors.New("--uds is required in Traefik mode")
		}
	}
	if o.eventLog == "" || !isAbsolutePath(o.eventLog) {
		return options{}, errors.New("--event-log must be an explicit absolute metadata-only JSONL path")
	}
	return o, nil
}

func validateLoopbackAddress(address string) error {
	if strings.TrimSpace(address) == "" {
		return errors.New("an explicit loopback host:port is required")
	}
	host, _, err := net.SplitHostPort(address)
	if err != nil {
		return errors.New("must be a host:port address")
	}
	ip := net.ParseIP(host)
	if ip == nil || !ip.IsLoopback() {
		return errors.New("must bind to a numeric loopback address, never a DNS or public address")
	}
	return nil
}

func isAbsolutePath(path string) bool {
	return path != "" && strings.HasPrefix(path, "/")
}

func serveEnvoy(address string, coordinator *composite.Coordinator) error {
	listener, err := net.Listen("tcp", address)
	if err != nil {
		return fmt.Errorf("listen Envoy gRPC: %w", err)
	}
	defer listener.Close()
	authz, err := compositeenvoy.NewAuthzServer(coordinator)
	if err != nil {
		return err
	}
	extproc, err := compositeenvoy.NewExtProcServer(coordinator)
	if err != nil {
		return err
	}
	server := grpc.NewServer(
		grpc.MaxRecvMsgSize(maxGRPCMessage),
		grpc.MaxSendMsgSize(maxGRPCMessage),
		grpc.MaxConcurrentStreams(128),
	)
	authv3.RegisterAuthorizationServer(server, authz)
	extprocv3.RegisterExternalProcessorServer(server, extproc)
	return serveGRPCUntilSignal(server, listener)
}

func serveGRPCUntilSignal(server *grpc.Server, listener net.Listener) error {
	serveDone := make(chan error, 1)
	go func() { serveDone <- server.Serve(listener) }()
	signals := make(chan os.Signal, 1)
	signal.Notify(signals, syscall.SIGINT, syscall.SIGTERM)
	defer signal.Stop(signals)
	select {
	case err := <-serveDone:
		if err != nil && !errors.Is(err, grpc.ErrServerStopped) {
			return err
		}
		return nil
	case <-signals:
	}
	finished := make(chan struct{})
	go func() { server.GracefulStop(); close(finished) }()
	timer := time.NewTimer(shutdownTimeout)
	defer timer.Stop()
	select {
	case <-finished:
		return nil
	case <-timer.C:
		server.Stop()
		return errors.New("Envoy gRPC graceful shutdown exceeded deadline")
	}
}

func serveTraefik(forwardAuthAddress, udsPath string, coordinator *composite.Coordinator) error {
	udsListener, err := compositetraefik.ListenPrivate(udsPath)
	if err != nil {
		return fmt.Errorf("listen Traefik companion UDS: %w", err)
	}
	defer udsListener.Close()
	httpListener, err := net.Listen("tcp", forwardAuthAddress)
	if err != nil {
		return fmt.Errorf("listen Traefik ForwardAuth: %w", err)
	}
	defer httpListener.Close()
	forwardAuth := &compositetraefik.ForwardAuth{Coordinator: coordinator, Config: compositetraefik.ForwardAuthConfig{MaxBodyBytes: 32}}
	httpServer := &http.Server{Handler: forwardAuth, ReadHeaderTimeout: 2 * time.Second, ReadTimeout: 5 * time.Second, WriteTimeout: 5 * time.Second, IdleTimeout: 5 * time.Second}
	udsServer := &compositetraefik.UDS{Coordinator: coordinator, Timeout: 5 * time.Second}
	serveErr := make(chan error, 2)
	go func() { serveErr <- httpServer.Serve(httpListener) }()
	go func() { serveErr <- udsServer.Serve(udsListener) }()
	signals := make(chan os.Signal, 1)
	signal.Notify(signals, syscall.SIGINT, syscall.SIGTERM)
	defer signal.Stop(signals)
	select {
	case err := <-serveErr:
		if err != nil && !errors.Is(err, http.ErrServerClosed) && !errors.Is(err, net.ErrClosed) {
			return err
		}
		return nil
	case <-signals:
	}
	ctx, cancel := context.WithTimeout(context.Background(), shutdownTimeout)
	defer cancel()
	_ = httpServer.Shutdown(ctx)
	_ = udsListener.Close()
	return nil
}
