import { useEffect, useState } from 'react'
import { parseRuns } from './runs'
import Timeline from './Timeline'

const REFRESH_MS = 2000

export default function App() {
  const [runs, setRuns] = useState([])
  const [selectedId, setSelectedId] = useState(null)
  const [filter, setFilter] = useState('')

  useEffect(() => {
    async function load() {
      const response = await fetch('/runs.jsonl')
      setRuns(parseRuns(await response.text()))
    }
    load()
    const timer = setInterval(load, REFRESH_MS)
    return () => clearInterval(timer)
  }, [])

  const visible = runs.filter((run) => run.task.toLowerCase().includes(filter.toLowerCase()))
  const selected = runs.find((run) => run.id === selectedId) ?? visible[0]

  return (
    <div className="app">
      <aside className="sidebar">
        <h1>Runs</h1>
        <input placeholder="Filter by task" value={filter} onChange={(e) => setFilter(e.target.value)} />
        {visible.length === 0 && <p className="muted">No runs to show.</p>}
        {visible.map((run) => (
          <button
            key={run.id}
            className={run === selected ? 'run active' : 'run'}
            onClick={() => setSelectedId(run.id)}
          >
            <span>{run.task}</span>
            <span className="muted">
              {run.id} · {run.status}
            </span>
          </button>
        ))}
      </aside>
      <main>{selected && <Timeline run={selected} />}</main>
    </div>
  )
}