import React from 'react'
import { StageArtifact } from '../types'

const ModelTabs: React.FC<{ artifacts: StageArtifact[] }> = ({ artifacts }) => {
  return (
    <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
      {artifacts.map((artifact) => (
        <div key={artifact.model} style={{ border: '1px solid #eee', padding: '8px', borderRadius: '8px', minWidth: '220px' }}>
          <strong>{artifact.model}</strong>
          <pre style={{ whiteSpace: 'pre-wrap', maxHeight: '300px', overflow: 'auto' }}>{artifact.response_text}</pre>
        </div>
      ))}
    </div>
  )
}

export default ModelTabs
