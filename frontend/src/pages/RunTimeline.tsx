import React, { useEffect, useState } from 'react'
import { fetchRuns } from '../api'
import { RunSummary } from '../types'

const RunTimeline: React.FC = () => {
  const [runs, setRuns] = useState<RunSummary[]>([])

  useEffect(() => {
    fetchRuns().then(setRuns)
  }, [])

  return (
    <section>
      <h2>Recent runs</h2>
      <ul>
        {runs.map((run) => (
          <li key={run.run_id}>
            {run.run_id} · {run.pipeline} · {run.status}
            <div style={{ fontSize: '0.9em', color: '#555' }}>{run.topic_prompt}</div>
          </li>
        ))}
      </ul>
    </section>
  )
}

export default RunTimeline
