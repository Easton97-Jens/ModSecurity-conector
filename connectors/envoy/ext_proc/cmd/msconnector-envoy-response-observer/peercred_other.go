//go:build !linux

package main

import (
	"fmt"
	"net"
)

func verifyPeerCredentials(net.Conn, int, int) error {
	return fmt.Errorf("private UDS peer credentials are unsupported on this platform")
}
