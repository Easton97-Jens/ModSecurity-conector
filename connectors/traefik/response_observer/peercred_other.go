//go:build !linux

package response_observer

import "net"

func verifyResponseCompanionPeer(_ net.Conn, _ int, _ int) error {
	return errUnsupportedResponseCompanionPeer
}
