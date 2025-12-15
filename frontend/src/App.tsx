import React from 'react'
import Dashboard from './pages/Dashboard'
import NewRun from './pages/NewRun'
import Templates from './pages/Templates'
import Projects from './pages/Projects'
import WeeklyTopics from './pages/WeeklyTopics'
import RunTimeline from './pages/RunTimeline'

const App: React.FC = () => {
  return (
    <div style={{ fontFamily: 'Inter, sans-serif', padding: '16px', display: 'grid', gap: '16px' }}>
      <header>
        <h1>CouncilLab</h1>
        <p>Local-first council research sandbox.</p>
      </header>
      <Dashboard />
      <WeeklyTopics />
      <NewRun />
      <RunTimeline />
      <Templates />
      <Projects />
    </div>
  )
}

export default App
