export type RunMode = 'live' | 'overnight'
export type Pipeline = 'lite' | 'deep'

export interface StageArtifact {
  model: string
  prompt: string
  response_text: string
  response_json?: unknown
  usage?: unknown
  cost_estimate_usd?: number | null
  latency_ms?: number | null
  error?: string | null
}

export interface Stage {
  stage_name: string
  status: string
  artifacts: StageArtifact[]
}

export interface RunSummary {
  run_id: string
  created_at: string
  status: string
  pipeline: Pipeline
  mode: RunMode
  topic_prompt: string
}

export interface RunCreate {
  prompt: string
  pipeline: Pipeline
  mode: RunMode
}

export interface Template {
  id: string
  title: string
  prompt: string
}

export interface Project {
  id: string
  name: string
  description: string
  active: boolean
}

export interface Topic {
  slot: string
  category: string
  title: string
  why_it_matters: string
  launch_prompt: string
  suggested_depth: string
  falsifiers: string[]
}

export interface WeeklyTopicBatch {
  batch_id: string
  topics: Topic[]
}
