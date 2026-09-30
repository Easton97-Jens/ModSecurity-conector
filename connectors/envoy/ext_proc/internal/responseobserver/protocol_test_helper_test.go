package responseobserver

import (
	"fmt"
	"net"
	"strings"
	"time"
)

// dial is deliberately test-only. Production callers must use
// dialWithExpectedPeer so a response companion is authenticated before CLAIM.
func dial(path string, timeout time.Duration) (*client, error) {
	if strings.TrimSpace(path) == "" || timeout <= 0 {
		return nil, fmt.Errorf("response observer: socket path and positive timeout are required")
	}
	dialer := net.Dialer{Timeout: timeout}
	conn, err := dialer.Dial("unix", path)
	if err != nil {
		return nil, fmt.Errorf("response observer: dial private socket: %w", err)
	}
	return &client{conn: conn, timeout: timeout}, nil
}
