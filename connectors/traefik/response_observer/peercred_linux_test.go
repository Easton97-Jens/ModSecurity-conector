//go:build linux

package response_observer

import (
	"context"
	"net"
	"os"
	"path/filepath"
	"testing"
	"time"
)

func traefikPeerTestID(value int) *int {
	return &value
}

func TestOpenSessionRejectsPeerMismatchBeforeClaim(t *testing.T) {
	path := filepath.Join(t.TempDir(), "companion.sock")
	listener, err := net.Listen("unix", path)
	if err != nil {
		t.Fatal(err)
	}
	defer listener.Close()

	readCount := make(chan int, 1)
	go func() {
		conn, acceptErr := listener.Accept()
		if acceptErr != nil {
			readCount <- -1
			return
		}
		defer conn.Close()
		_ = conn.SetReadDeadline(time.Now().Add(2 * time.Second))
		buffer := make([]byte, 1)
		n, _ := conn.Read(buffer)
		readCount <- n
	}()

	mismatchedUID := os.Geteuid() ^ 1
	_, err = openSession(context.Background(), Config{
		SocketPath:      path,
		TimeoutMillis:   1000,
		ExpectedPeerUID: traefikPeerTestID(mismatchedUID),
		ExpectedPeerGID: traefikPeerTestID(os.Getegid()),
	}, testHandle)
	if err == nil {
		t.Fatal("openSession accepted a mismatched companion UID")
	}
	if got := <-readCount; got != 0 {
		t.Fatalf("companion received %d bytes before peer rejection, want 0", got)
	}
}

func TestNormalizeConfigResolvesExpectedPeerIdentity(t *testing.T) {
	config, err := normalizeConfig(&Config{})
	if err != nil {
		t.Fatal(err)
	}
	if config.ExpectedPeerUID == nil || config.ExpectedPeerGID == nil ||
		*config.ExpectedPeerUID != os.Geteuid() || *config.ExpectedPeerGID != os.Getegid() {
		t.Fatalf("default expected peer identity = %#v:%#v", config.ExpectedPeerUID, config.ExpectedPeerGID)
	}
	uid, gid := os.Geteuid(), os.Getegid()
	config, err = normalizeConfig(&Config{
		ExpectedPeerUID: traefikPeerTestID(uid),
		ExpectedPeerGID: traefikPeerTestID(gid),
	})
	if err != nil || *config.ExpectedPeerUID != uid || *config.ExpectedPeerGID != gid {
		t.Fatalf("explicit expected peer identity = %#v, %v", config, err)
	}
	if _, err := normalizeConfig(&Config{ExpectedPeerUID: traefikPeerTestID(uid)}); err == nil {
		t.Fatal("accepted incomplete expected peer identity")
	}
}
