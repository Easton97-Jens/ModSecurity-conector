//go:build !linux

package responseobserver

import (
	"fmt"
	"net"
)

func verifyResponseCompanionPeer(_ net.Conn, _ int, _ int) error {
	return fmt.Errorf("response observer: Linux SO_PEERCRED is required for response companion authentication")
}
