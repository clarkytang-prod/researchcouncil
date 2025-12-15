import React, { useState } from 'react'
import { createRun } from '../api'

const NewRun: React.FC = () => {
  const [prompt, setPrompt] = useState('')
  const [mode, setMode] = useState<'live' | 'overnight'>('live')
  const [pipeline, setPipeline] = useState<'lite' | 'deep'>('lite')
  const [created, setCreated] = useState<string | null>(null)

  const submit = async () => {
    const res = await createRun({ prompt, mode, pipeline })
    setCreated(res.run_id)
  }

  return (
    <section>
      <h2>New Run</h2>
      <textarea value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="Prompt" style={{ width: '100%', minHeight: '80px' }} />
      <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }}>
        <label>
          Pipeline:
          <select value={pipeline} onChange={(e) => setPipeline(e.target.value as 'lite' | 'deep')}>
            <option value="lite">Council Lite</option>
            <option value="deep">Council Deep (stub)</option>
          </select>
        </label>
        <label>
          Mode:
          <select value={mode} onChange={(e) => setMode(e.target.value as 'live' | 'overnight')}>
            <option value="live">Live</option>
            <option value="overnight">Overnight</option>
          </select>
        </label>
        <button onClick={submit}>Run Council</button>
      </div>
      {created && <p>Created run: {created}</p>}
    </section>
  )
}

export default NewRun
