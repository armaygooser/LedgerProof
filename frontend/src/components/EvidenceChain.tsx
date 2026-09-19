import {
  CheckCircleFilled,
  ClockCircleOutlined,
  CopyOutlined,
  LinkOutlined,
  RollbackOutlined,
  SafetyCertificateOutlined,
} from '@ant-design/icons'
import { Button, Empty, Tag, Timeline, Tooltip, message } from 'antd'
import type { AuditEvent, GovernanceStatus } from '../types'
import { shortHash } from '../utils/format'

const labels: Record<string, string> = {
  pending_approval: '动作提案',
  approved: '人工批准',
  executed: '核心执行记录',
  domain_executed: '付款止付回执',
  verification_recorded: '独立复核',
  rolled_back: '核心回滚记录',
  domain_rolled_back: '付款释放回执',
}

function eventIcon(event: AuditEvent) {
  if (event.status.includes('rolled_back')) return <RollbackOutlined />
  if (event.status === 'verification_recorded') return <SafetyCertificateOutlined />
  if (event.status === 'pending_approval') return <ClockCircleOutlined />
  return <CheckCircleFilled />
}

export function EvidenceChain({ events, governance }: { events: AuditEvent[]; governance: GovernanceStatus }) {
  const [messageApi, contextHolder] = message.useMessage()
  const copy = async (value: string) => {
    await navigator.clipboard.writeText(value)
    messageApi.success('完整哈希已复制')
  }

  return (
    <section className="panel chain-panel">
      {contextHolder}
      <div className="panel-header">
        <div>
          <span className="panel-kicker">CYBERGUARD AUDIT LEDGER</span>
          <h2>哈希证据链</h2>
        </div>
        <div className="chain-summary">
          <Tag color={governance.audit_valid ? 'green' : 'red'} icon={<LinkOutlined />}>
            {governance.audit_valid ? '链完整' : '链未验证'}
          </Tag>
          <span>{governance.audit_records} 条全局记录</span>
        </div>
      </div>
      {events.length === 0 ? (
        <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} description="完成调查并形成提案后生成审计链" />
      ) : (
        <Timeline
          className="hash-timeline"
          items={events.map((event) => ({
            dot: eventIcon(event),
            color: event.status.includes('rolled_back') ? 'red' : event.status === 'verification_recorded' ? 'green' : 'blue',
            children: (
              <div className="hash-event">
                <div className="hash-event-title">
                  <strong>{labels[event.status] ?? event.status}</strong>
                  <time>{new Date(event.recorded_at).toLocaleTimeString('zh-CN', { hour12: false })}</time>
                </div>
                <div className="hash-line">
                  <span>Record</span>
                  <code>{shortHash(event.record_sha256, 10, 8)}</code>
                  <Tooltip title="复制完整哈希">
                    <Button type="text" size="small" icon={<CopyOutlined />} onClick={() => copy(event.record_sha256)} />
                  </Tooltip>
                </div>
                <div className="hash-line muted">
                  <span>Previous</span>
                  <code>{shortHash(event.previous_record_sha256, 10, 8)}</code>
                </div>
                {Boolean(event.detail.result) && <p className="event-result">{String(event.detail.result)}</p>}
              </div>
            ),
          }))}
        />
      )}
      <div className="chain-head">
        <span>当前链头</span>
        <code>{shortHash(governance.audit_head, 14, 12)}</code>
      </div>
    </section>
  )
}
