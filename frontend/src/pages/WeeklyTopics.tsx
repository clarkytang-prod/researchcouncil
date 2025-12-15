import React, { useEffect, useState } from 'react'
import { fetchCurrentTopics, refreshTopics, selectTopic } from '../api'
import { WeeklyTopicBatch } from '../types'

const WeeklyTopics: React.FC = () => {
  const [batch, setBatch] = useState<WeeklyTopicBatch | null>(null)
  const load = async () => {
    const data = await fetchCurrentTopics()
    setBatch(data)
  }

  useEffect(() => {
    load()
  }, [])

  if (!batch) return null

  return (
    <section>
      <h2>Weekly Topics</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '12px' }}>
        {batch.topics.map((topic) => (
          <div key={topic.slot} style={{ border: '1px solid #ccc', padding: '8px', borderRadius: '8px' }}>
            <h3>{topic.title}</h3>
            <p><em>{topic.category}</em></p>
            <p>{topic.why_it_matters}</p>
            <button onClick={async () => { await selectTopic(topic.slot); load() }}>Run Council</button>
          </div>
        ))}
      </div>
      <button style={{ marginTop: '8px' }} onClick={async () => setBatch(await refreshTopics())}>Refresh topics</button>
    </section>
  )
}

export default WeeklyTopics
