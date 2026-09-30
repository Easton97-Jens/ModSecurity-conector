//go:build !linux

package response_observer

import "testing"

func TestResponseCompanionPeerVerificationFailsClosedWithoutLinuxSOPEERCRED(t *testing.T) {
	if err := verifyResponseCompanionPeer(nil, 0, 0); err == nil {
		t.Fatal("unsupported platform accepted response companion authentication")
	}
}
