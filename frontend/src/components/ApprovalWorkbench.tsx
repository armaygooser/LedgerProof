import {
  CheckCircleFilled,
  ExclamationCircleFilled,
  PlayCircleOutlined,
  ReloadOutlined,
  RollbackOutlined,
  SafetyCertificateOutlined,
} from '@ant-design/icons'
import { Button, Divider, Progress, Tag } from 'antd'
import type { DemoState } from '../types'
import { money, phaseLabel, shortHash } from '../utils/format'

interface Props {
  state: DemoState
  busy: boolean
  onRun: () => void
  onApprove: () => void
  onExecute: () => void
  onVerify: () => void
  onRollback: () => void
  onReset: () => void
}

export function ApprovalWorkbench({
  state,
  busy,
  onRun,
  onApprove,
  onExecute,
  onVerify,
  onRollback,
  onReset,
}: Props) {
  const proposal = state.proposal
  const approval = state.approval
  return (
    <aside className="approval-column">
      <section className={`approval-card phase-${state.phase}`}>
        <div className="approval-head">
          <div>
            <span className="panel-kicker">HUMAN DECISION GATE</span>
            <h2>人工审批工作台</h2>
          </div>
          <Tag color={state.phase === 'awaiting_approval' ? 'orange' : state.phase === 'verified' ? 'green' : 'blue'}>
            {phaseLabel(state.phase)}
          </Tag>
        </div>

        {!proposal ? (
          <div className="approval-empty">
            <ExclamationCircleFilled />
            <strong>高风险付款等待调查</strong>
            <p>七个 Agent 将封存证据、核对交易、识别异常并形成最小影响处置提案。</p>
            <Button type="primary" size="large" block icon={<PlayCircleOutlined />} loading={busy} onClick={onRun}>
              一键审计至审批
            </Button>
          </div>
        ) : (
          <>
            <div className="proposal-action">
              <span>建议动作</span>
              <strong>暂停异常付款</strong>
              <small>{String(proposal.action)}</small>
            </div>
            <dl className="proposal-facts">
              <div><dt>目标批次</dt><dd>{String(proposal.target)}</dd></div>
              <div><dt>影响范围</dt><dd>{proposal.transaction_ids?.length ?? 0} / {state.population_count} 笔</dd></div>
              <div><dt>影响金额</dt><dd className="risk-text">{money(Number(proposal.affected_amount))}</dd></div>
              <div><dt>风险等级</dt><dd><Tag color="red">L2 · HIGH</Tag></dd></div>
              <div><dt>证据覆盖</dt><dd>{state.evidence_coverage.toFixed(0)}%</dd></div>
            </dl>
            <Divider />
            <div className="proposal-hash">
              <span>提案记录 SHA-256</span>
              <code>{shortHash(String(proposal.record_sha256), 12, 10)}</code>
              <small>批准只对当前哈希对应的提案有效</small>
            </div>
            {state.phase === 'awaiting_approval' && (
              <Button type="primary" danger size="large" block loading={busy} onClick={onApprove}>
                人工批准止付
              </Button>
            )}
            {state.phase === 'approved' && (
              <Button type="primary" size="large" block icon={<PlayCircleOutlined />} loading={busy} onClick={onExecute}>
                执行受控止付
              </Button>
            )}
            {state.phase === 'executed' && (
              <Button type="primary" size="large" block icon={<SafetyCertificateOutlined />} loading={busy} onClick={onVerify}>
                启动独立复核
              </Button>
            )}
            {state.phase === 'verified' && (
              <div className="verified-block">
                <CheckCircleFilled />
                <strong>独立复核通过</strong>
                <p>止付范围、金额、证据根和 CyberGuard 审计链均已重新验证。</p>
                <Button danger block icon={<RollbackOutlined />} loading={busy} onClick={onRollback}>
                  发起受控回滚
                </Button>
              </div>
            )}
            {state.phase === 'rolled_back' && (
              <div className="rollback-block">
                <RollbackOutlined />
                <strong>付款止付已释放</strong>
                <p>原 VERIFIED 结论已失效；审计链保留全部执行与回滚记录。</p>
                <Button block icon={<ReloadOutlined />} loading={busy} onClick={onReset}>重置演示案件</Button>
              </div>
            )}
          </>
        )}
      </section>

      <section className="runtime-card">
        <div className="runtime-title">
          <span>GOVERNANCE RUNTIME</span>
          <Tag color={state.governance.connected ? 'green' : 'red'}>{state.governance.connected ? 'ONLINE' : 'OFFLINE'}</Tag>
        </div>
        <strong>CyberGuard Executor</strong>
        <code>{state.governance.image}</code>
        <div className="runtime-row"><span>Service</span><b>{state.governance.service}</b></div>
        <div className="runtime-row"><span>Mode</span><b>{state.governance.mode}</b></div>
        <div className="runtime-row"><span>Audit</span><b className={state.governance.audit_valid ? 'ok' : 'bad'}>{state.governance.audit_valid ? 'VALID' : 'UNAVAILABLE'}</b></div>
        <Progress percent={state.governance.connected ? 100 : 15} showInfo={false} strokeColor={state.governance.connected ? '#168f67' : '#d9363e'} />
        {state.governance.error && <p className="runtime-error">{state.governance.error}</p>}
      </section>
    </aside>
  )
}
