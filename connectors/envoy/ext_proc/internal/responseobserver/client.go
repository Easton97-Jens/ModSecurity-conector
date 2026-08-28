package responseobserver

import (
	"fmt"
	"net/http"
	"strings"
	"time"
)

type header struct{ name, value string }

func (c *client) claim(handle string) (result, error) {
	if !validHandle(handle) {
		return result{}, fmt.Errorf("response observer: malformed response handle")
	}
	return c.call(opClaim, []byte(handle))
}

func (c *client) responseHeaders(status int, headers []header) (result, error) {
	payload, err := appendU16(nil, status)
	if err != nil {
		return result{}, err
	}
	version := "HTTP/1.1"
	payload, err = appendU16(payload, len(version))
	if err != nil {
		return result{}, err
	}
	payload = append(payload, version...)
	payload, err = appendU16(payload, len(headers))
	if err != nil {
		return result{}, err
	}
	for _, h := range headers {
		if len(h.name) == 0 || len(h.name) > 65535 || len(h.value) > 65535 || strings.ContainsAny(h.name, "\x00\r\n") || strings.ContainsAny(h.value, "\x00\r\n") {
			return result{}, fmt.Errorf("response observer: invalid response header")
		}
		payload, err = appendU16(payload, len(h.name))
		if err != nil {
			return result{}, err
		}
		payload = append(payload, h.name...)
		payload, err = appendU16(payload, len(h.value))
		if err != nil {
			return result{}, err
		}
		payload = append(payload, h.value...)
		if len(payload) > maxPayload {
			return result{}, fmt.Errorf("response observer: response headers exceed frame limit")
		}
	}
	return c.call(opResponseHeaders, payload)
}

func (c *client) body(body []byte) (result, error) {
	if len(body) > maxBody {
		return result{}, fmt.Errorf("response observer: response body chunk exceeds limit")
	}
	return c.call(opResponseBody, body)
}

func (c *client) eos() (result, error) { return c.call(opResponseEOS, nil) }

func (c *client) commit(headersSent, bodyStarted bool) (result, error) {
	payload := []byte{0, 0}
	if headersSent {
		payload[0] = 1
	}
	if bodyStarted {
		payload[1] = 1
	}
	return c.call(opCommit, payload)
}

func (c *client) cancel(cause byte) (result, error) {
	if cause > terminationInvalidEngineResponse {
		return result{}, fmt.Errorf("response observer: invalid cancellation cause")
	}
	return c.call(opCancel, []byte{cause})
}

func (c *client) release() (result, error) { return c.call(opRelease, nil) }

func (c *client) outcome(action byte, status int) (result, error) {
	b, err := appendU16([]byte{action, 0}, status)
	if err != nil {
		return result{}, err
	}
	return c.call(opOutcome, b)
}

func responseHeaders(response *http.Response, max int) ([]header, error) {
	if response == nil || max <= 0 {
		return nil, fmt.Errorf("response observer: response is missing")
	}
	result := make([]header, 0, len(response.Header))
	total := 0
	for name, values := range response.Header {
		for _, value := range values {
			if len(result) >= max {
				return nil, fmt.Errorf("response observer: header count exceeds limit")
			}
			if len(name)+len(value) > max {
				return nil, fmt.Errorf("response observer: header exceeds limit")
			}
			total += len(name) + len(value)
			if total > max {
				return nil, fmt.Errorf("response observer: total headers exceed limit")
			}
			result = append(result, header{name: strings.ToLower(name), value: value})
		}
	}
	return result, nil
}

func timeoutOrDefault(value time.Duration) time.Duration {
	if value <= 0 {
		return 200 * time.Millisecond
	}
	return value
}
