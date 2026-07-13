//go:build libmodsecurity

package processor

/*
#include <stdlib.h>
#include "common_runtime_bridge.h"
*/
import "C"

import (
	"context"
	"fmt"
	"strconv"
	"strings"
	"sync"
	"unsafe"
)

const commonRuntimeErrorBufferSize = 512

// CommonRuntimeEngine is the Envoy-specific, CGo-backed adapter for the
// checked-in Common Runtime. It holds one libmodsecurity engine and opens one
// native Common transaction for each ext_proc Process stream. All native calls
// are serialized because Common Runtime's event/transaction bookkeeping is
// not documented as concurrent-safe.
type CommonRuntimeEngine struct {
	mu           sync.Mutex
	runtime      *C.msc_envoy_ext_proc_runtime
	closed       bool
	transactions map[*commonRuntimeTransaction]struct{}
}

// NewCommonRuntimeEngine creates a real Common/libmodsecurity runtime from a
// connector-local runtime configuration. The C ABI rejects non-streaming body
// modes so this bridge cannot silently degrade into a buffering path.
func NewCommonRuntimeEngine(configPath string) (*CommonRuntimeEngine, error) {
	if strings.TrimSpace(configPath) == "" {
		return nil, fmt.Errorf("Common runtime config path is required")
	}
	cConfigPath := C.CString(configPath)
	defer C.free(unsafe.Pointer(cConfigPath))
	var runtime *C.msc_envoy_ext_proc_runtime
	var nativeError [commonRuntimeErrorBufferSize]C.char
	if C.msc_envoy_ext_proc_runtime_create(cConfigPath, &runtime, &nativeError[0], C.size_t(len(nativeError))) == 0 {
		return nil, fmt.Errorf("create Common runtime: %s", nativeErrorText(nativeError[:]))
	}
	if runtime == nil {
		return nil, fmt.Errorf("create Common runtime returned no runtime")
	}
	return &CommonRuntimeEngine{
		runtime:      runtime,
		transactions: make(map[*commonRuntimeTransaction]struct{}),
	}, nil
}

// Close releases the libmodsecurity engine after every stream transaction has
// completed. It refuses to invalidate active native transactions; the gRPC
// server's graceful stop naturally satisfies this contract before main calls
// Close.
func (engine *CommonRuntimeEngine) Close() error {
	if engine == nil {
		return nil
	}
	engine.mu.Lock()
	defer engine.mu.Unlock()
	if engine.closed {
		return nil
	}
	if len(engine.transactions) != 0 {
		return fmt.Errorf("cannot close Common runtime with %d active transactions", len(engine.transactions))
	}
	C.msc_envoy_ext_proc_runtime_destroy(&engine.runtime)
	engine.closed = true
	return nil
}

func (engine *CommonRuntimeEngine) Open(ctx context.Context, metadata StreamMetadata) (Transaction, error) {
	if err := ctx.Err(); err != nil {
		return nil, err
	}
	if engine == nil {
		return nil, fmt.Errorf("Common runtime engine is nil")
	}
	engine.mu.Lock()
	defer engine.mu.Unlock()
	if engine.closed || engine.runtime == nil {
		return nil, fmt.Errorf("Common runtime engine is closed")
	}
	transaction := &commonRuntimeTransaction{engine: engine, metadata: metadata}
	engine.transactions[transaction] = struct{}{}
	return transaction, nil
}

type commonRuntimeTransaction struct {
	engine   *CommonRuntimeEngine
	metadata StreamMetadata
	native   *C.msc_envoy_ext_proc_transaction
	begun    bool
	closed   bool

	transactionID string
}

func (transaction *commonRuntimeTransaction) ProcessHeaders(ctx context.Context, direction Direction, headers []Header, endOfStream bool) (Decision, error) {
	if err := ctx.Err(); err != nil {
		return Decision{}, err
	}
	if transaction == nil || transaction.engine == nil {
		return Decision{}, fmt.Errorf("Common transaction is nil")
	}
	transaction.engine.mu.Lock()
	defer transaction.engine.mu.Unlock()
	if err := transaction.assertUsableLocked(); err != nil {
		return Decision{}, err
	}
	if direction == DirectionRequest {
		if transaction.begun {
			return Decision{}, fmt.Errorf("duplicate Common request headers")
		}
		request, cleanup, err := newCommonRequest(transaction.metadata, headers)
		if err != nil {
			return Decision{}, err
		}
		defer cleanup()
		var native *C.msc_envoy_ext_proc_transaction
		var nativeDecision C.msc_envoy_ext_proc_decision
		var nativeError [commonRuntimeErrorBufferSize]C.char
		if C.msc_envoy_ext_proc_transaction_begin(transaction.engine.runtime,
			request.value, cBoolean(endOfStream), &native, &nativeDecision,
			&nativeError[0], C.size_t(len(nativeError))) == 0 {
			return Decision{}, fmt.Errorf("Common request headers: %s", nativeErrorText(nativeError[:]))
		}
		if native == nil {
			return Decision{}, fmt.Errorf("Common request headers returned no transaction")
		}
		transaction.native = native
		transaction.begun = true
		transaction.updateTransactionIDLocked()
		return commonDecision(nativeDecision), nil
	}
	if direction != DirectionResponse || !transaction.begun || transaction.native == nil {
		return Decision{}, fmt.Errorf("response headers before Common request transaction")
	}
	response, cleanup, err := newCommonResponse(transaction.metadata.Request.Protocol, headers)
	if err != nil {
		return Decision{}, err
	}
	defer cleanup()
	var nativeDecision C.msc_envoy_ext_proc_decision
	var nativeError [commonRuntimeErrorBufferSize]C.char
	if C.msc_envoy_ext_proc_transaction_process_response_headers(transaction.native,
		response.value, cBoolean(endOfStream), &nativeDecision,
		&nativeError[0], C.size_t(len(nativeError))) == 0 {
		return Decision{}, fmt.Errorf("Common response headers: %s", nativeErrorText(nativeError[:]))
	}
	transaction.updateTransactionIDLocked()
	return commonDecision(nativeDecision), nil
}

func (transaction *commonRuntimeTransaction) ProcessBody(ctx context.Context, direction Direction, body []byte, endOfStream bool) (Decision, error) {
	if err := ctx.Err(); err != nil {
		return Decision{}, err
	}
	if transaction == nil || transaction.engine == nil {
		return Decision{}, fmt.Errorf("Common transaction is nil")
	}
	transaction.engine.mu.Lock()
	defer transaction.engine.mu.Unlock()
	if err := transaction.assertUsableLocked(); err != nil {
		return Decision{}, err
	}
	if !transaction.begun || transaction.native == nil {
		return Decision{}, fmt.Errorf("Common body before request headers")
	}
	if direction != DirectionRequest && direction != DirectionResponse {
		return Decision{}, fmt.Errorf("unsupported Common body direction %q", direction)
	}
	var nativeBody unsafe.Pointer
	if len(body) > 0 {
		nativeBody = C.CBytes(body)
		defer C.free(nativeBody)
	}
	var nativeDecision C.msc_envoy_ext_proc_decision
	var nativeError [commonRuntimeErrorBufferSize]C.char
	if C.msc_envoy_ext_proc_transaction_process_body(transaction.native,
		cBoolean(direction == DirectionResponse), (*C.uchar)(nativeBody), C.size_t(len(body)),
		cBoolean(endOfStream), &nativeDecision, &nativeError[0],
		C.size_t(len(nativeError))) == 0 {
		return Decision{}, fmt.Errorf("Common %s body: %s", direction, nativeErrorText(nativeError[:]))
	}
	transaction.updateTransactionIDLocked()
	return commonDecision(nativeDecision), nil
}

// MarkResponseCommitted records a response-header CONTINUE only after its
// matching gRPC response was successfully written to Envoy. It deliberately
// does not claim that a downstream byte was observed.
func (transaction *commonRuntimeTransaction) MarkResponseCommitted(ctx context.Context) error {
	if err := ctx.Err(); err != nil {
		return err
	}
	if transaction == nil || transaction.engine == nil {
		return fmt.Errorf("Common transaction is nil")
	}
	transaction.engine.mu.Lock()
	defer transaction.engine.mu.Unlock()
	if err := transaction.assertUsableLocked(); err != nil {
		return err
	}
	if !transaction.begun || transaction.native == nil {
		return fmt.Errorf("Common response commit before request headers")
	}
	C.msc_envoy_ext_proc_transaction_mark_response_committed(transaction.native, 0)
	return nil
}

// RecordHostAction writes the Common Runtime's host-confirmed outcome only
// after this adapter successfully sent the matching ext_proc response. The
// C ABI retains the original disruptive decision internally; this method never
// reserializes a request/response payload into an adapter-local event.
func (transaction *commonRuntimeTransaction) RecordHostAction(ctx context.Context, action HostAction) error {
	if err := ctx.Err(); err != nil {
		return err
	}
	if transaction == nil || transaction.engine == nil {
		return fmt.Errorf("Common transaction is nil")
	}
	if action.VisibleStatus < 100 || action.VisibleStatus > 599 {
		return fmt.Errorf("Common host action has invalid visible status")
	}
	if strings.TrimSpace(action.TransportResult) == "" || len(action.TransportResult) > 63 || strings.IndexByte(action.TransportResult, 0) >= 0 {
		return fmt.Errorf("Common host action has invalid transport result")
	}
	var nativeAction C.int
	switch action.Action {
	case AppliedActionDeny:
		nativeAction = C.MSC_ENVOY_EXT_PROC_DENY
	case AppliedActionRedirect:
		nativeAction = C.MSC_ENVOY_EXT_PROC_REDIRECT
	case AppliedActionLogOnly:
		nativeAction = C.MSC_ENVOY_EXT_PROC_LOG_ONLY
	default:
		return fmt.Errorf("unsupported Common host action %q", action.Action)
	}
	cTransportResult := C.CString(action.TransportResult)
	defer C.free(unsafe.Pointer(cTransportResult))
	transaction.engine.mu.Lock()
	defer transaction.engine.mu.Unlock()
	if err := transaction.assertUsableLocked(); err != nil {
		return err
	}
	if !transaction.begun || transaction.native == nil {
		return fmt.Errorf("Common host action before request headers")
	}
	var nativeError [commonRuntimeErrorBufferSize]C.char
	if C.msc_envoy_ext_proc_transaction_record_host_action(transaction.native,
		nativeAction, C.int(action.VisibleStatus), cTransportResult, &nativeError[0],
		C.size_t(len(nativeError))) == 0 {
		return fmt.Errorf("Common host action: %s", nativeErrorText(nativeError[:]))
	}
	return nil
}

func (transaction *commonRuntimeTransaction) TransactionID() string {
	if transaction == nil {
		return ""
	}
	return transaction.transactionID
}

func (transaction *commonRuntimeTransaction) Close(_ context.Context, _ Summary) {
	if transaction == nil || transaction.engine == nil {
		return
	}
	transaction.engine.mu.Lock()
	defer transaction.engine.mu.Unlock()
	if transaction.closed {
		return
	}
	if transaction.native != nil && !transaction.engine.closed {
		C.msc_envoy_ext_proc_transaction_close(transaction.native)
		transaction.native = nil
	}
	transaction.closed = true
	delete(transaction.engine.transactions, transaction)
}

func (transaction *commonRuntimeTransaction) assertUsableLocked() error {
	if transaction.closed {
		return fmt.Errorf("Common transaction is closed")
	}
	if transaction.engine.closed || transaction.engine.runtime == nil {
		return fmt.Errorf("Common runtime engine is closed")
	}
	return nil
}

func (transaction *commonRuntimeTransaction) updateTransactionIDLocked() {
	if transaction.native == nil {
		return
	}
	if nativeID := C.msc_envoy_ext_proc_transaction_id(transaction.native); nativeID != nil {
		transaction.transactionID = C.GoString(nativeID)
	}
}

func commonDecision(native C.msc_envoy_ext_proc_decision) Decision {
	switch int(native.action) {
	case int(C.MSC_ENVOY_EXT_PROC_ALLOW):
		return allowDecision()
	case int(C.MSC_ENVOY_EXT_PROC_REDIRECT):
		return Decision{Action: ActionRedirect, Status: int(native.status), RedirectURL: C.GoString(&native.redirect_url[0])}
	default:
		return Decision{Action: ActionDeny, Status: int(native.status)}
	}
}

func cBoolean(value bool) C.int {
	if value {
		return 1
	}
	return 0
}

func nativeErrorText(value []C.char) string {
	if len(value) == 0 {
		return "unknown Common runtime error"
	}
	text := strings.TrimSpace(C.GoString(&value[0]))
	if text == "" {
		return "unknown Common runtime error"
	}
	return text
}

type commonCHeaders struct {
	values      []C.msc_envoy_ext_proc_header
	native      *C.msc_envoy_ext_proc_header
	allocations []unsafe.Pointer
}

func newCommonCHeaders(headers []Header) (*commonCHeaders, error) {
	normalHeaders := 0
	for _, header := range headers {
		if !strings.HasPrefix(header.Name, ":") {
			normalHeaders++
		}
	}
	converted := &commonCHeaders{}
	if normalHeaders > 0 {
		converted.native = (*C.msc_envoy_ext_proc_header)(C.calloc(C.size_t(normalHeaders), C.size_t(C.sizeof_msc_envoy_ext_proc_header)))
		if converted.native == nil {
			return nil, fmt.Errorf("allocate Common headers")
		}
		converted.values = unsafe.Slice(converted.native, normalHeaders)
	}
	index := 0
	for _, header := range headers {
		// Envoy pseudo headers are mapped to method/URI/status metadata and must
		// not be forwarded as ordinary libmodsecurity headers.
		if strings.HasPrefix(header.Name, ":") {
			continue
		}
		if header.Name == "" || strings.IndexByte(header.Name, 0) >= 0 {
			converted.free()
			return nil, fmt.Errorf("invalid Envoy header name")
		}
		name := C.CBytes([]byte(header.Name))
		converted.allocations = append(converted.allocations, name)
		var value unsafe.Pointer
		if len(header.Value) > 0 {
			value = C.CBytes(header.Value)
			converted.allocations = append(converted.allocations, value)
		}
		converted.values[index].name = (*C.char)(name)
		converted.values[index].name_size = C.size_t(len(header.Name))
		converted.values[index].value = (*C.char)(value)
		converted.values[index].value_size = C.size_t(len(header.Value))
		index++
	}
	return converted, nil
}

func (headers *commonCHeaders) pointer() *C.msc_envoy_ext_proc_header {
	if headers == nil {
		return nil
	}
	return headers.native
}

func (headers *commonCHeaders) free() {
	if headers == nil {
		return
	}
	for _, allocation := range headers.allocations {
		C.free(allocation)
	}
	headers.allocations = nil
	if headers.native != nil {
		C.free(unsafe.Pointer(headers.native))
		headers.native = nil
	}
	headers.values = nil
}

type commonCRequest struct {
	value       *C.msc_envoy_ext_proc_request
	allocations []unsafe.Pointer
	headers     *commonCHeaders
}

func newCommonRequest(metadata StreamMetadata, headers []Header) (*commonCRequest, func(), error) {
	if err := validateCommonRequestMetadata(metadata.Request); err != nil {
		return nil, nil, err
	}
	convertedHeaders, err := newCommonCHeaders(headers)
	if err != nil {
		return nil, nil, err
	}
	request := &commonCRequest{headers: convertedHeaders}
	request.value = (*C.msc_envoy_ext_proc_request)(C.calloc(1, C.size_t(C.sizeof_msc_envoy_ext_proc_request)))
	if request.value == nil {
		convertedHeaders.free()
		return nil, nil, fmt.Errorf("allocate Common request")
	}
	allocate := func(value string) *C.char {
		allocation := C.CString(value)
		request.allocations = append(request.allocations, unsafe.Pointer(allocation))
		return allocation
	}
	request.value.method = allocate(metadata.Request.Method)
	request.value.uri = allocate(metadata.Request.URI)
	request.value.protocol = allocate(metadata.Request.Protocol)
	request.value.hostname = allocate(metadata.Request.Hostname)
	request.value.client_address = allocate(metadata.Request.ClientAddress)
	request.value.client_port = C.int(metadata.Request.ClientPort)
	request.value.server_address = allocate(metadata.Request.ServerAddress)
	request.value.server_port = C.int(metadata.Request.ServerPort)
	request.value.transaction_id = allocate(metadata.TransactionID)
	request.value.headers = convertedHeaders.pointer()
	request.value.header_count = C.size_t(len(convertedHeaders.values))
	return request, request.free, nil
}

func (request *commonCRequest) free() {
	if request == nil {
		return
	}
	for _, allocation := range request.allocations {
		C.free(allocation)
	}
	request.allocations = nil
	request.headers.free()
	if request.value != nil {
		C.free(unsafe.Pointer(request.value))
		request.value = nil
	}
}

type commonCResponse struct {
	value       *C.msc_envoy_ext_proc_response
	allocations []unsafe.Pointer
	headers     *commonCHeaders
}

func newCommonResponse(protocol string, headers []Header) (*commonCResponse, func(), error) {
	if strings.TrimSpace(protocol) == "" || strings.IndexByte(protocol, 0) >= 0 {
		return nil, nil, fmt.Errorf("missing Envoy request.protocol for Common response")
	}
	status, err := envoyResponseStatus(headers)
	if err != nil {
		return nil, nil, err
	}
	convertedHeaders, err := newCommonCHeaders(headers)
	if err != nil {
		return nil, nil, err
	}
	response := &commonCResponse{headers: convertedHeaders}
	response.value = (*C.msc_envoy_ext_proc_response)(C.calloc(1, C.size_t(C.sizeof_msc_envoy_ext_proc_response)))
	if response.value == nil {
		convertedHeaders.free()
		return nil, nil, fmt.Errorf("allocate Common response")
	}
	response.value.status = C.int(status)
	response.value.protocol = C.CString(protocol)
	response.allocations = append(response.allocations, unsafe.Pointer(response.value.protocol))
	response.value.headers = convertedHeaders.pointer()
	response.value.header_count = C.size_t(len(convertedHeaders.values))
	return response, response.free, nil
}

func (response *commonCResponse) free() {
	if response == nil {
		return
	}
	for _, allocation := range response.allocations {
		C.free(allocation)
	}
	response.allocations = nil
	response.headers.free()
	if response.value != nil {
		C.free(unsafe.Pointer(response.value))
		response.value = nil
	}
}

func validateCommonRequestMetadata(metadata RequestMetadata) error {
	for field, value := range map[string]string{
		"method":              metadata.Method,
		"URI":                 metadata.URI,
		"request.protocol":    metadata.Protocol,
		"source.address":      metadata.ClientAddress,
		"destination.address": metadata.ServerAddress,
	} {
		if strings.TrimSpace(value) == "" || strings.IndexByte(value, 0) >= 0 {
			return fmt.Errorf("missing or invalid Envoy %s required by Common runtime", field)
		}
	}
	if metadata.ClientPort < 0 || metadata.ClientPort > 65535 || metadata.ServerPort < 0 || metadata.ServerPort > 65535 {
		return fmt.Errorf("Envoy endpoint port is outside the valid range")
	}
	return nil
}

func envoyResponseStatus(headers []Header) (int, error) {
	for _, header := range headers {
		if header.Name != ":status" {
			continue
		}
		status, err := strconv.Atoi(string(header.Value))
		if err != nil || status < 100 || status > 599 {
			return 0, fmt.Errorf("invalid Envoy response :status")
		}
		return status, nil
	}
	return 0, fmt.Errorf("Envoy response headers are missing :status")
}
