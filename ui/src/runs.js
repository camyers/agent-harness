export function parseRuns(text) {
  const runs = new Map()
  for (const line of text.split('\n')) {
    if (!line.trim()) continue
    let event
    try {
      event = JSON.parse(line)
    } catch {
      continue
    }
    if (!runs.has(event.run_id)) runs.set(event.run_id, { id: event.run_id, events: [] })
    runs.get(event.run_id).events.push(event)
  }
  return [...runs.values()].map(summarize).reverse()
}

function summarize(run) {
  const usage = run.events.filter((e) => e.event === 'usage')
  const calls = run.events.filter((e) => e.event === 'tool_call')
  const task = run.events.find((e) => e.event === 'task')
  const end = run.events.find((e) => e.event === 'answer' || e.event === 'stopped')
  return {
    ...run,
    task: task ? task.task : '(no task logged)',
    model: usage.find((e) => e.model)?.model ?? 'not logged',
    tokens: usage.reduce((sum, e) => sum + e.prompt_tokens + e.completion_tokens, 0),
    latencyMs: usage.reduce((sum, e) => sum + e.latency_ms, 0),
    toolCalls: calls.length,
    problems: calls.filter((e) => e.outcome !== 'ok').length,
    status: end ? end.event : 'unfinished',
  }
}