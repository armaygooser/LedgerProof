import {
  CheckCircleFilled,
  ClockCircleOutlined,
  FileProtectOutlined,
  SafetyCertificateFilled,
  StopOutlined,
} from '@ant-design/icons'
import { Tag, Tooltip } from 'antd'
import type { AgentRun } from '../types'
import { shortHash } from '../utils/format'

function statusIcon(status: AgentRun['status']) {
  if (status === 'verified') return <SafetyCertificateFilled />
  if (status === 'complete') return <CheckCircleFilled />
  if (status === 'invalidated') return <StopOutlined />
  return <ClockCircleOutlined />
}

export function AgentActivity({ agents }: { agents: AgentRun[] }) {
  return (
    <section className="panel agent-panel">
      <div className="panel-header">
        <div>
          <span className="panel-kicker">SEGREGATED AGENT TEAM</span>
          <h2>七 Agent 审计工作区</h2>
        </div>
        <Tag color="blue">最小权限</Tag>
      </div>
      <div className="agent-list">
        {agents.map((agent) => (
          <article className={`agent-card agent-${agent.status}`} key={agent.agent_id}>
            <div className="agent-sequence">{String(agent.sequence).padStart(2, '0')}</div>
            <div className="agent-status-icon">{statusIcon(agent.status)}</div>
            <div className="agent-content">
              <div className="agent-title-row">
                <strong>{agent.name}</strong>
                <span>{agent.tool}</span>
              </div>
              <p>{agent.summary}</p>
              <div className="agent-meta">
                <Tooltip title={agent.permission}>
                  <span><FileProtectOutlined /> {agent.permission}</span>
                </Tooltip>
                {agent.output_sha256 && <code>SHA {shortHash(agent.output_sha256)}</code>}
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}
