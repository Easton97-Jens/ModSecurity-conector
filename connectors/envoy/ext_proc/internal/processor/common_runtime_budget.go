//go:build libmodsecurity

package processor

// Phase4BodyBudgetDisabled reports whether the legacy connector-owned
// cumulative response-inspection budget is disabled for the loaded Common
// Runtime mode. All valid Phase-4 modes delegate WAF inspection limits to
// libModSecurity. A missing engine or unknown mode stays conservative.
// Independent gRPC message/chunk and allocation limits remain unchanged.
func (engine *CommonRuntimeEngine) Phase4BodyBudgetDisabled() bool {
	if engine == nil {
		return false
	}
	switch engine.phase4Mode {
	case commonRuntimePhase4ModeOff, 1, 2:
		return true
	default:
		return false
	}
}
