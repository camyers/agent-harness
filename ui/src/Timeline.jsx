export default function Timeline({ run }) {
  return (
    <section>
      <h2>{run.task}</h2>
      <div className="summary">
        <Stat label="Model" value={run.model} />
        <Stat label="Tokens" value={run.tokens.toLocaleString()} />
        <Stat label="Time waiting on the model" value={`${run.latencyMs.toLocaleString()} ms`} />
        <Stat label="Tool calls" value={run.toolCalls} />
        <Stat label="Blocked, denied or failed" value={run.problems} />
      </div>
      <ol className="timeline">
        {run.events.map((event, index) => (
          <Event key={index} event={event} />
        ))}
      </ol>
    </section>
  )
}

function Stat({ label, value }) {
  return (
    <div className="stat">
      <span className="muted">{label}</span>
      <strong>{value}</strong>
    </div>
  )
}

function Event({ event }) {
  const time = event.timestamp.slice(11)

  if (event.event === 'task') {
    return (
      <Row time={time} kind="task" title="Task">
        {event.task}
      </Row>
    )
  }
  if (event.event === 'usage') {
    return (
      <Row time={time} kind="usage" title={`Step ${event.step}: the model replied`}>
        {event.prompt_tokens} tokens in, {event.completion_tokens} out, {event.latency_ms} ms
      </Row>
    )
  }
  if (event.event === 'tool_call') {
    return (
      <Row time={time} kind={event.outcome} title={`${event.tool} → ${event.outcome}`}>
        <code>{JSON.stringify(event.args)}</code>
        <details>
          <summary>Result</summary>
          <pre>{event.result}</pre>
        </details>
      </Row>
    )
  }
  if (event.event === 'answer') {
    return (
      <Row time={time} kind="answer" title="Answer">
        <pre>{event.content}</pre>
      </Row>
    )
  }
  if (event.event === 'stopped') {
    return (
      <Row time={time} kind="stopped" title="Stopped">
        {event.reason}
      </Row>
    )
  }
  if (event.event === 'context') {
    return (
      <Row time={time} kind="task" title="Test output given to the model">
        <details>
          <summary>Show log</summary>
          <pre>{event.text}</pre>
        </details>
      </Row>
    )
  }
  if (event.event === 'rejected') {
    return (
      <Row time={time} kind="blocked" title={`Step ${event.step}: tool call rejected by the provider`}>
        <code>{event.generation}</code>
      </Row>
    )
  }
  if (event.event === 'verify') {
    return (
      <Row time={time} kind={event.passed ? 'ok' : 'error'} title={event.passed ? 'Tests pass' : 'Tests still fail'}>
        <details>
          <summary>Test output</summary>
          <pre>{event.output}</pre>
        </details>
      </Row>
    )
  }
  return (
    <Row time={time} kind="other" title={event.event}>
      <pre>{JSON.stringify(event, null, 2)}</pre>
    </Row>
  )
}

function Row({ time, kind, title, children }) {
  return (
    <li className={`event ${kind}`}>
      <div className="event-head">
        <strong>{title}</strong>
        <span className="muted">{time}</span>
      </div>
      <div className="event-body">{children}</div>
    </li>
  )
}