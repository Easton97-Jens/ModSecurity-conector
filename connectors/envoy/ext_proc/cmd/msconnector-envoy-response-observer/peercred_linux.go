//go:build linux

package main

import (
	"fmt"
	"net"

	"golang.org/x/sys/unix"
)

func verifyPeerCredentials(conn net.Conn, expectedUID, expectedGID int) error {
	sysconn, ok := conn.(syscallConnProvider)
	if !ok {
		return fmt.Errorf("private UDS connection has no syscall control")
	}
	raw, err := sysconn.SyscallConn()
	if err != nil {
		return err
	}
	var checkErr error
	if err := raw.Control(func(fd uintptr) {
		cred, err := unix.GetsockoptUcred(int(fd), unix.SOL_SOCKET, unix.SO_PEERCRED)
		if err != nil {
			checkErr = err
			return
		}
		if int(cred.Uid) != expectedUID || int(cred.Gid) != expectedGID {
			checkErr = fmt.Errorf("peer credentials uid=%d gid=%d, expected uid=%d gid=%d", cred.Uid, cred.Gid, expectedUID, expectedGID)
		}
	}); err != nil {
		return err
	}
	return checkErr
}
