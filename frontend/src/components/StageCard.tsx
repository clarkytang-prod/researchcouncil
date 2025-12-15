import React from 'react'
import { Stage } from '../types'

const StageCard: React.FC<{ stage: Stage }> = ({ stage }) => {
  return (
    <div style={{ border: '1px solid #ddd', padding: '8px', borderRadius: '8px' }}>
      <strong>{stage.stage_name}</strong>
      <p>Status: {stage.status}</p>
      <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(stage.artifacts, null, 2)}</pre>
    </div>
  )
}

export default StageCard
