import React from 'react'
import { StageArtifact } from '../types'

const AuditDrawer: React.FC<{ artifact: StageArtifact }> = ({ artifact }) => {
  return (
    <details>
      <summary>Audit</summary>
      <p>Prompt</p>
      <pre style={{ whiteSpace: 'pre-wrap' }}>{artifact.prompt}</pre>
      <p>Raw JSON</p>
      <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(artifact.response_json, null, 2)}</pre>
      <p>Usage</p>
      <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(artifact.usage, null, 2)}</pre>
    </details>
  )
}

export default AuditDrawer
