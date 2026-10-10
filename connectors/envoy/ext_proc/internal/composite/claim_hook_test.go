package composite

import (
	"context"
	"errors"
	"testing"

	"github.com/Easton97-Jens/ModSecurity-conector/connectors/envoy/ext_proc/internal/processor"
)

type claimHookEngine struct{ tx *claimHookTransaction }

func (e claimHookEngine) Open(context.Context, processor.StreamMetadata) (processor.Transaction, error) {
	return e.tx, nil
}

type claimHookTransaction struct {
	fakeTx
	claims       int
	err          error
	contextValue any
}

func (tx *claimHookTransaction) ClaimResponseCompanion(ctx context.Context) error {
	tx.claims++
	tx.contextValue = ctx.Value(claimContextKey{})
	return tx.err
}

type claimContextKey struct{}

func TestClaimContextCallsNativeHookOnlyAfterLeaseGuards(t *testing.T) {
	for _, fail := range []bool{false, true} {
		t.Run(map[bool]string{false: "success", true: "failure"}[fail], func(t *testing.T) {
			tx := &claimHookTransaction{}
			if fail {
				tx.err = errors.New("native claim rejected")
			}
			c, err := New("envoy", []byte("01234567890123456789012345678901"), Limits{}, claimHookEngine{tx}, &eventLog{})
			if err != nil {
				t.Fatal(err)
			}
			defer c.Close()
			a, _, err := c.BeginRequest(context.Background(), metadata(), nil, true)
			if err != nil {
				t.Fatal(err)
			}
			token, err := a.Lease()
			if err != nil {
				t.Fatal(err)
			}
			for _, invalid := range []struct{ token, session string }{{token + "x", "s"}, {token, ""}} {
				if _, err := c.ClaimContext(context.Background(), invalid.token, invalid.session); err == nil {
					t.Fatal("invalid claim accepted")
				}
			}
			ctx, cancel := context.WithCancel(context.Background())
			cancel()
			if _, err := c.ClaimContext(ctx, token, "s"); !errors.Is(err, context.Canceled) {
				t.Fatal(err)
			}
			if tx.claims != 0 {
				t.Fatalf("invalid claim called native hook %d times", tx.claims)
			}
			ctx = context.WithValue(context.Background(), claimContextKey{}, "trusted-caller")
			r, err := c.ClaimContext(ctx, token, "s")
			if tx.claims != 1 || tx.contextValue != "trusted-caller" {
				t.Fatalf("hook state: %d/%v", tx.claims, tx.contextValue)
			}
			if fail {
				if r != nil || !errors.Is(err, tx.err) {
					t.Fatalf("failed hook accepted: %v/%v", r, err)
				}
				a.e.mu.Lock()
				accepted := a.e.claimed
				a.e.mu.Unlock()
				if accepted {
					t.Fatal("failed native claim set claimed")
				}
			} else if err != nil || r == nil {
				t.Fatalf("valid claim failed: %v", err)
			}
			if _, err := c.ClaimContext(context.Background(), token, "s"); err == nil {
				t.Fatal("replay accepted")
			}
			if tx.claims != 1 {
				t.Fatalf("replay called native hook again: %d", tx.claims)
			}
		})
	}
}
