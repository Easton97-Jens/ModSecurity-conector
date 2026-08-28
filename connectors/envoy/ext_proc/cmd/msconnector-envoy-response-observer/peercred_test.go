package main

import (
	"net"
	"os"
	"path/filepath"
	"testing"
)

func testSocketDir(t *testing.T) string {
	t.Helper()
	dir, err := os.MkdirTemp("", "mso-")
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { _ = os.RemoveAll(dir) })
	return dir
}

func TestPrivateUDSAcceptsExpectedPeerCredentials(t *testing.T) {
	dir := testSocketDir(t)
	if err := os.Chmod(dir, 0700); err != nil {
		t.Fatal(err)
	}
	path := filepath.Join(dir, "observer.sock")
	listener, err := secureListener(path)
	if err != nil {
		t.Fatal(err)
	}
	defer listener.Close()
	checked := &peerCredListener{Listener: listener, uid: os.Geteuid(), gid: os.Getegid()}
	accepted := make(chan error, 1)
	go func() {
		conn, err := checked.Accept()
		if err != nil {
			accepted <- err
			return
		}
		accepted <- conn.Close()
	}()
	conn, err := net.Dial("unix", path)
	if err != nil {
		t.Fatal(err)
	}
	_ = conn.Close()
	if err := <-accepted; err != nil {
		t.Fatal(err)
	}
}

func TestPrivateUDSRejectsNonCanonicalAndSymlinkPaths(t *testing.T) {
	if _, err := secureListener("/tmp/../tmp/observer.sock"); err == nil {
		t.Fatal("accepted path containing ..")
	}
	dir := testSocketDir(t)
	if err := os.Chmod(dir, 0700); err != nil {
		t.Fatal(err)
	}
	link := dir + "-target"
	if err := os.Symlink(dir, link); err != nil {
		t.Fatal(err)
	}
	defer os.Remove(link)
	if _, err := secureListener(filepath.Join(link, "observer.sock")); err == nil {
		t.Fatal("accepted symlinked UDS parent")
	}
}
