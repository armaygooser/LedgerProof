import type { ReactNode } from 'react'

interface Props {
  label: string
  value: string
  note: string
  icon: ReactNode
  tone?: 'blue' | 'red' | 'amber' | 'green' | 'purple'
}

export function MetricCard({ label, value, note, icon, tone = 'blue' }: Props) {
  return (
    <div className={`metric-card metric-${tone}`}>
      <div className="metric-icon">{icon}</div>
      <div className="metric-copy">
        <span>{label}</span>
        <strong>{value}</strong>
        <small>{note}</small>
      </div>
    </div>
  )
}
