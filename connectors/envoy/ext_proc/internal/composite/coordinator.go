// Package composite correlates request authorization with response inspection.
//
// It is deliberately independent of Envoy protobufs.  A transport adapter
// obtains the lease from Admission.Lease, carries it as protected internal
// metadata, and passes its own server-owned stream/session identifier to
// Claim.  Lease values are never emitted to the lifecycle observer.
package composite

import (
	"context"
	"crypto/hmac"
	"crypto/rand"
	"crypto/sha256"
	"crypto/subtle"
	"encoding/base64"
	"encoding/binary"
	"errors"
	"fmt"
	"net"
	"strings"
	"sync"
	"time"

	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/processor"
)

var (
	ErrClosed            = errors.New("composite coordinator is closed")
	ErrExpired           = errors.New("composite lease expired")
	ErrInvalidLease      = errors.New("invalid composite lease")
	ErrOutOfOrder        = errors.New("composite phase out of order")
	ErrLimit             = errors.New("composite limit exceeded")
	ErrNotAllowed        = errors.New("request authorization did not allow")
	ErrDuplicate         = errors.New("composite lease already claimed or terminal")
	ErrSession           = errors.New("composite session mismatch")
	ErrEventBackpressure = errors.New("composite event queue saturated")
	ErrObserver          = errors.New("composite observer failed")
)

type Limits struct {
	Capacity        int
	TTL             time.Duration
	IdleTTL         time.Duration
	MaxRequestBody  int64
	MaxResponseBody int64
	MaxBodyChunks   int
	MaxHeaders      int
	MaxHeaderBytes  int
}

// ReservationSnapshot is the immutable request-header input accepted only
// over the private Traefik UDS.  ForwardAuth never supplies its headers to
// Activate: it can activate only this stored snapshot after its trusted
// X-Forwarded method and URI verify the coordinator-owned binding.
//
// Header names are canonical lower-case HTTP tokens. Repeated values are
// separate, contiguous Header entries and are never comma-joined.
type ReservationSnapshot struct {
	Version       uint8
	Method        string
	URI           string
	Protocol      string
	ServerAddress string
	ServerPort    int
	Headers       []processor.Header
}

const ReservationSnapshotVersion uint8 = 2

func (l Limits) withDefaults() Limits {
	if l.Capacity <= 0 {
		l.Capacity = 128
	}
	if l.TTL <= 0 {
		l.TTL = 30 * time.Second
	}
	if l.IdleTTL <= 0 {
		l.IdleTTL = 5 * time.Second
	}
	if l.MaxRequestBody <= 0 {
		l.MaxRequestBody = 1 << 20
	}
	if l.MaxResponseBody <= 0 {
		l.MaxResponseBody = 1 << 20
	}
	if l.MaxBodyChunks <= 0 {
		l.MaxBodyChunks = 256
	}
	if l.MaxHeaders <= 0 {
		l.MaxHeaders = 256
	}
	if l.MaxHeaderBytes <= 0 {
		l.MaxHeaderBytes = 64 << 10
	}
	return l
}

type Event struct {
	DecisionID       string
	Connector        string
	RuleID           string
	Phase            string
	Outcome          string
	Reason           string
	RequestedAction  string
	ActualHostAction string
	CleanupOutcome   string
	VisibleStatus    int
	RequestPath      string
	ResponsePath     string
	Transport        string
	EventTime        time.Time
}

func pipelineMetadata(connector string) (string, string, string) {
	if connector == "traefik" || connector == "traefik-forwardauth" {
		return "traefik.forwardAuth", "traefik.native_uds", "traefik_forwardauth_private_uds"
	}
	return "envoy.ext_authz", "envoy.ext_proc", "envoy_ext_authz_ext_proc_grpc"
}

type Observer interface{ Observe(Event) error }
type discardObserver struct{}

func (discardObserver) Observe(Event) error { return nil }

type Coordinator struct {
	connector   string
	key         []byte
	limits      Limits
	engine      processor.TransactionOpener
	observer    Observer
	mu          sync.Mutex
	entries     map[string]*entry
	slots       chan struct{}
	closed      bool
	fault       error
	stop        chan struct{}
	stopped     chan struct{}
	events      chan Event
	eventDone   chan struct{}
	eventMu     sync.RWMutex
	eventClosed bool
	finishGate  sync.RWMutex
}

func New(connector string, key []byte, limits Limits, engine processor.TransactionOpener, observer Observer) (*Coordinator, error) {
	if connector == "" || len(key) < 32 || engine == nil {
		return nil, errors.New("connector, 256-bit key, and engine are required")
	}
	if limits.Capacity < 0 || limits.TTL < 0 || limits.IdleTTL < 0 || limits.MaxRequestBody < 0 || limits.MaxResponseBody < 0 || limits.MaxBodyChunks < 0 || limits.MaxHeaders < 0 || limits.MaxHeaderBytes < 0 {
		return nil, ErrLimit
	}
	if limits.Capacity > 4096 {
		return nil, ErrLimit
	}
	if observer == nil {
		observer = discardObserver{}
	}
	l := limits.withDefaults()
	c := &Coordinator{connector: connector, key: append([]byte(nil), key...), limits: l, engine: engine, observer: observer, entries: make(map[string]*entry), slots: make(chan struct{}, l.Capacity), stop: make(chan struct{}), stopped: make(chan struct{}), events: make(chan Event, l.Capacity*8), eventDone: make(chan struct{})}
	go c.dispatchEvents()
	go c.expirer()
	return c, nil
}
func (c *Coordinator) dispatchEvents() {
	defer close(c.eventDone)
	for ev := range c.events {
		if err := c.observer.Observe(ev); err != nil {
			c.setFault(fmt.Errorf("%w: %v", ErrObserver, err))
		}
	}
}

// Err returns the first permanent fail-closed coordinator error, if any.
func (c *Coordinator) Err() error {
	return c.currentFault()
}

func (c *Coordinator) currentFault() error {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.fault
}

func (c *Coordinator) setFault(err error) error {
	if err == nil {
		return nil
	}
	c.mu.Lock()
	newFault := c.fault == nil
	if newFault {
		c.fault = err
	}
	fault := c.fault
	c.mu.Unlock()
	if newFault {
		go c.abortAll("event_delivery_failure")
	}
	return fault
}

func (c *Coordinator) abortAll(reason string) {
	c.mu.Lock()
	entries := c.takeAllLocked()
	c.mu.Unlock()
	for _, e := range entries {
		e.finish(context.Background(), reason)
	}
}

func (c *Coordinator) expirer() {
	d := c.limits.IdleTTL / 2
	if d < 10*time.Millisecond {
		d = 10 * time.Millisecond
	}
	t := time.NewTicker(d)
	defer func() { t.Stop(); close(c.stopped) }()
	for {
		select {
		case <-t.C:
			c.Sweep(time.Now())
		case <-c.stop:
			return
		}
	}
}

func (c *Coordinator) Close() {
	c.mu.Lock()
	if c.closed {
		c.mu.Unlock()
		return
	}
	c.closed = true
	close(c.stop)
	es := c.takeAllLocked()
	c.mu.Unlock()
	<-c.stopped
	for _, e := range es {
		e.finish(context.Background(), "restart")
	}
	// Hold the gate until every cleanup that had already started is complete;
	// only then can event delivery safely close.
	c.finishGate.Lock()
	c.eventMu.Lock()
	c.eventClosed = true
	close(c.events)
	c.eventMu.Unlock()
	c.finishGate.Unlock()
	<-c.eventDone
}

func (c *Coordinator) Restart() error {
	newKey := make([]byte, 32)
	if _, err := rand.Read(newKey); err != nil {
		return err
	}
	c.mu.Lock()
	c.key = newKey
	es := c.takeAllLocked()
	c.mu.Unlock()
	for _, e := range es {
		e.finish(context.Background(), "restart")
	}
	return nil
}

func (c *Coordinator) takeAllLocked() []*entry {
	es := make([]*entry, 0, len(c.entries))
	for id, e := range c.entries {
		delete(c.entries, id)
		es = append(es, e)
	}
	return es
}

// Admission owns the one retained transaction from P1/P2 until Lease or a
// terminal failure.  Its methods are safe to call only by the request stream.
type Admission struct {
	c *Coordinator
	e *entry
}

func (c *Coordinator) BeginRequest(ctx context.Context, meta processor.StreamMetadata, headers []processor.Header, endStream bool) (*Admission, processor.Decision, error) {
	if err := c.admitCapacity(); err != nil {
		return nil, processor.Decision{}, err
	}
	id, err := randomID(32)
	if err != nil {
		c.releaseCapacity()
		return nil, processor.Decision{}, err
	}
	meta.TransactionID = id
	tx, err := c.engine.Open(ctx, meta)
	if err != nil {
		c.releaseCapacity()
		return nil, processor.Decision{}, err
	}
	e := &entry{c: c, id: id, tx: tx, created: time.Now(), last: time.Now(), phase: phaseRequestHeaders, meta: meta, summary: processor.Summary{TransactionID: meta.TransactionID, LateAction: processor.LateActionNone}}
	c.mu.Lock()
	if c.closed || c.fault != nil {
		fault := c.fault
		c.mu.Unlock()
		tx.Close(context.WithoutCancel(ctx), e.summary)
		c.releaseCapacity()
		if fault != nil {
			return nil, processor.Decision{}, fault
		}
		return nil, processor.Decision{}, ErrClosed
	}
	c.entries[id] = e
	c.mu.Unlock()
	decision, err := e.requestHeaders(ctx, headers, endStream)
	if err != nil {
		e.finish(ctx, reason(err))
		return nil, decision, err
	}
	if decision.Action != processor.ActionAllow {
		e.mu.Lock()
		e.markBlockedLocked()
		e.mu.Unlock()
		return &Admission{c: c, e: e}, decision, nil
	}
	return &Admission{c: c, e: e}, decision, nil
}

func (c *Coordinator) admitCapacity() error {
	c.mu.Lock()
	closed := c.closed
	fault := c.fault
	c.mu.Unlock()
	if closed {
		return ErrClosed
	}
	if fault != nil {
		return fault
	}
	select {
	case c.slots <- struct{}{}:
		return nil
	default:
		return ErrLimit
	}
}
func (c *Coordinator) releaseCapacity() {
	select {
	case <-c.slots:
	default:
	}
}

func (e *entry) markBlockedLocked() {
	e.blocked = true
}

func (a *Admission) ProcessBody(ctx context.Context, body []byte, endStream bool) (processor.Decision, error) {
	if a == nil || a.e == nil {
		return processor.Decision{}, ErrClosed
	}
	d, err := a.e.requestBody(ctx, body, endStream)
	if err != nil || d.Action != processor.ActionAllow {
		why := reason(err)
		if why == "" {
			why = "request_block"
		}
		if err != nil && !errors.Is(err, ErrLimit) {
			a.e.finish(ctx, why)
			return d, err
		}
		if err == nil || errors.Is(err, ErrLimit) {
			a.e.mu.Lock()
			a.e.markBlockedLocked()
			a.e.mu.Unlock()
		}
		if err == nil {
			return d, nil
		}
	} else if endStream {
		// A private reservation becomes claimable only after the actual P2
		// allow result.  requestBody deliberately cannot do this itself: its
		// caller is responsible for marking a disruptive P2 as blocked first.
		a.e.mu.Lock()
		eventErr := a.e.markReservedLeaseLocked()
		a.e.mu.Unlock()
		if eventErr != nil {
			a.e.finish(ctx, "event_delivery_failure")
			return d, eventErr
		}
	}
	return d, err
}

// RecordHostAction records the action actually accepted by the host for a
// request-phase disruptive Common decision. The adapter must call Finish or
// Cancel afterwards; a blocked admission can never mint a lease.
func (a *Admission) RecordHostAction(ctx context.Context, action processor.HostAction) error {
	if a == nil || a.e == nil {
		return ErrClosed
	}
	e := a.e
	e.mu.Lock()
	if err := e.checkLocked(); err != nil {
		e.mu.Unlock()
		return err
	}
	if !e.blocked {
		e.mu.Unlock()
		return ErrOutOfOrder
	}
	if e.syntheticRequestBodyLimit {
		e.mu.Unlock()
		return errors.New("synthetic request body limit has no native Common host action")
	}
	if e.hostActionRecorded {
		e.mu.Unlock()
		return ErrDuplicate
	}
	if err := validateHostAction(action); err != nil {
		e.mu.Unlock()
		return err
	}
	if action.Action != processor.AppliedActionDeny && action.Action != processor.AppliedActionRedirect && action.Action != processor.AppliedActionLogOnly {
		e.mu.Unlock()
		return errors.New("invalid host action")
	}
	if recorder, ok := e.tx.(processor.HostActionRecorder); ok {
		if err := recorder.RecordHostAction(ctx, action); err != nil {
			e.mu.Unlock()
			e.finish(context.Background(), "companion_failure")
			return err
		}
	}
	e.hostActionRecorded = true
	err := e.emitLocked(Event{DecisionID: e.id, Connector: e.c.connector, Phase: "request_host_action", Outcome: "recorded", RequestedAction: "block", ActualHostAction: string(action.Action), VisibleStatus: action.VisibleStatus, EventTime: time.Now()})
	e.mu.Unlock()
	if err != nil {
		e.finish(context.Background(), "companion_failure")
		return err
	}
	return nil
}

// RecordRequestBodyLimitHostAction records the bounded 413 selected by the
// coordinator before the overflowing bytes are sent to Common. There is no
// native Common disruptive decision in this path, so it deliberately never
// invokes processor.HostActionRecorder or claims native rule evidence.
func (a *Admission) RecordRequestBodyLimitHostAction() error {
	if a == nil || a.e == nil {
		return ErrClosed
	}
	e := a.e
	e.mu.Lock()
	if err := e.checkLocked(); err != nil {
		e.mu.Unlock()
		return err
	}
	if !e.blocked || !e.syntheticRequestBodyLimit {
		e.mu.Unlock()
		return ErrOutOfOrder
	}
	if e.hostActionRecorded {
		e.mu.Unlock()
		return ErrDuplicate
	}
	e.hostActionRecorded = true
	err := e.emitLocked(Event{DecisionID: e.id, Connector: e.c.connector, Phase: "request_host_action", Outcome: "recorded", Reason: "request_body_limit", RequestedAction: "block", ActualHostAction: string(processor.AppliedActionDeny), VisibleStatus: 413, EventTime: time.Now()})
	e.mu.Unlock()
	if err != nil {
		e.finish(context.Background(), "companion_failure")
		return err
	}
	return nil
}
func (a *Admission) Lease() (string, error) {
	if a == nil || a.e == nil {
		return "", ErrClosed
	}
	return a.e.issueLease()
}
func (a *Admission) Cancel(ctx context.Context) {
	if a != nil && a.e != nil {
		a.e.finish(ctx, "cancel")
	}
}
func (a *Admission) Finish(ctx context.Context, reason string) {
	if a != nil && a.e != nil {
		a.e.finish(ctx, reason)
	}
}

type Response struct {
	c       *Coordinator
	e       *entry
	session string
}

// MarkResponseCommitted records that the adapter successfully continued the
// response. It is not a claim that a client byte was observed.
func (r *Response) MarkResponseCommitted(ctx context.Context) error {
	if r == nil || r.e == nil {
		return ErrClosed
	}
	return r.e.markCommitted(ctx, r.session)
}

// RecordHostAction records only an action actually accepted by the host.
// After commit, disruptive actions are truthfully downgraded to log_only.
func (r *Response) RecordHostAction(ctx context.Context, action processor.HostAction) error {
	if r == nil || r.e == nil {
		return ErrClosed
	}
	return r.e.recordHostAction(ctx, r.session, action)
}

// RecordNeutralOutcome records a safe allow outcome without invoking the
// disruptive Common host-action seam.
func (r *Response) RecordNeutralOutcome(ctx context.Context, visibleStatus int, transportResult string) error {
	if r == nil || r.e == nil {
		return ErrClosed
	}
	if err := validateHostAction(processor.HostAction{Action: processor.AppliedActionLogOnly, VisibleStatus: visibleStatus, TransportResult: transportResult}); err != nil {
		return err
	}
	e := r.e
	e.mu.Lock()
	defer e.mu.Unlock()
	if err := e.checkSessionLocked(r.session); err != nil {
		return err
	}
	if !e.committed || !e.responseEnded {
		return ErrOutOfOrder
	}
	return e.emitLocked(Event{DecisionID: e.id, Connector: e.c.connector, Phase: "neutral_outcome", Outcome: "allow", ActualHostAction: "allow", VisibleStatus: visibleStatus, EventTime: time.Now()})
}

func finishOutOfOrderClaim(e *entry) {
	if !e.reserved {
		go e.finish(context.Background(), "out_of_order")
	}
}

func (c *Coordinator) Claim(token, session string) (*Response, error) {
	if session == "" || len(session) > 256 {
		return nil, ErrSession
	}
	if err := c.currentFault(); err != nil {
		return nil, err
	}
	id, ok := c.verifyToken(token)
	if !ok {
		return nil, ErrInvalidLease
	}
	c.mu.Lock()
	e := c.entries[id]
	c.mu.Unlock()
	if e == nil {
		return nil, ErrExpired
	}
	e.mu.Lock()
	defer e.mu.Unlock()
	if e.expired(time.Now()) {
		go e.finish(context.Background(), "timeout")
		return nil, ErrExpired
	}
	if e.reserved && session != e.session {
		return nil, ErrSession
	}
	if e.claimed && session != e.session {
		go e.finish(context.Background(), "session_mismatch")
		return nil, ErrSession
	}
	if e.claimed || e.terminal {
		go e.finish(context.Background(), "duplicate")
		return nil, ErrDuplicate
	}
	if e.blocked {
		if !e.hostActionRecorded {
			return nil, ErrOutOfOrder
		}
		return nil, ErrNotAllowed
	}
	if e.phase != phaseLeased {
		// A private reservation may be claimed before ForwardAuth has
		// activated it. Leave cleanup to the owning UDS session so a
		// disconnect/abort retains its truthful terminal reason instead of
		// racing an asynchronous out_of_order cleanup.
		finishOutOfOrderClaim(e)
		return nil, ErrOutOfOrder
	}
	e.claimed, e.session, e.phase, e.last = true, session, phaseResponseHeaders, time.Now()
	if err := e.emitLocked(Event{DecisionID: e.id, Connector: c.connector, Phase: "claim", Outcome: "accepted", Reason: ""}); err != nil {
		go e.finish(context.Background(), "event_delivery_failure")
		return nil, err
	}
	return &Response{c: c, e: e, session: session}, nil
}

func (r *Response) Headers(ctx context.Context, headers []processor.Header, endStream bool) (processor.Decision, error) {
	if r == nil || r.e == nil {
		return processor.Decision{}, ErrClosed
	}
	return r.e.responseHeaders(ctx, r.session, headers, endStream)
}
func (r *Response) Body(ctx context.Context, body []byte, endStream bool) (processor.Decision, error) {
	if r == nil || r.e == nil {
		return processor.Decision{}, ErrClosed
	}
	return r.e.responseBody(ctx, r.session, body, endStream)
}
func (r *Response) Finish(ctx context.Context, reason string) {
	if r != nil && r.e != nil {
		r.e.finish(ctx, reason)
	}
}

type phase uint8

const (
	phaseReserved phase = iota
	phaseRequestHeaders
	phaseRequestBody
	phaseLeased
	phaseResponseHeaders
	phaseResponseBody
)

type entry struct {
	c                                                                          *Coordinator
	mu                                                                         sync.Mutex
	id                                                                         string
	tx                                                                         processor.Transaction
	meta                                                                       processor.StreamMetadata
	summary                                                                    processor.Summary
	created, last                                                              time.Time
	phase                                                                      phase
	requestBodyBytes, responseBodyBytes                                        int64
	requestChunks, responseChunks                                              int
	terminal, removed, claimed, leaseIssued, committed, responseEnded, blocked bool
	reserved                                                                   bool
	binding                                                                    [sha256.Size]byte
	snapshot                                                                   ReservationSnapshot
	p4EventEmitted, syntheticRequestBodyLimit, hostActionRecorded              bool
	session                                                                    string
	closeOnce                                                                  sync.Once
}

// Reserve creates a server-owned, single-use lease before the ForwardAuth
// request exists. The immutable snapshot is copied from a private UDS frame;
// no ForwardAuth HTTP header is used as P1 input. The session is generated by
// the private UDS handler and retained on the bounded entry.
func (c *Coordinator) Reserve(session string, snapshot ReservationSnapshot) (string, error) {
	if session == "" || len(session) > 256 {
		return "", ErrSession
	}
	stored, binding, err := cloneReservationSnapshot(c.limits, snapshot)
	if err != nil {
		return "", err
	}
	if err := c.admitCapacity(); err != nil {
		return "", err
	}
	id, err := randomID(32)
	if err != nil {
		c.releaseCapacity()
		return "", err
	}
	now := time.Now()
	e := &entry{c: c, id: id, created: now, last: now, phase: phaseReserved, reserved: true, session: session, binding: binding, snapshot: stored, summary: processor.Summary{TransactionID: id, LateAction: processor.LateActionNone}}
	token, err := c.makeToken(id)
	if err != nil {
		c.releaseCapacity()
		return "", err
	}
	c.mu.Lock()
	if c.closed || c.fault != nil {
		fault := c.fault
		c.mu.Unlock()
		c.releaseCapacity()
		if fault != nil {
			return "", fault
		}
		return "", ErrClosed
	}
	c.entries[id] = e
	c.mu.Unlock()
	// A reservation can be aborted before ForwardAuth has emitted P1/P2. Emit a
	// payload-free lifecycle opener now so the bounded observer can pair that
	// pre-admission abort with its one terminal cleanup instead of seeing an
	// orphan terminal event.
	if err := e.emitLocked(Event{DecisionID: e.id, Connector: c.connector, Phase: "reservation", Outcome: "reserved"}); err != nil {
		e.finish(context.Background(), "event_delivery_failure")
		return "", err
	}
	return token, nil
}

// Activate binds a reserved lease to the one Common transaction used by the
// ForwardAuth request and processes P1/P2. Method and URI originate from
// Traefik-generated ForwardAuth metadata; P1 headers originate exclusively
// from the immutable reservation snapshot. It never creates or returns a new
// lease. The opaque token is consumed only later by Claim on the original
// private UDS session.
func (c *Coordinator) Activate(ctx context.Context, token, method, uri string, meta processor.StreamMetadata, endStream bool) (*Admission, processor.Decision, error) {
	id, ok := c.verifyToken(token)
	if !ok {
		return nil, processor.Decision{}, ErrInvalidLease
	}
	c.mu.Lock()
	e := c.entries[id]
	c.mu.Unlock()
	if e == nil {
		return nil, processor.Decision{}, ErrExpired
	}
	e.mu.Lock()
	if err := e.checkLocked(); err != nil {
		e.mu.Unlock()
		return nil, processor.Decision{}, err
	}
	if !e.reserved || e.phase != phaseReserved || e.tx != nil {
		e.mu.Unlock()
		return nil, processor.Decision{}, ErrDuplicate
	}
	// Hash an explicit version and length-delimited canonical fields rather
	// than an ambiguous separator-delimited string. The stored headers are
	// part of the commitment, but never leave the private UDS/coordinator path.
	snapshot := e.snapshot
	candidate := snapshot
	candidate.Method, candidate.URI = method, uri
	candidateBinding := reservationBinding(candidate)
	if !validReservationMethod(method) || !validReservationURI(uri) ||
		meta.Request.Method != method || meta.Request.URI != uri ||
		!strings.EqualFold(meta.Request.Hostname, reservationSnapshotHost(snapshot.Headers)) ||
		subtle.ConstantTimeCompare(e.binding[:], candidateBinding[:]) != 1 {
		e.mu.Unlock()
		return nil, processor.Decision{}, ErrInvalidLease
	}
	headers := snapshot.Headers
	e.snapshot = ReservationSnapshot{}
	clear(e.binding[:])
	meta.TransactionID = e.id
	meta.Request.Protocol = snapshot.Protocol
	meta.Request.ServerAddress = snapshot.ServerAddress
	meta.Request.ServerPort = snapshot.ServerPort
	tx, err := c.engine.Open(ctx, meta)
	if err != nil {
		e.mu.Unlock()
		wipeReservationHeaders(headers)
		e.finish(ctx, "open_failure")
		return nil, processor.Decision{}, err
	}
	e.tx, e.meta = tx, meta
	e.phase = phaseRequestHeaders
	e.last = time.Now()
	e.mu.Unlock()
	defer wipeReservationHeaders(headers)
	a := &Admission{c: c, e: e}
	d, err := e.requestHeaders(ctx, headers, endStream)
	if err != nil {
		e.finish(ctx, reason(err))
		return nil, d, err
	}
	if d.Action != processor.ActionAllow {
		e.mu.Lock()
		e.markBlockedLocked()
		e.mu.Unlock()
	} else if endStream {
		e.mu.Lock()
		if err := e.markReservedLeaseLocked(); err != nil {
			e.mu.Unlock()
			e.finish(context.Background(), "event_delivery_failure")
			return nil, d, err
		}
		e.mu.Unlock()
	}
	return a, d, nil
}

func reservationSnapshotHost(headers []processor.Header) string {
	for _, header := range headers {
		if header.Name == "host" {
			return string(header.Value)
		}
	}
	return ""
}

// Abort releases a reserved or activated entry for the owning private
// session. Invalid or wrong-session tokens are deliberately non-terminal so
// an attacker cannot delete a valid reservation by guessing its lease.
func (c *Coordinator) Abort(token, session string) error {
	return c.AbortWithReason(token, session, "abort")
}

// AbortWithReason is restricted to connector-owned terminal causes. It lets a
// private UDS read deadline retain its truthful timeout cause instead of
// relabeling it as a generic reservation abort.
func (c *Coordinator) AbortWithReason(token, session, reason string) error {
	switch reason {
	case "abort", "disconnect", "finish", "timeout":
	default:
		return ErrOutOfOrder
	}
	if session == "" || len(session) > 256 {
		return ErrSession
	}
	id, ok := c.verifyToken(token)
	if !ok {
		return ErrInvalidLease
	}
	c.mu.Lock()
	e := c.entries[id]
	c.mu.Unlock()
	if e == nil {
		return ErrExpired
	}
	e.mu.Lock()
	if e.reserved && e.session != session {
		e.mu.Unlock()
		return ErrSession
	}
	blocked := e.blocked
	e.mu.Unlock()
	if blocked {
		reason = "request_block"
	}
	e.finish(context.Background(), reason)
	return nil
}

func (e *entry) expired(now time.Time) bool {
	return now.Sub(e.created) >= e.c.limits.TTL || now.Sub(e.last) >= e.c.limits.IdleTTL
}
func (e *entry) requestHeaders(ctx context.Context, h []processor.Header, eos bool) (processor.Decision, error) {
	e.mu.Lock()
	defer e.mu.Unlock()
	if err := e.checkLocked(); err != nil {
		return processor.Decision{}, err
	}
	if err := checkHeaders(e.c.limits, h); err != nil {
		return processor.Decision{}, err
	}
	d, err := e.tx.ProcessHeaders(ctx, processor.DirectionRequest, h, eos)
	e.summary.RequestHeaderCount = uint64(len(h))
	if eos {
		e.phase = phaseLeased
	} else {
		e.phase = phaseRequestBody
	}
	e.last = time.Now()
	if eventErr := e.emitLocked(Event{DecisionID: e.id, Connector: e.c.connector, RuleID: d.RuleID, Phase: "P1", Outcome: "observed", RequestedAction: string(d.Action), VisibleStatus: d.Status}); eventErr != nil {
		return d, eventErr
	}
	return d, err
}
func (e *entry) requestBody(ctx context.Context, b []byte, eos bool) (processor.Decision, error) {
	e.mu.Lock()
	defer e.mu.Unlock()
	if err := e.checkLocked(); err != nil {
		return processor.Decision{}, err
	}
	if e.phase != phaseRequestBody {
		return processor.Decision{}, ErrOutOfOrder
	}
	if e.requestBodyBytes+int64(len(b)) > e.c.limits.MaxRequestBody || e.requestChunks+1 > e.c.limits.MaxBodyChunks {
		return e.requestBodyLimitLocked()
	}
	e.requestBodyBytes += int64(len(b))
	e.requestChunks++
	d, err := e.tx.ProcessBody(ctx, processor.DirectionRequest, b, eos)
	e.summary.RequestBodyBytes = e.requestBodyBytes
	e.summary.RequestBodyChunks = uint64(e.requestChunks)
	if eos {
		e.phase = phaseLeased
	}
	e.last = time.Now()
	if eventErr := e.emitLocked(Event{DecisionID: e.id, Connector: e.c.connector, RuleID: d.RuleID, Phase: "P2", Outcome: "observed", RequestedAction: string(d.Action), VisibleStatus: d.Status}); eventErr != nil {
		return d, eventErr
	}
	return d, err
}

// markReservedLeaseLocked records readiness of an already-created private
// reservation after the final request phase. It never serializes the opaque
// lease into events and has no effect on Envoy's explicit Admission.Lease
// flow.
func (e *entry) markReservedLeaseLocked() error {
	if !e.reserved || e.leaseIssued || e.blocked || e.phase != phaseLeased {
		return nil
	}
	e.leaseIssued = true
	return e.emitLocked(Event{DecisionID: e.id, Connector: e.c.connector, Phase: "lease", Outcome: "issued"})
}

// requestBodyLimitLocked emits one bounded P2 decision without delivering the
// overflowing bytes to the engine. Adapters can then record the actual 413
// host action and terminal cleanup against the same decision ID.
func (e *entry) requestBodyLimitLocked() (processor.Decision, error) {
	e.blocked = true
	e.syntheticRequestBodyLimit = true
	e.last = time.Now()
	d := processor.Decision{Action: processor.ActionDeny, Status: 413}
	if err := e.emitLocked(Event{DecisionID: e.id, Connector: e.c.connector, Phase: "P2", Outcome: "observed", Reason: "request_body_limit", RequestedAction: string(d.Action), VisibleStatus: d.Status}); err != nil {
		return d, err
	}
	return d, ErrLimit
}
func (e *entry) issueLease() (string, error) {
	e.mu.Lock()
	defer e.mu.Unlock()
	if err := e.checkLocked(); err != nil {
		return "", err
	}
	if e.phase != phaseLeased {
		return "", ErrOutOfOrder
	}
	if e.blocked {
		return "", ErrNotAllowed
	}
	if e.leaseIssued {
		return "", ErrDuplicate
	}
	t, err := e.c.makeToken(e.id)
	if err != nil {
		return "", err
	}
	e.phase = phaseLeased
	e.leaseIssued = true
	e.last = time.Now()
	if err := e.emitLocked(Event{DecisionID: e.id, Connector: e.c.connector, Phase: "lease", Outcome: "issued"}); err != nil {
		return "", err
	}
	return t, nil
}
func (e *entry) responseHeaders(ctx context.Context, s string, h []processor.Header, eos bool) (processor.Decision, error) {
	e.mu.Lock()
	defer e.mu.Unlock()
	if err := e.checkSessionLocked(s); err != nil {
		return processor.Decision{}, err
	}
	if e.phase != phaseResponseHeaders {
		return processor.Decision{}, ErrOutOfOrder
	}
	if err := checkHeaders(e.c.limits, h); err != nil {
		return processor.Decision{}, err
	}
	d, err := e.tx.ProcessHeaders(ctx, processor.DirectionResponse, h, eos)
	e.summary.ResponseHeaderCount = uint64(len(h))
	e.last = time.Now()
	if eventErr := e.emitLocked(Event{DecisionID: e.id, Connector: e.c.connector, RuleID: d.RuleID, Phase: "P3", Outcome: "observed", RequestedAction: string(d.Action), VisibleStatus: d.Status}); eventErr != nil {
		return d, eventErr
	}
	if eos && !e.p4EventEmitted {
		if eventErr := e.emitLocked(Event{DecisionID: e.id, Connector: e.c.connector, RuleID: d.RuleID, Phase: "P4", Outcome: "observed", RequestedAction: string(d.Action), VisibleStatus: d.Status}); eventErr != nil {
			return d, eventErr
		}
		e.p4EventEmitted = true
	}
	if err != nil {
		go e.finish(context.Background(), "companion_failure")
	}
	// The adapter must record the actual host action before terminal cleanup.
	if eos {
		e.responseEnded = true
	} else {
		e.phase = phaseResponseBody
	}
	return d, err
}
func (e *entry) responseBody(ctx context.Context, s string, b []byte, eos bool) (processor.Decision, error) {
	e.mu.Lock()
	defer e.mu.Unlock()
	if err := e.checkSessionLocked(s); err != nil {
		return processor.Decision{}, err
	}
	if e.phase != phaseResponseBody {
		return processor.Decision{}, ErrOutOfOrder
	}
	if e.responseBodyBytes+int64(len(b)) > e.c.limits.MaxResponseBody {
		return processor.Decision{}, ErrLimit
	}
	e.responseBodyBytes += int64(len(b))
	e.responseChunks++
	if e.responseChunks > e.c.limits.MaxBodyChunks {
		return processor.Decision{}, ErrLimit
	}
	d, err := e.tx.ProcessBody(ctx, processor.DirectionResponse, b, eos)
	e.summary.ResponseBodyBytes = e.responseBodyBytes
	e.summary.ResponseBodyChunks++
	e.last = time.Now()
	if eos {
		e.responseEnded = true
	}
	// STREAMED response bodies may contain several chunks.  P4 is one logical
	// phase, so emit it once: at the first disruptive decision (to preserve the
	// requested action) or at EOS when every chunk allowed the response.
	if (eos || d.Action != processor.ActionAllow) && !e.p4EventEmitted {
		if eventErr := e.emitLocked(Event{DecisionID: e.id, Connector: e.c.connector, RuleID: d.RuleID, Phase: "P4", Outcome: "observed", RequestedAction: string(d.Action), VisibleStatus: d.Status}); eventErr != nil {
			return d, eventErr
		}
		e.p4EventEmitted = true
	}
	if err != nil {
		go e.finish(context.Background(), "companion_failure")
	}
	return d, err
}
func (e *entry) markCommitted(ctx context.Context, s string) error {
	e.mu.Lock()
	defer e.mu.Unlock()
	if err := e.checkSessionLocked(s); err != nil {
		return err
	}
	if e.committed {
		return ErrDuplicate
	}
	if committer, ok := e.tx.(processor.ResponseCommitter); ok {
		if err := committer.MarkResponseCommitted(ctx); err != nil {
			go e.finish(context.Background(), "companion_failure")
			return err
		}
	}
	e.committed = true
	e.last = time.Now()
	return nil
}
func (e *entry) recordHostAction(ctx context.Context, s string, action processor.HostAction) error {
	e.mu.Lock()
	if err := e.checkSessionLocked(s); err != nil {
		e.mu.Unlock()
		return err
	}
	if err := validateHostAction(action); err != nil {
		e.mu.Unlock()
		return err
	}
	if action.Action != processor.AppliedActionDeny && action.Action != processor.AppliedActionRedirect && action.Action != processor.AppliedActionLogOnly {
		e.mu.Unlock()
		return errors.New("invalid host action")
	}
	if e.hostActionRecorded {
		e.mu.Unlock()
		return ErrDuplicate
	}
	if e.committed && action.Action != processor.AppliedActionLogOnly {
		action.Action = processor.AppliedActionLogOnly
		action.TransportResult = "log_only"
	}
	if recorder, ok := e.tx.(processor.HostActionRecorder); ok {
		if err := recorder.RecordHostAction(ctx, action); err != nil {
			e.mu.Unlock()
			e.finish(context.Background(), "companion_failure")
			return err
		}
	}
	e.hostActionRecorded = true
	err := e.emitLocked(Event{DecisionID: e.id, Connector: e.c.connector, Phase: "host_action", Outcome: "recorded", ActualHostAction: string(action.Action), VisibleStatus: action.VisibleStatus, EventTime: time.Now()})
	e.mu.Unlock()
	if err != nil {
		e.finish(context.Background(), "companion_failure")
	}
	return err
}
func (e *entry) checkLocked() error {
	if err := e.c.currentFault(); err != nil {
		return err
	}
	if e.terminal || e.removed {
		return ErrClosed
	}
	if e.expired(time.Now()) {
		return ErrExpired
	}
	return nil
}
func (e *entry) checkSessionLocked(s string) error {
	if err := e.checkLocked(); err != nil {
		return err
	}
	if !e.claimed || s != e.session {
		e.terminal = true
		go e.finish(context.Background(), "session_mismatch")
		return ErrSession
	}
	return nil
}
func (e *entry) emitLocked(ev Event) error {
	if ev.RequestPath == "" || ev.ResponsePath == "" || ev.Transport == "" {
		ev.RequestPath, ev.ResponsePath, ev.Transport = pipelineMetadata(e.c.connector)
	}
	if ev.EventTime.IsZero() {
		ev.EventTime = time.Now()
	}
	e.c.eventMu.RLock()
	if e.c.eventClosed {
		e.c.eventMu.RUnlock()
		return ErrClosed
	}
	select {
	case e.c.events <- ev:
		e.c.eventMu.RUnlock()
		return nil
	default:
		e.c.eventMu.RUnlock()
		return e.c.setFault(ErrEventBackpressure)
	}
}

func validateHostAction(action processor.HostAction) error {
	if action.VisibleStatus < 100 || action.VisibleStatus > 599 {
		return errors.New("invalid host status")
	}
	if len(action.TransportResult) == 0 || len(action.TransportResult) > 128 {
		return errors.New("invalid host transport result")
	}
	for _, b := range []byte(action.TransportResult) {
		if b < 0x20 || b > 0x7e {
			return errors.New("invalid host transport result")
		}
	}
	return nil
}
func (e *entry) finish(ctx context.Context, why string) {
	e.c.finishGate.RLock()
	defer e.c.finishGate.RUnlock()
	e.closeOnce.Do(func() {
		e.mu.Lock()
		if e.terminal && !e.removed {
			e.removed = true
		}
		e.terminal = true
		e.summary.CloseReason = processor.CloseReason(why)
		wipeReservationHeaders(e.snapshot.Headers)
		e.snapshot = ReservationSnapshot{}
		clear(e.binding[:])
		e.mu.Unlock()
		e.c.mu.Lock()
		delete(e.c.entries, e.id)
		e.c.mu.Unlock()
		e.c.releaseCapacity()
		if e.tx != nil {
			e.tx.Close(ctx, e.summary)
		}
		_ = e.emitLocked(Event{DecisionID: e.id, Connector: e.c.connector, Phase: "terminal", Outcome: "closed", Reason: why, CleanupOutcome: "closed", EventTime: time.Now()})
	})
}

func (c *Coordinator) Sweep(now time.Time) {
	c.mu.Lock()
	all := make([]*entry, 0, len(c.entries))
	for _, e := range c.entries {
		all = append(all, e)
	}
	c.mu.Unlock()
	es := make([]*entry, 0)
	for _, e := range all {
		e.mu.Lock()
		expired := e.expired(now)
		e.mu.Unlock()
		if expired {
			c.mu.Lock()
			if c.entries[e.id] == e {
				delete(c.entries, e.id)
				es = append(es, e)
			}
			c.mu.Unlock()
		}
	}
	for _, e := range es {
		e.finish(context.Background(), "timeout")
	}
}
func checkHeaders(l Limits, h []processor.Header) error {
	if len(h) > l.MaxHeaders {
		return ErrLimit
	}
	n := 0
	for _, x := range h {
		n += len(x.Name) + len(x.Value)
		if n > l.MaxHeaderBytes {
			return ErrLimit
		}
	}
	return nil
}

func cloneReservationSnapshot(l Limits, snapshot ReservationSnapshot) (ReservationSnapshot, [sha256.Size]byte, error) {
	if snapshot.Version != ReservationSnapshotVersion || !validReservationMethod(snapshot.Method) || !validReservationURI(snapshot.URI) {
		return ReservationSnapshot{}, [sha256.Size]byte{}, ErrInvalidLease
	}
	if !validReservationMetadata(snapshot.Protocol, snapshot.ServerAddress, snapshot.ServerPort) {
		return ReservationSnapshot{}, [sha256.Size]byte{}, ErrInvalidLease
	}
	if err := checkHeaders(l, snapshot.Headers); err != nil {
		return ReservationSnapshot{}, [sha256.Size]byte{}, err
	}
	stored := ReservationSnapshot{
		Version:       snapshot.Version,
		Method:        snapshot.Method,
		URI:           snapshot.URI,
		Protocol:      snapshot.Protocol,
		ServerAddress: snapshot.ServerAddress,
		ServerPort:    snapshot.ServerPort,
		Headers:       make([]processor.Header, len(snapshot.Headers)),
	}
	lastName := ""
	hostValues := 0
	for i, header := range snapshot.Headers {
		if !validReservationHeaderName(header.Name) || header.Name != strings.ToLower(header.Name) ||
			(lastName != "" && header.Name < lastName) || invalidReservationHeaderValue(header.Value) {
			wipeReservationHeaders(stored.Headers)
			return ReservationSnapshot{}, [sha256.Size]byte{}, ErrInvalidLease
		}
		if header.Name == "host" {
			hostValues++
		}
		lastName = header.Name
		stored.Headers[i] = processor.Header{Name: header.Name, Value: append([]byte(nil), header.Value...)}
	}
	if hostValues != 1 {
		wipeReservationHeaders(stored.Headers)
		return ReservationSnapshot{}, [sha256.Size]byte{}, ErrInvalidLease
	}
	return stored, reservationBinding(stored), nil
}

func validReservationMetadata(protocol, serverAddress string, serverPort int) bool {
	if protocol == "" || len(protocol) > 16 || serverAddress == "" || len(serverAddress) > 256 || serverPort < 1 || serverPort > 65535 {
		return false
	}
	return strings.HasPrefix(protocol, "HTTP/") && !strings.ContainsAny(protocol, "\r\n\x00") && net.ParseIP(serverAddress) != nil
}

func validReservationMethod(value string) bool {
	return len(value) > 0 && len(value) <= 256 && validReservationHeaderName(value)
}

func validReservationURI(value string) bool {
	if len(value) == 0 || len(value) > 64<<10 || !strings.HasPrefix(value, "/") {
		return false
	}
	return !strings.ContainsAny(value, "\r\n\x00")
}

func validReservationHeaderName(value string) bool {
	if value == "" || len(value) > 256 {
		return false
	}
	for i := 0; i < len(value); i++ {
		c := value[i]
		if (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') {
			continue
		}
		if !strings.ContainsRune("!#$%&'*+-.^_`|~", rune(c)) {
			return false
		}
	}
	return true
}

func invalidReservationHeaderValue(value []byte) bool {
	if len(value) > 8192 {
		return true
	}
	for _, b := range value {
		if b == '\r' || b == '\n' || b == 0 {
			return true
		}
	}
	return false
}

// reservationBinding commits to the complete, canonical reservation input.
// Every field is explicitly length-delimited so method, URI, name, and value
// boundaries cannot be confused by delimiter contents.
func reservationBinding(snapshot ReservationSnapshot) [sha256.Size]byte {
	h := sha256.New()
	_, _ = h.Write([]byte{snapshot.Version})
	writeReservationField(h, []byte(snapshot.Method))
	writeReservationField(h, []byte(snapshot.URI))
	writeReservationField(h, []byte(snapshot.Protocol))
	writeReservationField(h, []byte(snapshot.ServerAddress))
	var port [4]byte
	binary.BigEndian.PutUint32(port[:], uint32(snapshot.ServerPort))
	_, _ = h.Write(port[:])
	var count [4]byte
	binary.BigEndian.PutUint32(count[:], uint32(len(snapshot.Headers)))
	_, _ = h.Write(count[:])
	for _, header := range snapshot.Headers {
		writeReservationField(h, []byte(header.Name))
		writeReservationField(h, header.Value)
	}
	var sum [sha256.Size]byte
	copy(sum[:], h.Sum(nil))
	return sum
}

func writeReservationField(h interface{ Write([]byte) (int, error) }, value []byte) {
	var size [4]byte
	binary.BigEndian.PutUint32(size[:], uint32(len(value)))
	_, _ = h.Write(size[:])
	_, _ = h.Write(value)
}

func wipeReservationHeaders(headers []processor.Header) {
	for i := range headers {
		clear(headers[i].Value)
		headers[i].Value = nil
		headers[i].Name = ""
	}
}
func randomID(n int) (string, error) {
	b := make([]byte, n)
	if _, err := rand.Read(b); err != nil {
		return "", err
	}
	return base64.RawURLEncoding.EncodeToString(b), nil
}
func (c *Coordinator) makeToken(id string) (string, error) {
	raw, _ := base64.RawURLEncoding.DecodeString(id)
	nonce := make([]byte, 32)
	if _, err := rand.Read(nonce); err != nil {
		return "", err
	}
	p := make([]byte, 1+32+32)
	p[0] = 1
	copy(p[1:], raw)
	copy(p[33:], nonce)
	c.mu.Lock()
	key := append([]byte(nil), c.key...)
	connector := c.connector
	c.mu.Unlock()
	mac := hmac.New(sha256.New, key)
	mac.Write([]byte(connector))
	mac.Write(p)
	return base64.RawURLEncoding.EncodeToString(append(p, mac.Sum(nil)...)), nil
}
func (c *Coordinator) verifyToken(token string) (string, bool) {
	b, err := base64.RawURLEncoding.DecodeString(token)
	if err != nil || len(b) != 1+32+32+32 || b[0] != 1 {
		return "", false
	}
	if base64.RawURLEncoding.EncodeToString(b) != token {
		return "", false
	}
	p, tag := b[:65], b[65:]
	c.mu.Lock()
	key := append([]byte(nil), c.key...)
	connector := c.connector
	c.mu.Unlock()
	mac := hmac.New(sha256.New, key)
	mac.Write([]byte(connector))
	mac.Write(p)
	if !hmac.Equal(tag, mac.Sum(nil)) {
		return "", false
	}
	return base64.RawURLEncoding.EncodeToString(p[1:33]), true
}
func reason(err error) string {
	if err == nil {
		return ""
	}
	if errors.Is(err, ErrLimit) {
		return "limit"
	}
	if errors.Is(err, ErrExpired) {
		return "timeout"
	}
	return fmt.Sprintf("failure:%v", err)
}
