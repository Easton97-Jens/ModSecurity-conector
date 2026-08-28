package main

import (
	"flag"
	"fmt"
	"net"
	"os"
	"os/signal"
	"path/filepath"
	"runtime"
	"strings"
	"syscall"
	"time"

	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/responseobserver"
	extprocv3 "github.com/envoyproxy/go-control-plane/envoy/service/ext_proc/v3"
	"google.golang.org/grpc"
)

const (
	responseObserverMaxRecvMessageBytes = (1 << 20) + (64 << 10)
	responseObserverMaxSendMessageBytes = 64 << 10
)

// newResponseObserverGRPCServer keeps the gRPC ingress bound aligned with the
// bounded one-MiB response body accepted by the observer. The additional
// 64-KiB headroom covers the protobuf envelope and bounded metadata without
// turning the private UDS endpoint into an unbounded input path.
func newResponseObserverGRPCServer(service extprocv3.ExternalProcessorServer) *grpc.Server {
	server := grpc.NewServer(
		grpc.MaxRecvMsgSize(responseObserverMaxRecvMessageBytes),
		grpc.MaxSendMsgSize(responseObserverMaxSendMessageBytes),
	)
	extprocv3.RegisterExternalProcessorServer(server, service)
	return server
}

func main() {
	listen := flag.String("listen", "/run/modsecurity/envoy-ext-proc-response-observer.sock", "private Envoy ext_proc UDS (parent must be mode 0700)")
	socket := flag.String("socket", "/run/modsecurity/envoy-ext-authz-companion.sock", "private response companion UDS")
	timeout := flag.Duration("timeout", 200*time.Millisecond, "per-operation UDS deadline")
	flag.Parse()
	service, err := responseobserver.New(responseobserver.Config{SocketPath: *socket, Timeout: *timeout})
	if err != nil {
		fmt.Fprintf(os.Stderr, "response observer: %v\n", err)
		os.Exit(2)
	}
	listener, err := secureListener(*listen)
	if err != nil {
		fmt.Fprintf(os.Stderr, "response observer listen: %v\n", err)
		os.Exit(1)
	}
	defer listener.Close()
	listener = &peerCredListener{Listener: listener, uid: os.Geteuid(), gid: os.Getegid()}
	server := newResponseObserverGRPCServer(service)
	go func() { _ = server.Serve(listener) }()
	signals := make(chan os.Signal, 1)
	signal.Notify(signals, syscall.SIGINT, syscall.SIGTERM)
	<-signals
	server.GracefulStop()
}

// peerCredListener enforces the private-process boundary for the UDS.
// Rejected peers are closed and never reach gRPC; this observer offers no TCP
// mode or fallback.
type peerCredListener struct {
	net.Listener
	uid, gid int
}

func (listener *peerCredListener) Accept() (net.Conn, error) {
	for {
		conn, err := listener.Listener.Accept()
		if err != nil {
			return nil, err
		}
		if err := verifyPeerCredentials(conn, listener.uid, listener.gid); err != nil {
			// Keep the local UDS trust boundary observable without disclosing a
			// request, response, or the opaque correlation capability.
			fmt.Fprintf(os.Stderr, "response observer rejected private UDS peer: %v\n", err)
			_ = conn.Close()
			continue
		}
		return conn, nil
	}
}

func secureListener(address string) (net.Listener, error) {
	if runtime.GOOS != "linux" {
		return nil, fmt.Errorf("private UDS listener requires Linux SO_PEERCRED")
	}
	if !filepath.IsAbs(address) || filepath.Clean(address) != address || strings.Contains(filepath.ToSlash(address), "/../") || strings.HasSuffix(filepath.ToSlash(address), "/..") {
		return nil, fmt.Errorf("private UDS path must be absolute, normalized, and free of '..'")
	}
	info, err := os.Stat(filepath.Dir(address))
	if err != nil {
		return nil, fmt.Errorf("private UDS parent: %w", err)
	}
	if info.Mode().Perm() != 0700 {
		return nil, fmt.Errorf("private UDS parent must be mode 0700")
	}
	if resolved, err := filepath.EvalSymlinks(filepath.Dir(address)); err != nil || resolved != filepath.Dir(address) {
		return nil, fmt.Errorf("private UDS parent must be symlink-free and canonical")
	}
	if stat, ok := info.Sys().(*syscall.Stat_t); !ok || uint32(stat.Uid) != uint32(os.Geteuid()) {
		return nil, fmt.Errorf("private UDS parent must be owned by effective uid")
	}
	if _, err := os.Lstat(address); err == nil {
		return nil, fmt.Errorf("private UDS path already exists")
	} else if !os.IsNotExist(err) {
		return nil, err
	}
	listener, err := net.Listen("unix", address)
	if err != nil {
		return nil, err
	}
	if err := os.Chmod(address, 0600); err != nil {
		listener.Close()
		return nil, err
	}
	st, err := os.Stat(address)
	if err != nil {
		listener.Close()
		return nil, err
	}
	identity, ok := st.Sys().(*syscall.Stat_t)
	if !ok {
		listener.Close()
		return nil, fmt.Errorf("private UDS stat unavailable")
	}
	return &ownedListener{Listener: listener, path: address, dev: identity.Dev, ino: identity.Ino}, nil
}

type ownedListener struct {
	net.Listener
	path     string
	dev, ino uint64
}

func (listener *ownedListener) Close() error {
	err := listener.Listener.Close()
	if st, statErr := os.Stat(listener.path); statErr == nil {
		if identity, ok := st.Sys().(*syscall.Stat_t); ok && identity.Dev == listener.dev && identity.Ino == listener.ino {
			_ = os.Remove(listener.path)
		}
	}
	return err
}
