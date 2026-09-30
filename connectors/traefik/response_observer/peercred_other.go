//go:build !linux

package response_observer

import (
	"fmt"
	"net"
)

func verifyResponseCompanionPeer(_ net.Conn, _ int, _ int) error {
	return fmt.Errorf("modsecurity response observer: Linux SO_PEERCRED is required for response companion authentication")
}
