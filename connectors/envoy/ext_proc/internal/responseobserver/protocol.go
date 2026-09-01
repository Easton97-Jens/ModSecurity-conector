package responseobserver

import (
	"encoding/binary"
	"fmt"
	"io"
	"net"
	"strings"
	"time"
)

const (
	maxPayload                  = 65536
	maxBody                     = 32768
	maxHeaders                  = 65535
	maxResponseHeaderFieldCount = 256
	maxResponseHeaderNameBytes  = 256
	maxResponseHeaderValueBytes = 8192
	maxResponseHeaderPayload    = maxPayload + 2 + 2 + len("HTTP/1.1") + 2 +
		4*maxResponseHeaderFieldCount
	frameSize = 12
)

const (
	opClaim byte = 1 + iota
	opResponseHeaders
	opResponseBody
	opResponseEOS
	opCommit
	opCancel
	opRelease
	opOutcome
)

const (
	resultOpcode    byte = 128
	protocolVersion byte = 2
)

// Cancellation causes are part of MRC1 protocol version 2. A non-zero value
// is not a synonym for upstream disconnect.
const (
	terminationClientCancel byte = iota
	terminationUpstreamDisconnect
	terminationConnectorError
	terminationProtocolError
	terminationEngineTimeout
	terminationEngineUnavailable
	terminationInvalidEngineResponse
)

const (
	resultOK      byte = 0
	maxResultCode byte = 1
	maxResultText      = 8192
)

// Decision kinds are intentionally numeric and stable across the private UDS
// boundary. They mirror the common contract; no transaction or host identity
// is carried by this protocol.
const (
	decisionAllow byte = iota
	decisionLogOnly
	decisionDeny
	decisionRedirect
	decisionDrop
	decisionConnectionAbort
	decisionError
	decisionUnsupported
)

const (
	actionAllow byte = iota
	actionDeny
	actionRedirect
	actionDrop
	actionLogOnly
	actionAbortConnection
	actionStreamReset
	actionError
	actionUnsupported
	actionRateLimit
)

type result struct {
	requestOpcode byte
	code          byte
	decision      byte
	status        int
	errorCode     int
	redirect      string
	rule          string
}

func validHandle(handle string) bool {
	if len(handle) != 64 || strings.ToLower(handle) != handle {
		return false
	}
	for _, c := range handle {
		if !(c >= '0' && c <= '9' || c >= 'a' && c <= 'f') {
			return false
		}
	}
	return true
}

type client struct {
	conn    net.Conn
	timeout time.Duration
}

func maxPayloadForOpcode(op byte) int {
	if op == opResponseHeaders {
		return maxResponseHeaderPayload
	}
	return maxPayload
}

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

func (c *client) close() error {
	if c == nil || c.conn == nil {
		return nil
	}
	return c.conn.Close()
}

func (c *client) call(op byte, payload []byte) (result, error) {
	if len(payload) > maxPayloadForOpcode(op) {
		return result{}, fmt.Errorf("response observer: payload exceeds %d bytes", maxPayloadForOpcode(op))
	}
	if err := c.conn.SetDeadline(time.Now().Add(c.timeout)); err != nil {
		return result{}, err
	}
	var header [frameSize]byte
	copy(header[:4], []byte("MRC1"))
	header[4] = protocolVersion
	header[5] = op
	binary.BigEndian.PutUint32(header[8:], uint32(len(payload)))
	if err := writeFull(c.conn, header[:]); err != nil {
		return result{}, err
	}
	if len(payload) > 0 {
		if err := writeFull(c.conn, payload); err != nil {
			return result{}, err
		}
	}
	if _, err := io.ReadFull(c.conn, header[:]); err != nil {
		return result{}, err
	}
	if string(header[:4]) != "MRC1" || header[4] != protocolVersion || header[5] != resultOpcode || header[6] != 0 || header[7] != 0 {
		return result{}, fmt.Errorf("response observer: invalid result frame")
	}
	length := binary.BigEndian.Uint32(header[8:])
	if length > maxPayload {
		return result{}, fmt.Errorf("response observer: result exceeds %d bytes", maxPayload)
	}
	data := make([]byte, length)
	if _, err := io.ReadFull(c.conn, data); err != nil {
		return result{}, err
	}
	return parseResult(op, data)
}

func parseResult(op byte, data []byte) (result, error) {
	if !validResultPayload(op, data) {
		return result{}, fmt.Errorf("response observer: short result payload")
	}
	r := result{requestOpcode: data[0], code: data[1], decision: data[2], status: int(binary.BigEndian.Uint16(data[4:])), errorCode: int(binary.BigEndian.Uint16(data[6:]))}
	if r.requestOpcode != op || data[3] != 0 {
		return result{}, fmt.Errorf("response observer: result opcode mismatch")
	}
	redirectLen := int(binary.BigEndian.Uint16(data[8:]))
	r.redirect = string(data[12 : 12+redirectLen])
	r.rule = string(data[12+redirectLen:])
	return r, nil
}

func validResultPayload(op byte, data []byte) bool {
	if len(data) < 12 || data[3] != 0 || data[1] > maxResultCode ||
		data[2] > decisionUnsupported {
		return false
	}
	errorCode := int(binary.BigEndian.Uint16(data[6:]))
	if (data[1] == resultOK && errorCode != 0) ||
		(data[1] != resultOK && errorCode == 0) {
		return false
	}
	status := int(binary.BigEndian.Uint16(data[4:]))
	if data[1] == resultOK && !validSuccessfulResultStatus(op, data[2], status) {
		return false
	}
	redirectLen := int(binary.BigEndian.Uint16(data[8:]))
	ruleLen := int(binary.BigEndian.Uint16(data[10:]))
	if 12+redirectLen+ruleLen != len(data) || redirectLen > maxResultText ||
		ruleLen > maxResultText {
		return false
	}
	if !validResultText(data[12:12+redirectLen]) ||
		!validResultText(data[12+redirectLen:]) {
		return false
	}
	if data[2] == decisionRedirect {
		return status >= 300 && status <= 399 && redirectLen != 0
	}
	return redirectLen == 0
}

func validResultText(data []byte) bool {
	for _, value := range data {
		if value < 32 || value == 127 {
			return false
		}
	}
	return true
}

func validSuccessfulResultStatus(op, decision byte, status int) bool {
	if status >= 100 && status <= 599 {
		return true
	}
	return status == 0 && (decision == decisionAllow ||
		decision == decisionLogOnly || decision == decisionDrop ||
		decision == decisionConnectionAbort ||
		((op == opRelease || op == opCancel) && decision == decisionError))
}

func writeFull(writer io.Writer, data []byte) error {
	for len(data) > 0 {
		n, err := writer.Write(data)
		if err != nil {
			return err
		}
		if n <= 0 || n > len(data) {
			return io.ErrShortWrite
		}
		data = data[n:]
	}
	return nil
}

func u16(value int) ([]byte, error) {
	if value < 0 || value > 65535 {
		return nil, fmt.Errorf("response observer: value exceeds uint16")
	}
	b := make([]byte, 2)
	binary.BigEndian.PutUint16(b, uint16(value))
	return b, nil
}

func appendU16(dst []byte, value int) ([]byte, error) {
	b, err := u16(value)
	if err != nil {
		return nil, err
	}
	return append(dst, b...), nil
}
