//go:build !linux

package response_observer

import (
	"errors"
	"net"
)

func verifyResponseCompanionPeer(_ net.Conn, _ int, _ int) error {
	return errors.New("modsecurity response observer: Linux SO_PEERCRED is required for response companion authentication")
}
