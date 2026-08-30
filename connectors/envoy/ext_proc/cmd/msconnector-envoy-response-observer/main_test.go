package main

import (
	"context"
	"errors"
	"net"
	"os"
	"path/filepath"
	"sync"
	"syscall"
	"testing"
	"time"

	extprocv3 "github.com/envoyproxy/go-control-plane/envoy/service/ext_proc/v3"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/test/bufconn"
	"google.golang.org/protobuf/proto"
)

type failingResponseObserverListener struct{}

func (failingResponseObserverListener) Accept() (net.Conn, error) {
	return nil, errors.New("listener failed")
}
func (failingResponseObserverListener) Close() error   { return nil }
func (failingResponseObserverListener) Addr() net.Addr { return responseObserverTestAddr("failed") }

type responseObserverTestAddr string

func (a responseObserverTestAddr) Network() string { return "test" }
func (a responseObserverTestAddr) String() string  { return string(a) }

type replacingResponseObserverListener struct {
	path string
}

func (listener replacingResponseObserverListener) Accept() (net.Conn, error) {
	return nil, errors.New("not implemented")
}
func (listener replacingResponseObserverListener) Close() error {
	if err := os.Remove(listener.path); err != nil {
		return err
	}
	return os.WriteFile(listener.path, []byte("replacement"), 0600)
}
func (listener replacingResponseObserverListener) Addr() net.Addr {
	return responseObserverTestAddr("replacement")
}

type gatedResponseObserverListener struct {
	connection net.Conn
	accepted   chan struct{}
	release    chan struct{}
	closeOnce  sync.Once
}

func (listener *gatedResponseObserverListener) Accept() (net.Conn, error) {
	close(listener.accepted)
	<-listener.release
	return listener.connection, nil
}

func (listener *gatedResponseObserverListener) Close() error {
	listener.closeOnce.Do(func() { close(listener.release) })
	return nil
}

func (listener *gatedResponseObserverListener) Addr() net.Addr {
	return responseObserverTestAddr("gated")
}

func TestServeResponseObserverReturnsUnexpectedServeFailure(t *testing.T) {
	err := serveResponseObserver(grpc.NewServer(), failingResponseObserverListener{}, make(chan os.Signal))
	if err == nil || err.Error() != "listener failed" {
		t.Fatalf("serveResponseObserver error = %v, want listener failure", err)
	}
}

func TestForceStopResponseObserverClosesPeerAcceptedAfterShutdownBegins(t *testing.T) {
	serverConnection, clientConnection := net.Pipe()
	defer clientConnection.Close()
	baseListener := &gatedResponseObserverListener{
		connection: serverConnection,
		accepted:   make(chan struct{}),
		release:    make(chan struct{}),
	}
	listener := newTrackedResponseObserverListener(baseListener)
	accepted := make(chan error, 1)
	go func() {
		_, err := listener.Accept()
		accepted <- err
	}()
	select {
	case <-baseListener.accepted:
	case <-time.After(time.Second):
		t.Fatal("underlying listener did not accept the peer")
	}
	if err := clientConnection.SetReadDeadline(time.Now().Add(time.Second)); err != nil {
		t.Fatal(err)
	}

	stopped := make(chan struct{})
	go func() {
		forceStopResponseObserver(grpc.NewServer(), listener)
		close(stopped)
	}()
	select {
	case err := <-accepted:
		if !errors.Is(err, net.ErrClosed) {
			t.Fatalf("tracked accept error = %v, want net.ErrClosed", err)
		}
	case <-time.After(time.Second):
		t.Fatal("tracked listener did not reject the late accepted peer")
	}
	if _, err := clientConnection.Read(make([]byte, 1)); err == nil {
		t.Fatal("late accepted peer remained open after forced stop")
	} else if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
		t.Fatalf("late accepted peer was not closed: %v", err)
	}
	select {
	case <-stopped:
	case <-time.After(time.Second):
		t.Fatal("force stop did not finish")
	}
}

func TestOwnedListenerDoesNotRemoveReplacedSocket(t *testing.T) {
	path := filepath.Join(t.TempDir(), "observer.sock")
	if err := os.WriteFile(path, []byte("owned"), 0600); err != nil {
		t.Fatal(err)
	}
	info, err := os.Stat(path)
	if err != nil {
		t.Fatal(err)
	}
	identity := info.Sys().(*syscall.Stat_t)
	listener := &ownedListener{
		Listener: replacingResponseObserverListener{path: path},
		path:     path,
		dev:      identity.Dev,
		ino:      identity.Ino,
	}
	if err := listener.Close(); err != nil {
		t.Fatal(err)
	}
	contents, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	if string(contents) != "replacement" {
		t.Fatalf("replacement socket contents = %q", contents)
	}
}

func TestOwnedListenerRemovesItsOwnSocketPath(t *testing.T) {
	dir := testSocketDir(t)
	if err := os.Chmod(dir, 0700); err != nil {
		t.Fatal(err)
	}
	path := filepath.Join(dir, "observer.sock")
	base, err := net.Listen("unix", path)
	if err != nil {
		t.Fatal(err)
	}
	unixListener, ok := base.(*net.UnixListener)
	if !ok {
		t.Fatalf("listener type = %T, want *net.UnixListener", base)
	}
	unixListener.SetUnlinkOnClose(false)
	info, err := os.Stat(path)
	if err != nil {
		t.Fatal(err)
	}
	identity := info.Sys().(*syscall.Stat_t)
	listener := &ownedListener{
		Listener: base,
		path:     path,
		dev:      identity.Dev,
		ino:      identity.Ino,
	}
	if err := listener.Close(); err != nil {
		t.Fatal(err)
	}
	if _, err := os.Lstat(path); !os.IsNotExist(err) {
		t.Fatalf("owned socket path remains after close: %v", err)
	}
}

type blockingResponseObserverProbe struct {
	extprocv3.UnimplementedExternalProcessorServer
	started  chan struct{}
	release  chan struct{}
	finished chan struct{}
}

func (probe *blockingResponseObserverProbe) Process(stream extprocv3.ExternalProcessor_ProcessServer) error {
	if _, err := stream.Recv(); err != nil {
		return err
	}
	close(probe.started)
	defer close(probe.finished)
	<-probe.release
	return nil
}

func TestServeResponseObserverForcesStopAfterGracefulStopDeadline(t *testing.T) {
	previousTimeout := responseObserverGracefulStopTimeout
	responseObserverGracefulStopTimeout = 10 * time.Millisecond
	defer func() { responseObserverGracefulStopTimeout = previousTimeout }()

	baseListener := bufconn.Listen(1024 * 1024)
	listener := newTrackedResponseObserverListener(baseListener)
	probe := &blockingResponseObserverProbe{
		started: make(chan struct{}), release: make(chan struct{}), finished: make(chan struct{}),
	}
	server := newResponseObserverGRPCServer(probe)
	signals := make(chan os.Signal, 1)
	result := make(chan error, 1)
	go func() { result <- serveResponseObserver(server, listener, signals) }()

	contextValue, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	connection, err := grpc.DialContext(
		contextValue,
		"bufnet",
		grpc.WithContextDialer(func(context.Context, string) (net.Conn, error) { return baseListener.Dial() }),
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		t.Fatal(err)
	}
	defer connection.Close()
	stream, err := extprocv3.NewExternalProcessorClient(connection).Process(contextValue)
	if err != nil {
		t.Fatal(err)
	}
	if err := stream.Send(&extprocv3.ProcessingRequest{}); err != nil {
		t.Fatal(err)
	}
	select {
	case <-probe.started:
	case <-contextValue.Done():
		t.Fatal("blocking stream did not start")
	}
	signals <- syscall.SIGTERM
	select {
	case err := <-result:
		if !errors.Is(err, errResponseObserverGracefulStopTimedOut) {
			t.Fatalf("serveResponseObserver error = %v, want graceful-stop timeout", err)
		}
	case <-time.After(time.Second):
		t.Fatal("serveResponseObserver did not force-stop the stalled stream")
	}
	close(probe.release)
	select {
	case <-probe.finished:
	case <-time.After(time.Second):
		t.Fatal("stalled stream did not finish after forced stop")
	}
}

func TestServeResponseObserverStopsPreHandshakePeerAfterGracefulStopDeadline(t *testing.T) {
	previousTimeout := responseObserverGracefulStopTimeout
	responseObserverGracefulStopTimeout = 10 * time.Millisecond
	defer func() { responseObserverGracefulStopTimeout = previousTimeout }()

	dir := testSocketDir(t)
	if err := os.Chmod(dir, 0700); err != nil {
		t.Fatal(err)
	}
	base, err := secureListener(filepath.Join(dir, "observer.sock"))
	if err != nil {
		t.Fatal(err)
	}
	defer base.Close()
	tracked := newTrackedResponseObserverListener(base)
	tracked.accepted = make(chan struct{})
	listener := &peerCredListener{Listener: tracked, uid: os.Geteuid(), gid: os.Getegid()}
	server := newResponseObserverGRPCServer(&blockingResponseObserverProbe{})
	signals := make(chan os.Signal, 1)
	result := make(chan error, 1)
	go func() { result <- serveResponseObserver(server, listener, signals) }()

	connection, err := net.Dial("unix", filepath.Join(dir, "observer.sock"))
	if err != nil {
		t.Fatal(err)
	}
	defer connection.Close()
	select {
	case <-tracked.accepted:
	case <-time.After(time.Second):
		t.Fatal("pre-handshake peer was not accepted")
	}
	signals <- syscall.SIGTERM
	select {
	case err := <-result:
		if err != nil && !errors.Is(err, errResponseObserverGracefulStopTimedOut) {
			t.Fatalf("serveResponseObserver error = %v, want nil or graceful-stop timeout", err)
		}
	case <-time.After(time.Second):
		t.Fatal("serveResponseObserver exceeded its shutdown bound for a pre-handshake peer")
	}
	if err := connection.SetReadDeadline(time.Now().Add(time.Second)); err != nil {
		t.Fatal(err)
	}
	for {
		_, err := connection.Read(make([]byte, 1024))
		if err == nil {
			continue
		}
		if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
			t.Fatalf("pre-handshake peer was not closed: %v", err)
		}
		break
	}
}

type responseObserverReceiveProbe struct {
	extprocv3.UnimplementedExternalProcessorServer
	received chan int
}

func (probe *responseObserverReceiveProbe) Process(stream extprocv3.ExternalProcessor_ProcessServer) error {
	request, err := stream.Recv()
	if err != nil {
		return err
	}
	probe.received <- len(request.GetResponseBody().GetBody())
	return stream.Send(&extprocv3.ProcessingResponse{
		Response: &extprocv3.ProcessingResponse_ResponseBody{
			ResponseBody: &extprocv3.BodyResponse{
				Response: &extprocv3.CommonResponse{Status: extprocv3.CommonResponse_CONTINUE},
			},
		},
	})
}

func TestResponseObserverGRPCReceiveLimitAdmitsBoundedResponseBody(t *testing.T) {
	body := make([]byte, 1<<20)
	request := &extprocv3.ProcessingRequest{
		Request: &extprocv3.ProcessingRequest_ResponseBody{
			ResponseBody: &extprocv3.HttpBody{Body: body, EndOfStream: true},
		},
	}
	if size := proto.Size(request); size > responseObserverMaxRecvMessageBytes {
		t.Fatalf("bounded response body serializes to %d bytes, receive bound is only %d", size, responseObserverMaxRecvMessageBytes)
	}

	listener := bufconn.Listen(responseObserverMaxRecvMessageBytes + 1024)
	probe := &responseObserverReceiveProbe{received: make(chan int, 1)}
	server := newResponseObserverGRPCServer(probe)
	defer server.Stop()
	go func() { _ = server.Serve(listener) }()
	defer listener.Close()

	contextValue, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	connection, err := grpc.DialContext(
		contextValue,
		"bufnet",
		grpc.WithContextDialer(func(context.Context, string) (net.Conn, error) {
			return listener.Dial()
		}),
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		t.Fatalf("dial response observer: %v", err)
	}
	defer connection.Close()

	stream, err := extprocv3.NewExternalProcessorClient(connection).Process(contextValue)
	if err != nil {
		t.Fatalf("open response observer stream: %v", err)
	}
	if err := stream.Send(request); err != nil {
		t.Fatalf("send bounded response body: %v", err)
	}
	if _, err := stream.Recv(); err != nil {
		t.Fatalf("receive response observer acknowledgement: %v", err)
	}
	select {
	case received := <-probe.received:
		if received != len(body) {
			t.Fatalf("response observer received %d bytes, want %d", received, len(body))
		}
	case <-contextValue.Done():
		t.Fatal("response observer did not receive the bounded body")
	}
}
