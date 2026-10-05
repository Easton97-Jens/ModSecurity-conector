//go:build linux
// +build linux

package response_observer

import (
	"errors"
	"fmt"
	"net"
	"syscall"
)

type responseCompanionIdentity struct {
	uid uint32
	gid uint32
}

func verifyResponseCompanionPeer(conn net.Conn, wantUID, wantGID int) error {
	if conn == nil {
		return errors.New("modsecurity response observer: missing private socket connection")
	}
	maximumLinuxID := uint64(^uint32(0))
	if wantUID < 0 || wantGID < 0 || uint64(wantUID) > maximumLinuxID ||
		uint64(wantGID) > maximumLinuxID {
		return errors.New("modsecurity response observer: expected peer UID and GID must be valid Linux IDs")
	}
	actual, err := readResponseCompanionIdentity(conn)
	if err != nil {
		return err
	}
	if actual.uid == uint32(wantUID) && actual.gid == uint32(wantGID) {
		return nil
	}
	return errors.New("modsecurity response observer: private socket peer identity mismatch")
}

func readResponseCompanionIdentity(conn net.Conn) (responseCompanionIdentity, error) {
	unixConn, ok := conn.(*net.UnixConn)
	if !ok {
		return responseCompanionIdentity{}, errors.New("modsecurity response observer: private socket does not expose credentials")
	}
	raw, err := unixConn.SyscallConn()
	if err != nil {
		return responseCompanionIdentity{}, fmt.Errorf("modsecurity response observer: access private socket descriptor: %w", err)
	}
	var identity responseCompanionIdentity
	var readErr error
	if controlErr := raw.Control(func(fd uintptr) {
		credential, socketErr := syscall.GetsockoptUcred(int(fd), syscall.SOL_SOCKET, syscall.SO_PEERCRED)
		if socketErr != nil {
			readErr = socketErr
			return
		}
		if credential == nil {
			readErr = errors.New("missing private socket credentials")
			return
		}
		identity.uid = credential.Uid
		identity.gid = credential.Gid
	}); controlErr != nil {
		return responseCompanionIdentity{}, fmt.Errorf("modsecurity response observer: inspect private socket credentials: %w", controlErr)
	}
	if readErr != nil {
		return responseCompanionIdentity{}, fmt.Errorf("modsecurity response observer: read private socket credentials: %w", readErr)
	}
	return identity, nil
}
