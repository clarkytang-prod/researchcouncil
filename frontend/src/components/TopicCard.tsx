import React from 'react'
import { Topic } from '../types'

const TopicCard: React.FC<{ topic: Topic; onSelect?: () => void }> = ({ topic, onSelect }) => {
  return (
    <div style={{ border: '1px solid #e3e3e3', padding: '8px', borderRadius: '8px' }}>
      <strong>{topic.title}</strong>
      <p>{topic.why_it_matters}</p>
      {onSelect && <button onClick={onSelect}>Run</button>}
    </div>
  )
}

export default TopicCard
