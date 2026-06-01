/** Hero line synced to orchestration graphic mode buttons. */
export const ORCHESTRATION_STORY_LINES = {
  smart:
    "One interface, many gateways—intelligent routing picks the best provider per transaction.",
  failover:
    "Built-in failover and health checks keep payments running when a provider drops.",
  balance:
    "Spread volume by success rate, cost, and SLA—not one fixed route for everything.",
};

export function orchestrationStoryLineFor(id) {
  return ORCHESTRATION_STORY_LINES[id] || ORCHESTRATION_STORY_LINES.smart;
}
