import React, { useEffect, useState } from 'react'
import { createProject, fetchProjects } from '../api'
import { Project } from '../types'

const Projects: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([])
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')

  const reload = async () => {
    const res = await fetchProjects()
    setProjects(res)
  }

  useEffect(() => {
    reload()
  }, [])

  const submit = async () => {
    await createProject({ name, description, active: true })
    setName('')
    setDescription('')
    reload()
  }

  return (
    <section>
      <h2>Projects</h2>
      <div style={{ display: 'flex', gap: '8px', marginBottom: '8px' }}>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" />
        <input value={description} onChange={(e) => setDescription(e.target.value)} placeholder="Description" />
        <button onClick={submit}>Add</button>
      </div>
      <ul>
        {projects.map((p) => (
          <li key={p.id}>
            <strong>{p.name}</strong> ({p.active ? 'active' : 'inactive'}) — {p.description}
          </li>
        ))}
      </ul>
    </section>
  )
}

export default Projects
