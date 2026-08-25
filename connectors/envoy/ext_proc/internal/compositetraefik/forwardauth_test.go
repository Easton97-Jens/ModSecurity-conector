package compositetraefik

import (
	"bytes"
	"context"
	"net"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/composite"
	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/processor"
)

type snapshotP1Engine struct {
	headers    []processor.Header
	bodyCalls  int
	denyStatus int
}

func (e *snapshotP1Engine) Open(context.Context, processor.StreamMetadata) (processor.Transaction, error) {
	return &snapshotP1Tx{engine: e}, nil
}

type snapshotP1Tx struct{ engine *snapshotP1Engine }

func (t *snapshotP1Tx) ProcessHeaders(_ context.Context, direction processor.Direction, headers []processor.Header, _ bool) (processor.Decision, error) {
	if direction != processor.DirectionRequest {
		return processor.Decision{Action: processor.ActionAllow}, nil
	}
	t.engine.headers = make([]processor.Header, len(headers))
	for i, header := range headers {
		t.engine.headers[i] = processor.Header{Name: header.Name, Value: append([]byte(nil), header.Value...)}
		if header.Name == "x-msconnector-vector" && string(header.Value) == "p1-block" {
			status := t.engine.denyStatus
			if status == 0 {
				status = http.StatusForbidden
			}
			return processor.Decision{Action: processor.ActionDeny, Status: status}, nil
		}
	}
	return processor.Decision{Action: processor.ActionAllow}, nil
}

func (t *snapshotP1Tx) ProcessBody(context.Context, processor.Direction, []byte, bool) (processor.Decision, error) {
	t.engine.bodyCalls++
	return processor.Decision{Action: processor.ActionAllow}, nil
}
func (*snapshotP1Tx) Close(context.Context, processor.Summary) {}

func TestForwardAuthNeverReturnsLeaseHeader(t *testing.T) {
	c, err := composite.New("traefik", []byte("01234567890123456789012345678901"), composite.Limits{}, processor.PassthroughEngine{}, nil)
	if err != nil {
		t.Fatal(err)
	}
	defer c.Close()
	body := []byte("hello")
	token, err := c.Reserve("uds-session", composite.ReservationSnapshot{Version: composite.ReservationSnapshotVersion, Method: http.MethodPost, URI: "/check", Headers: []processor.Header{{Name: "host", Value: []byte("example.test")}}})
	if err != nil {
		t.Fatal(err)
	}
	req := httptest.NewRequest(http.MethodPost, "http://127.0.0.1/check", bytes.NewReader(body))
	req.Header.Add(LeaseHeader, token)
	req.Header.Add("X-Forwarded-Method", http.MethodPost)
	req.Header.Add("X-Forwarded-Uri", "/check")
	req.Header.Add("X-Forwarded-Proto", "http")
	req.Header.Add("X-Forwarded-Host", "example.test")
	req.Header.Add("X-Forwarded-For", "127.0.0.1")
	req = req.WithContext(context.WithValue(req.Context(), http.LocalAddrContextKey, &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 19182}))
	rec := httptest.NewRecorder()
	(&ForwardAuth{Coordinator: c}).ServeHTTP(rec, req)
	if rec.Code != http.StatusOK {
		t.Fatalf("status = %d, body=%s", rec.Code, rec.Body.String())
	}
	if got := rec.Header().Get(LeaseHeader); got != "" {
		t.Fatalf("sensitive response metadata leaked: lease=%q", got)
	}
}

func TestForwardAuthUsesOnlyPrivateReservationSnapshotForP1(t *testing.T) {
	engine := &snapshotP1Engine{}
	c, err := composite.New("traefik", []byte("01234567890123456789012345678901"), composite.Limits{}, engine, nil)
	if err != nil {
		t.Fatal(err)
	}
	defer c.Close()
	token, err := c.Reserve("uds-session", composite.ReservationSnapshot{
		Version: composite.ReservationSnapshotVersion,
		Method:  http.MethodPost,
		URI:     "/snapshot",
		Headers: []processor.Header{
			{Name: "host", Value: []byte("example.test")},
			{Name: "x-msconnector-vector", Value: []byte("p1-block")},
		},
	})
	if err != nil {
		t.Fatal(err)
	}
	req := httptest.NewRequest(http.MethodPost, "http://127.0.0.1/snapshot", bytes.NewBufferString("body"))
	req.Header.Set(LeaseHeader, token)
	req.Header.Set("X-Forwarded-Method", http.MethodPost)
	req.Header.Set("X-Forwarded-Uri", "/snapshot")
	req.Header.Set("X-Forwarded-Proto", "http")
	req.Header.Set("X-Forwarded-Host", "example.test")
	req.Header.Set("X-Forwarded-For", "127.0.0.1")
	// This request has no vector header. A deny proves P1 came exclusively
	// from the UDS-retained snapshot, not from the ForwardAuth HTTP allow-list.
	req = req.WithContext(context.WithValue(req.Context(), http.LocalAddrContextKey, &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 19182}))
	rec := httptest.NewRecorder()
	(&ForwardAuth{Coordinator: c}).ServeHTTP(rec, req)
	if rec.Code != http.StatusForbidden {
		t.Fatalf("status = %d, body=%q", rec.Code, rec.Body.String())
	}
	if engine.bodyCalls != 0 {
		t.Fatalf("P2 ran after P1 terminal decision: %d", engine.bodyCalls)
	}
	if len(engine.headers) != 2 || engine.headers[1].Name != "x-msconnector-vector" || string(engine.headers[1].Value) != "p1-block" {
		t.Fatalf("P1 headers = %#v", engine.headers)
	}
}

func TestForwardAuthNormalizesInvalidRequestDenyStatus(t *testing.T) {
	for _, malformedStatus := range []int{http.StatusEarlyHints, http.StatusOK} {
		t.Run(http.StatusText(malformedStatus), func(t *testing.T) {
			engine := &snapshotP1Engine{denyStatus: malformedStatus}
			c, err := composite.New("traefik", []byte("01234567890123456789012345678901"), composite.Limits{}, engine, nil)
			if err != nil {
				t.Fatal(err)
			}
			defer c.Close()
			token, err := c.Reserve("uds-session", composite.ReservationSnapshot{
				Version: composite.ReservationSnapshotVersion,
				Method:  http.MethodGet,
				URI:     "/invalid-deny",
				Headers: []processor.Header{
					{Name: "host", Value: []byte("example.test")},
					{Name: "x-msconnector-vector", Value: []byte("p1-block")},
				},
			})
			if err != nil {
				t.Fatal(err)
			}
			req := httptest.NewRequest(http.MethodGet, "http://127.0.0.1/invalid-deny", nil)
			req.Header.Set(LeaseHeader, token)
			req.Header.Set("X-Forwarded-Method", http.MethodGet)
			req.Header.Set("X-Forwarded-Uri", "/invalid-deny")
			req.Header.Set("X-Forwarded-Proto", "http")
			req.Header.Set("X-Forwarded-Host", "example.test")
			req.Header.Set("X-Forwarded-For", "127.0.0.1")
			req = req.WithContext(context.WithValue(req.Context(), http.LocalAddrContextKey, &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 19182}))
			rec := httptest.NewRecorder()
			(&ForwardAuth{Coordinator: c}).ServeHTTP(rec, req)
			if rec.Code != http.StatusForbidden {
				t.Fatalf("invalid request deny status reached client: got %d, want %d", rec.Code, http.StatusForbidden)
			}
		})
	}
}

func TestForwardAuthRejectsNonIPAddressForwardedClient(t *testing.T) {
	c, err := composite.New("traefik", []byte("01234567890123456789012345678901"), composite.Limits{}, processor.PassthroughEngine{}, nil)
	if err != nil {
		t.Fatal(err)
	}
	defer c.Close()
	token, err := c.Reserve("uds-session", composite.ReservationSnapshot{Version: composite.ReservationSnapshotVersion, Method: http.MethodGet, URI: "/", Headers: []processor.Header{{Name: "host", Value: []byte("example.test")}}})
	if err != nil {
		t.Fatal(err)
	}
	req := httptest.NewRequest(http.MethodGet, "http://127.0.0.1/", nil)
	req.Header.Set(LeaseHeader, token)
	req.Header.Set("X-Forwarded-Method", http.MethodGet)
	req.Header.Set("X-Forwarded-Uri", "/")
	req.Header.Set("X-Forwarded-Proto", "http")
	req.Header.Set("X-Forwarded-Host", "example.test")
	req.Header.Set("X-Forwarded-For", "untrusted-client-name")
	req = req.WithContext(context.WithValue(req.Context(), http.LocalAddrContextKey, &net.TCPAddr{IP: net.ParseIP("127.0.0.1"), Port: 19182}))
	rec := httptest.NewRecorder()
	(&ForwardAuth{Coordinator: c}).ServeHTTP(rec, req)
	if rec.Code != http.StatusServiceUnavailable {
		t.Fatalf("status = %d", rec.Code)
	}
}
