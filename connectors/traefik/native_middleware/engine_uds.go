package native_middleware

import (
	"context"
	"encoding/binary"
	"errors"
	"io"
	"net"
	"strings"
	"sync"
	"time"
)

const (
	udsProtocolVersion      = byte(1)
	udsFrameHeaderSize      = 12
	udsMaxPayload           = 64 << 10
	udsMaxChunk             = 32 << 10
	udsMaxHeaders           = 128
	udsMaxMethod            = 32
	udsMaxURI               = 4096
	udsMaxHTTPVersion       = 32
	udsMaxHostname          = 255
	udsMaxAddress           = 255
	udsMaxHostRequestID     = 256
	udsMaxHeaderName        = 256
	udsMaxHeaderValue       = 8192
	udsDefaultTimeout       = 5 * time.Second
	udsOpcodeBegin          = byte(1)
	udsOpcodeRequestChunk   = byte(2)
	udsOpcodeRequestEOS     = byte(3)
	udsOpcodeResponseHead   = byte(4)
	udsOpcodeResponseBody   = byte(5)
	udsOpcodeResponseEOS    = byte(6)
	udsOpcodeResponseCommit = byte(7)
	udsOpcodeFinish         = byte(8)
	udsOpcodeDestroy        = byte(9)
	udsOpcodeOutcome        = byte(10)
	udsOpcodeResult         = byte(128)
	udsResultOK             = byte(0)
	udsActionAllow          = byte(0)
	udsActionLogOnly        = byte(1)
	udsActionDeny           = byte(2)
	udsActionRedirect       = byte(3)
	udsOutcomeApplied       = byte(1)
)

var (
	errUDSEngineProtocol = errors.New("modsecurity native middleware: invalid local engine protocol response")
	errUDSEngineRejected = errors.New("modsecurity native middleware: local engine rejected lifecycle operation")
)

// unixSocketEngine keeps the compiled Common/libmodsecurity runtime outside
// the Yaegi interpreter. Open dials once; the returned transaction reuses that
// single Unix-domain-socket connection for its entire ServeHTTP lifecycle.
type unixSocketEngine struct {
	socketPath string
	timeout    time.Duration
}

func newUnixSocketEngine(socketPath string) Engine {
	return &unixSocketEngine{socketPath: socketPath, timeout: udsDefaultTimeout}
}

func (engine *unixSocketEngine) Open(ctx context.Context, metadata Metadata) (Transaction, error) {
	if engine == nil || !safeUnixSocketPath(engine.socketPath) {
		return nil, errUDSEngineProtocol
	}
	dialer := net.Dialer{Timeout: engine.timeout}
	connection, err := dialer.DialContext(ctx, "unix", engine.socketPath)
	if err != nil {
		return nil, err
	}
	return &unixSocketTransaction{
		connection: connection,
		metadata:   metadata,
		timeout:    engine.timeout,
	}, nil
}

type unixSocketTransaction struct {
	mu         sync.Mutex
	connection net.Conn
	metadata   Metadata
	timeout    time.Duration
	begun      bool
	closed     bool
}

type udsResult struct {
	action   byte
	status   int
	redirect string
}

func (transaction *unixSocketTransaction) ProcessHeaders(ctx context.Context, direction Direction, headers []Header, end bool) (Decision, error) {
	transaction.mu.Lock()
	defer transaction.mu.Unlock()
	if direction != DirectionRequest || transaction.closed || transaction.begun {
		return allowDecision(), errUDSEngineProtocol
	}
	payload, err := buildUDSBegin(transaction.metadata, headers)
	if err != nil {
		return allowDecision(), err
	}
	result, err := transaction.exchangeLocked(ctx, udsOpcodeBegin, payload)
	if err != nil {
		return allowDecision(), err
	}
	transaction.begun = true
	decision := result.decision()
	if decision.disruptive() || !end {
		return decision, nil
	}
	result, err = transaction.exchangeLocked(ctx, udsOpcodeRequestEOS, nil)
	if err != nil {
		return allowDecision(), err
	}
	return result.decision(), nil
}

func (transaction *unixSocketTransaction) ProcessResponseHeaders(ctx context.Context, status int, httpVersion string, headers []Header) (Decision, error) {
	transaction.mu.Lock()
	defer transaction.mu.Unlock()
	if transaction.closed || !transaction.begun {
		return allowDecision(), errUDSEngineProtocol
	}
	payload, err := buildUDSResponseHeaders(status, httpVersion, headers)
	if err != nil {
		return allowDecision(), err
	}
	result, err := transaction.exchangeLocked(ctx, udsOpcodeResponseHead, payload)
	if err != nil {
		return allowDecision(), err
	}
	return result.decision(), nil
}

func (transaction *unixSocketTransaction) ProcessBody(ctx context.Context, direction Direction, body []byte, end bool) (Decision, error) {
	transaction.mu.Lock()
	defer transaction.mu.Unlock()
	if transaction.closed || !transaction.begun || len(body) > udsMaxChunk {
		return allowDecision(), errUDSEngineProtocol
	}
	chunkOpcode := udsOpcodeRequestChunk
	eosOpcode := udsOpcodeRequestEOS
	if direction == DirectionResponse {
		chunkOpcode = udsOpcodeResponseBody
		eosOpcode = udsOpcodeResponseEOS
	} else if direction != DirectionRequest {
		return allowDecision(), errUDSEngineProtocol
	}
	if len(body) > 0 {
		if _, err := transaction.exchangeLocked(ctx, chunkOpcode, body); err != nil {
			return allowDecision(), err
		}
	}
	if !end {
		return allowDecision(), nil
	}
	result, err := transaction.exchangeLocked(ctx, eosOpcode, nil)
	if err != nil {
		return allowDecision(), err
	}
	return result.decision(), nil
}

func (transaction *unixSocketTransaction) SetResponseCommit(ctx context.Context, headersSent bool, bodyStarted bool) error {
	transaction.mu.Lock()
	defer transaction.mu.Unlock()
	if transaction.closed || !transaction.begun {
		return errUDSEngineProtocol
	}
	payload := []byte{0, 0}
	if headersSent {
		payload[0] = 1
	}
	if bodyStarted {
		payload[1] = 1
	}
	_, err := transaction.exchangeLocked(ctx, udsOpcodeResponseCommit, payload)
	return err
}

func (transaction *unixSocketTransaction) AcknowledgeApplied(ctx context.Context, decision Decision) error {
	transaction.mu.Lock()
	defer transaction.mu.Unlock()
	if transaction.closed || !transaction.begun {
		return errUDSEngineProtocol
	}
	action := udsActionDeny
	if decision.Action == ActionRedirect {
		action = udsActionRedirect
	}
	status, _ := normalizeDecision(decision)
	payload := []byte{action, udsOutcomeApplied, 0, 0}
	binary.BigEndian.PutUint16(payload[2:], uint16(status))
	_, err := transaction.exchangeLocked(ctx, udsOpcodeOutcome, payload)
	return err
}

func (transaction *unixSocketTransaction) AcknowledgeLateLogOnly(ctx context.Context, visibleStatus int) error {
	transaction.mu.Lock()
	defer transaction.mu.Unlock()
	if transaction.closed || !transaction.begun || visibleStatus < 100 || visibleStatus > 999 {
		return errUDSEngineProtocol
	}
	payload := []byte{udsActionLogOnly, 0, 0, 0}
	binary.BigEndian.PutUint16(payload[2:], uint16(visibleStatus))
	_, err := transaction.exchangeLocked(ctx, udsOpcodeOutcome, payload)
	return err
}

func (transaction *unixSocketTransaction) Close(ctx context.Context, _ Summary) {
	transaction.mu.Lock()
	defer transaction.mu.Unlock()
	if transaction.closed {
		return
	}
	transaction.closed = true
	if transaction.connection == nil {
		return
	}
	if transaction.begun {
		if _, err := transaction.exchangeLocked(ctx, udsOpcodeFinish, nil); err == nil {
			_, _ = transaction.exchangeLocked(ctx, udsOpcodeDestroy, nil)
		}
	}
	_ = transaction.connection.Close()
	transaction.connection = nil
}

func (transaction *unixSocketTransaction) exchangeLocked(ctx context.Context, opcode byte, payload []byte) (udsResult, error) {
	if transaction.connection == nil || len(payload) > udsMaxPayload {
		return udsResult{}, errUDSEngineProtocol
	}
	if err := ctx.Err(); err != nil {
		return udsResult{}, err
	}
	deadline := time.Now().Add(transaction.timeout)
	if contextDeadline, ok := ctx.Deadline(); ok && contextDeadline.Before(deadline) {
		deadline = contextDeadline
	}
	if err := transaction.connection.SetDeadline(deadline); err != nil {
		return udsResult{}, err
	}
	if err := writeUDSFrame(transaction.connection, opcode, payload); err != nil {
		return udsResult{}, err
	}
	responseOpcode, response, err := readUDSFrame(transaction.connection)
	if err != nil {
		return udsResult{}, err
	}
	if responseOpcode != udsOpcodeResult {
		return udsResult{}, errUDSEngineProtocol
	}
	return parseUDSResult(response, opcode)
}

func (result udsResult) decision() Decision {
	switch result.action {
	case udsActionAllow, udsActionLogOnly:
		return allowDecision()
	case udsActionRedirect:
		return Decision{Action: ActionRedirect, Status: result.status, Location: result.redirect}
	default:
		return Decision{Action: ActionDeny, Status: result.status}
	}
}

func writeUDSFrame(writer io.Writer, opcode byte, payload []byte) error {
	if len(payload) > udsMaxPayload {
		return errUDSEngineProtocol
	}
	header := make([]byte, udsFrameHeaderSize)
	copy(header, "MSE1")
	header[4] = udsProtocolVersion
	header[5] = opcode
	binary.BigEndian.PutUint32(header[8:], uint32(len(payload)))
	if err := writeUDSAll(writer, header); err != nil {
		return err
	}
	if len(payload) == 0 {
		return nil
	}
	return writeUDSAll(writer, payload)
}

func writeUDSAll(writer io.Writer, payload []byte) error {
	for len(payload) > 0 {
		count, err := writer.Write(payload)
		if count > 0 {
			payload = payload[count:]
		}
		if err != nil {
			return err
		}
		if count == 0 {
			return io.ErrShortWrite
		}
	}
	return nil
}

func readUDSFrame(reader io.Reader) (byte, []byte, error) {
	header := make([]byte, udsFrameHeaderSize)
	if _, err := io.ReadFull(reader, header); err != nil {
		return 0, nil, err
	}
	if string(header[:4]) != "MSE1" || header[4] != udsProtocolVersion || header[6] != 0 || header[7] != 0 {
		return 0, nil, errUDSEngineProtocol
	}
	length := binary.BigEndian.Uint32(header[8:])
	if length > udsMaxPayload {
		return 0, nil, errUDSEngineProtocol
	}
	payload := make([]byte, int(length))
	if _, err := io.ReadFull(reader, payload); err != nil {
		return 0, nil, err
	}
	return header[5], payload, nil
}

func parseUDSResult(payload []byte, command byte) (udsResult, error) {
	if len(payload) < 14 || payload[0] != command {
		return udsResult{}, errUDSEngineProtocol
	}
	transactionIDSize := int(binary.BigEndian.Uint16(payload[8:10]))
	ruleIDSize := int(binary.BigEndian.Uint16(payload[10:12]))
	redirectSize := int(binary.BigEndian.Uint16(payload[12:14]))
	if 14+transactionIDSize+ruleIDSize+redirectSize != len(payload) {
		return udsResult{}, errUDSEngineProtocol
	}
	if payload[1] != udsResultOK {
		return udsResult{}, errUDSEngineRejected
	}
	if payload[2] > udsActionRedirect {
		// The native middleware has no verified mapping for drop, abort, error,
		// or unsupported engine decisions. Do not relabel one as an HTTP deny.
		return udsResult{}, errUDSEngineRejected
	}
	redirectOffset := 14 + transactionIDSize + ruleIDSize
	return udsResult{
		action:   payload[2],
		status:   int(binary.BigEndian.Uint16(payload[4:6])),
		redirect: string(payload[redirectOffset : redirectOffset+redirectSize]),
	}, nil
}

func buildUDSBegin(metadata Metadata, headers []Header) ([]byte, error) {
	if len(headers) > udsMaxHeaders {
		return nil, errUDSEngineProtocol
	}
	payload := make([]byte, 0, 1024)
	var err error
	if payload, err = appendUDSText(payload, metadata.Method, udsMaxMethod, true); err != nil {
		return nil, err
	}
	if payload, err = appendUDSText(payload, metadata.RequestURI, udsMaxURI, true); err != nil {
		return nil, err
	}
	httpVersion := metadata.HTTPVersion
	if httpVersion == "" {
		httpVersion = "HTTP/1.1"
	}
	if payload, err = appendUDSText(payload, httpVersion, udsMaxHTTPVersion, true); err != nil {
		return nil, err
	}
	if payload, err = appendUDSText(payload, metadata.Hostname, udsMaxHostname, false); err != nil {
		return nil, err
	}
	if payload, err = appendUDSText(payload, metadata.ClientAddress, udsMaxAddress, false); err != nil {
		return nil, err
	}
	payload = appendUDSUint16(payload, uint16(clampPort(metadata.ClientPort)))
	if payload, err = appendUDSText(payload, metadata.ServerAddress, udsMaxAddress, false); err != nil {
		return nil, err
	}
	payload = appendUDSUint16(payload, uint16(clampPort(metadata.ServerPort)))
	if payload, err = appendUDSText(payload, metadata.TransactionID, udsMaxHostRequestID, false); err != nil {
		return nil, err
	}
	payload = appendUDSUint16(payload, uint16(len(headers)))
	for _, header := range headers {
		if payload, err = appendUDSText(payload, header.Name, udsMaxHeaderName, true); err != nil {
			return nil, err
		}
		if payload, err = appendUDSText(payload, header.Value, udsMaxHeaderValue, false); err != nil {
			return nil, err
		}
	}
	if len(payload) > udsMaxPayload {
		return nil, errUDSEngineProtocol
	}
	return payload, nil
}

func buildUDSResponseHeaders(status int, httpVersion string, headers []Header) ([]byte, error) {
	if status < 100 || status > 999 || len(headers) > udsMaxHeaders {
		return nil, errUDSEngineProtocol
	}
	payload := appendUDSUint16(nil, uint16(status))
	if httpVersion == "" {
		httpVersion = "HTTP/1.1"
	}
	var err error
	if payload, err = appendUDSText(payload, httpVersion, udsMaxHTTPVersion, true); err != nil {
		return nil, err
	}
	payload = appendUDSUint16(payload, uint16(len(headers)))
	for _, header := range headers {
		if payload, err = appendUDSText(payload, header.Name, udsMaxHeaderName, true); err != nil {
			return nil, err
		}
		if payload, err = appendUDSText(payload, header.Value, udsMaxHeaderValue, false); err != nil {
			return nil, err
		}
	}
	if len(payload) > udsMaxPayload {
		return nil, errUDSEngineProtocol
	}
	return payload, nil
}

func appendUDSText(payload []byte, value string, maximum int, required bool) ([]byte, error) {
	if (required && value == "") || len(value) > maximum || len(value) > 65535 || strings.IndexByte(value, 0) >= 0 {
		return nil, errUDSEngineProtocol
	}
	payload = appendUDSUint16(payload, uint16(len(value)))
	return append(payload, value...), nil
}

func appendUDSUint16(payload []byte, value uint16) []byte {
	return append(payload, byte(value>>8), byte(value))
}

func clampPort(port int) int {
	if port < 0 {
		return 0
	}
	if port > 65535 {
		return 65535
	}
	return port
}

var (
	_ Engine                    = (*unixSocketEngine)(nil)
	_ Transaction               = (*unixSocketTransaction)(nil)
	_ responseHeaderTransaction = (*unixSocketTransaction)(nil)
	_ responseCommitTransaction = (*unixSocketTransaction)(nil)
	_ outcomeTransaction        = (*unixSocketTransaction)(nil)
)
