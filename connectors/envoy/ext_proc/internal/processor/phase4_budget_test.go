package processor

import (
	"math"
	"testing"
)

type phase4BudgetTestEngine struct {
	PassthroughEngine
	disabled bool
}

func (engine phase4BudgetTestEngine) Phase4BodyBudgetDisabled() bool {
	return engine.disabled
}

func TestPhase4BodyBudgetModes(t *testing.T) {
	cases := []struct {
		name      string
		direction Direction
		disabled  bool
		current   int64
		chunk     int
		want      Action
	}{
		{"off-response-above-budget", DirectionResponse, true, 8, 1, ActionAllow},
		{"enabled-response-above-budget", DirectionResponse, false, 8, 1, ActionDeny},
		{"enabled-exact-limit", DirectionResponse, false, 7, 1, ActionAllow},
		{"off-still-limits-chunk", DirectionResponse, true, 0, 17, ActionDeny},
		{"off-still-limits-request", DirectionRequest, true, 8, 1, ActionDeny},
		{"off-still-rejects-overflow", DirectionResponse, true, math.MaxInt64, 1, ActionDeny},
		{"off-still-rejects-negative-length", DirectionResponse, true, 0, -1, ActionDeny},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			state := &streamState{
				config:  Config{MaxBodyChunkBytes: 16, MaxRequestBodyBytes: 8, MaxResponseBodyBytes: 8},
				engine:  phase4BudgetTestEngine{disabled: tc.disabled},
				summary: Summary{RequestBodyBytes: tc.current, ResponseBodyBytes: tc.current},
			}
			if got := state.bodyLimitDecision(tc.direction, tc.chunk); got.Action != tc.want {
				t.Fatalf("action = %s, want %s", got.Action, tc.want)
			}
		})
	}
}

func TestMissingPhase4BudgetCapabilityKeepsLimit(t *testing.T) {
	state := &streamState{
		config:  Config{MaxBodyChunkBytes: 16, MaxRequestBodyBytes: 8, MaxResponseBodyBytes: 8},
		engine:  PassthroughEngine{},
		summary: Summary{ResponseBodyBytes: 8},
	}
	if got := state.bodyLimitDecision(DirectionResponse, 1); got.Action != ActionDeny {
		t.Fatalf("missing budget capability unexpectedly allowed response: %s", got.Action)
	}
}
