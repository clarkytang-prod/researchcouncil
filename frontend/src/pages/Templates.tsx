import React, { useEffect, useState } from 'react'
import { createTemplate, fetchTemplates } from '../api'
import { Template } from '../types'

const Templates: React.FC = () => {
  const [templates, setTemplates] = useState<Template[]>([])
  const [title, setTitle] = useState('')
  const [prompt, setPrompt] = useState('')

  const reload = async () => {
    const res = await fetchTemplates()
    setTemplates(res)
  }

  useEffect(() => {
    reload()
  }, [])

  const submit = async () => {
    await createTemplate({ title, prompt })
    setTitle('')
    setPrompt('')
    reload()
  }

  return (
    <section>
      <h2>Templates</h2>
      <div style={{ display: 'flex', gap: '8px', marginBottom: '8px' }}>
        <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Title" />
        <input value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="Prompt" />
        <button onClick={submit}>Add</button>
      </div>
      <ul>
        {templates.map((t) => (
          <li key={t.id}>
            <strong>{t.title}</strong>: {t.prompt}
          </li>
        ))}
      </ul>
    </section>
  )
}

export default Templates
