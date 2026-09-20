//go:build libmodsecurity

package processor

// Phase4BodyBudgetDisabled reports only the immutable mode loaded at engine
// creation. Neither a missing engine nor an unknown mode disables the budget.
// Independent gRPC message/chunk and allocation limits remain unchanged.
func (engine *CommonRuntimeEngine) Phase4BodyBudgetDisabled() bool {
	return engine != nil && engine.phase4Mode == commonRuntimePhase4ModeOff
}
