import { RunCreate, RunSummary, Template, Project, WeeklyTopicBatch } from './types'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request(path: string, options?: RequestInit) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export const createRun = (payload: RunCreate) => request('/api/runs', { method: 'POST', body: JSON.stringify(payload) })
export const fetchRuns = (): Promise<RunSummary[]> => request('/api/runs')
export const fetchTemplates = (): Promise<Template[]> => request('/api/templates')
export const createTemplate = (payload: { title: string; prompt: string }) =>
  request('/api/templates', { method: 'POST', body: JSON.stringify(payload) })
export const fetchProjects = (): Promise<Project[]> => request('/api/projects')
export const createProject = (payload: { name: string; description: string; active: boolean }) =>
  request('/api/projects', { method: 'POST', body: JSON.stringify(payload) })
export const fetchCurrentTopics = (): Promise<WeeklyTopicBatch> => request('/api/topics/current')
export const selectTopic = (slot: string) => request(`/api/topics/${slot}/select`, { method: 'POST' })
export const refreshTopics = () => request('/api/topics/refresh', { method: 'POST' })
