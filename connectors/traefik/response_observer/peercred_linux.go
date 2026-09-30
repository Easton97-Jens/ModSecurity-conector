//go:build linux

package response_observer

import (
	"fmt"
	"net"
	"syscall"
)

func verifyResponseCompanionPeer(conn net.Conn, expectedUID, expectedGID int) error {
	if conn == nil {
		return fmt.Errorf("modsecurity response observer: missing private socket connection")
	}
	if !validExpectedResponseCompanionPeerID(expectedUID) ||
		!validExpectedResponseCompanionPeerID(expectedGID) {
		return fmt.Errorf("modsecurity response observer: expected peer UID and GID must be valid Linux IDs")
	}
	syscallConn, ok := conn.(syscall.Conn)
	if !ok {
		return fmt.Errorf("modsecurity response observer: private socket does not expose credentials")
	}
	rawConn, err := syscallConn.SyscallConn()
	if err != nil {
		return fmt.Errorf("modsecurity response observer: access private socket descriptor: %w", err)
	}
	var credential *syscall.Ucred
	var credentialErr error
	if err := rawConn.Control(func(fd uintptr) {
		credential, credentialErr = syscall.GetsockoptUcred(
			int(fd), syscall.SOL_SOCKET, syscall.SO_PEERCRED,
		)
	}); err != nil {
		return fmt.Errorf("modsecurity response observer: inspect private socket credentials: %w", err)
	}
	if credentialErr != nil {
		return fmt.Errorf("modsecurity response observer: read private socket credentials: %w", credentialErr)
	}
	if credential == nil {
		return fmt.Errorf("modsecurity response observer: missing private socket credentials")
	}
	if credential.Uid != uint32(expectedUID) || credential.Gid != uint32(expectedGID) {
		return fmt.Errorf("modsecurity response observer: private socket peer identity mismatch")
	}
	return nil
}
