//go:build linux

package responseobserver

import (
	"fmt"
	"net"
	"syscall"

	"golang.org/x/sys/unix"
)

// VerifyPeerCredentials rejects a UDS peer whose kernel-supplied Linux UID/GID\n// does not equal the explicitly expected identity.\nfunc VerifyPeerCredentials(conn net.Conn, expectedUID, expectedGID int) error {
	if conn == nil {
		return fmt.Errorf("response observer: missing private socket connection")
	}
	if !validExpectedResponseCompanionPeerID(expectedUID) ||
		!validExpectedResponseCompanionPeerID(expectedGID) {
		return fmt.Errorf("response observer: expected peer UID and GID must be valid Linux IDs")
	}
	syscallConn, ok := conn.(syscall.Conn)
	if !ok {
		return fmt.Errorf("response observer: private socket does not expose credentials")
	}
	rawConn, err := syscallConn.SyscallConn()
	if err != nil {
		return fmt.Errorf("response observer: access private socket descriptor: %w", err)
	}
	var credential *unix.Ucred
	var credentialErr error
	if err := rawConn.Control(func(fd uintptr) {
		credential, credentialErr = unix.GetsockoptUcred(
			int(fd), unix.SOL_SOCKET, unix.SO_PEERCRED,
		)
	}); err != nil {
		return fmt.Errorf("response observer: inspect private socket credentials: %w", err)
	}
	if credentialErr != nil {
		return fmt.Errorf("response observer: read private socket credentials: %w", credentialErr)
	}
	if credential == nil {
		return fmt.Errorf("response observer: missing private socket credentials")
	}
	if credential.Uid != uint32(expectedUID) || credential.Gid != uint32(expectedGID) {
		return fmt.Errorf("response observer: private socket peer identity mismatch")
	}
	return nil
}
