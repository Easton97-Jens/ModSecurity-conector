package main

import (
	"errors"
	"flag"
	"fmt"
	"net"
	"os"
	"os/signal"
	"path/filepath"
	"runtime"
	"strings"
	"sync"
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

var (
	responseObserverGracefulStopTimeout     = 5 * time.Second
	errResponseObserverGracefulStopTimedOut = errors.New("response observer graceful shutdown timed out")
)

type syscallConnProvider interface {
	SyscallConn() (syscall.RawConn, error)
}

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
	listener = newTrackedResponseObserverListener(listener)
	listener = &peerCredListener{Listener: listener, uid: os.Geteuid(), gid: os.Getegid()}
	server := newResponseObserverGRPCServer(service)
	signals := make(chan os.Signal, 1)
	signal.Notify(signals, syscall.SIGINT, syscall.SIGTERM)
	defer signal.Stop(signals)
	if err := serveResponseObserver(server, listener, signals); err != nil {
		fmt.Fprintf(os.Stderr, "response observer serve: %v\n", err)
		_ = listener.Close()
		os.Exit(1)
	}
}

func serveResponseObserver(server *grpc.Server, listener net.Listener, signals <-chan os.Signal) error {
	serveErr := make(chan error, 1)
	go func() { serveErr <- server.Serve(listener) }()

	select {
	case err := <-serveErr:
		if err != nil && !errors.Is(err, grpc.ErrServerStopped) {
			go forceStopResponseObserver(server, listener)
			return err
		}
		return nil
	case <-signals:
		stopped := make(chan struct{})
		go func() {
			server.GracefulStop()
			close(stopped)
		}()
		timer := time.NewTimer(responseObserverGracefulStopTimeout)
		defer timer.Stop()
		select {
		case <-stopped:
			closeActiveResponseObserverConnections(listener)
			return nil
		case <-timer.C:
			// The binary exits through main after this terminal error. Keep the
			// force-stop work in flight so that a non-cooperative stream cannot
			// extend the configured graceful-stop deadline.
			go forceStopResponseObserver(server, listener)
			return errResponseObserverGracefulStopTimedOut
		}
	}
}

// forceStopResponseObserver marks the connection tracker closed before
// stopping accepts, then closes every tracked peer before stopping gRPC. This
// keeps a pre-handshake peer from holding the gRPC Serve wait group past the
// configured graceful-stop deadline.
func forceStopResponseObserver(server *grpc.Server, listener net.Listener) {
	closeActiveResponseObserverConnections(listener)
	_ = listener.Close()
	server.Stop()
}

func closeActiveResponseObserverConnections(listener net.Listener) {
	if closer, ok := listener.(responseObserverConnectionCloser); ok {
		closer.closeActiveConnections()
	}
}

type responseObserverConnectionCloser interface {
	closeActiveConnections()
}

type trackedResponseObserverListener struct {
	net.Listener
	mu          sync.Mutex
	connections map[*trackedResponseObserverConn]struct{}
	closing     bool
	accepted    chan struct{}
	acceptOnce  sync.Once
}

func newTrackedResponseObserverListener(listener net.Listener) *trackedResponseObserverListener {
	return &trackedResponseObserverListener{
		Listener:    listener,
		connections: make(map[*trackedResponseObserverConn]struct{}),
	}
}

func (listener *trackedResponseObserverListener) Accept() (net.Conn, error) {
	conn, err := listener.Listener.Accept()
	if err != nil {
		return nil, err
	}
	tracked := &trackedResponseObserverConn{Conn: conn, listener: listener}
	listener.mu.Lock()
	if listener.closing {
		listener.mu.Unlock()
		_ = conn.Close()
		return nil, net.ErrClosed
	}
	listener.connections[tracked] = struct{}{}
	listener.mu.Unlock()
	if listener.accepted != nil {
		listener.acceptOnce.Do(func() { close(listener.accepted) })
	}
	return tracked, nil
}

func (listener *trackedResponseObserverListener) closeActiveConnections() {
	listener.mu.Lock()
	listener.closing = true
	connections := make([]*trackedResponseObserverConn, 0, len(listener.connections))
	for connection := range listener.connections {
		connections = append(connections, connection)
	}
	listener.mu.Unlock()
	for _, connection := range connections {
		_ = connection.Close()
	}
}

func (listener *trackedResponseObserverListener) removeConnection(connection *trackedResponseObserverConn) {
	listener.mu.Lock()
	delete(listener.connections, connection)
	listener.mu.Unlock()
}

type trackedResponseObserverConn struct {
	net.Conn
	listener  *trackedResponseObserverListener
	closeOnce sync.Once
}

func (conn *trackedResponseObserverConn) Close() error {
	err := conn.Conn.Close()
	conn.closeOnce.Do(func() { conn.listener.removeConnection(conn) })
	return err
}

func (conn *trackedResponseObserverConn) SyscallConn() (syscall.RawConn, error) {
	provider, ok := conn.Conn.(syscallConnProvider)
	if !ok {
		return nil, fmt.Errorf("private UDS connection has no syscall control")
	}
	return provider.SyscallConn()
}

// peerCredListener enforces the private-process boundary for the UDS.
// Rejected peers are closed and never reach gRPC; this observer offers no TCP
// mode or fallback.
type peerCredListener struct {
	net.Listener
	uid, gid int
}

func (listener *peerCredListener) closeActiveConnections() {
	if closer, ok := listener.Listener.(responseObserverConnectionCloser); ok {
		closer.closeActiveConnections()
	}
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
	unixListener, ok := listener.(*net.UnixListener)
	if !ok {
		_ = listener.Close()
		return nil, fmt.Errorf("private UDS listener is not a Unix listener")
	}
	// Disable Go's pathname cleanup before every fallible ownership check.  A
	// same-identity replacement must never be removed by an error-path Close.
	unixListener.SetUnlinkOnClose(false)
	st, err := os.Stat(address)
	if err != nil {
		_ = listener.Close()
		return nil, err
	}
	identity, ok := st.Sys().(*syscall.Stat_t)
	if !ok {
		_ = listener.Close()
		return nil, fmt.Errorf("private UDS stat unavailable")
	}
	owned := &ownedListener{Listener: listener, path: address, dev: identity.Dev, ino: identity.Ino}
	if err := os.Chmod(address, 0600); err != nil {
		_ = owned.Close()
		return nil, err
	}
	return owned, nil
}

type ownedListener struct {
	net.Listener
	path     string
	dev, ino uint64
}

func (listener *ownedListener) Close() error {
	owned := false
	if st, statErr := os.Stat(listener.path); statErr == nil {
		if identity, ok := st.Sys().(*syscall.Stat_t); ok && identity.Dev == listener.dev && identity.Ino == listener.ino {
			owned = true
		}
	}
	err := listener.Listener.Close()
	if owned {
		if st, statErr := os.Stat(listener.path); statErr == nil {
			if identity, ok := st.Sys().(*syscall.Stat_t); ok && identity.Dev == listener.dev && identity.Ino == listener.ino {
				_ = os.Remove(listener.path)
			}
		}
	}
	return err
}
