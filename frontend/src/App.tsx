import { useEffect, useMemo, useState } from 'react'
import {
  ApiOutlined,
  AuditOutlined,
  BankOutlined,
  BellOutlined,
  CheckCircleFilled,
  DatabaseOutlined,
  FileProtectOutlined,
  LinkOutlined,
  MenuFoldOutlined,
  ReloadOutlined,
  SafetyCertificateOutlined,
  SettingOutlined,
  TeamOutlined,
  TransactionOutlined,
  UserOutlined,
  WarningFilled,
} from '@ant-design/icons'
import { Alert, Avatar, Button, Input, Modal, Progress, Skeleton, Tag, message } from 'antd'
import { loadDemo, mutateDemo } from './api'
import { AgentActivity } from './components/AgentActivity'
import { ApprovalWorkbench } from './components/ApprovalWorkbench'
import { EvidenceChain } from './components/EvidenceChain'
import { MetricCard } from './components/MetricCard'
import { RiskAnalytics } from './components/RiskAnalytics'
import { TransactionTable } from './components/TransactionTable'
import type { DemoState } from './types'
import { money, phaseLabel, shortHash } from './utils/format'

const phases = [
  ['detected', '异常发现'],
  ['findings_ready', '调查完成'],
  ['awaiting_approval', '人工审批'],
  ['executed', '受控执行'],
  ['verified', '独立复核'],
  ['rolled_back', '回滚'],
]

const phaseOrder: Record<string, number> = {
  detected: 0,
  investigating: 1,
  findings_ready: 1,
  awaiting_approval: 2,
  approved: 2,
  executed: 3,
  verified: 4,
  rolled_back: 5,
}

function App() {
  const [state, setState] = useState<DemoState | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [approvalOpen, setApprovalOpen] = useState(false)
  const [rollbackOpen, setRollbackOpen] = useState(false)
  const [approver, setApprover] = useState('财务总监 林岚')
  const [rollbackReason, setRollbackReason] = useState('人工复核后解除临时止付，恢复正常付款流程')
  const [messageApi, contextHolder] = message.useMessage()

  const refresh = async () => {
    try {
      setState(await loadDemo())
      setError(null)
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : String(cause))
    }
  }

  useEffect(() => {
    void refresh()
  }, [])

  const act = async (path: string, body?: object, success?: string) => {
    setBusy(true)
    try {
      const next = await mutateDemo(path, body)
      setState(next)
      setError(null)
      if (success) messageApi.success(success)
      return true
    } catch (cause) {
      const text = cause instanceof Error ? cause.message : String(cause)
      setError(text)
      messageApi.error(text)
      return false
    } finally {
      setBusy(false)
    }
  }

  const riskRate = useMemo(() => {
    if (!state) return 0
    return Number(((state.high_risk_count / state.population_count) * 100).toFixed(2))
  }, [state])

  if (!state) {
    return (
      <div className="loading-screen">
        <div className="loading-brand"><BankOutlined /><strong>LedgerProof</strong></div>
        <Skeleton active paragraph={{ rows: 8 }} />
        {error && <Alert type="error" message="无法连接财证中枢" description={error} showIcon />}
      </div>
    )
  }

  const currentPhase = phaseOrder[state.phase] ?? 0

  return (
    <div className="app-shell">
      {contextHolder}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark"><BankOutlined /></div>
          <div><strong>LedgerProof</strong><span>财证中枢</span></div>
        </div>
        <nav>
          <button className="nav-item active"><AuditOutlined /><span>审计总览</span></button>
          <button className="nav-item"><WarningFilled /><span>风险案件</span><b>1</b></button>
          <button className="nav-item"><TransactionOutlined /><span>交易分析</span></button>
          <button className="nav-item"><FileProtectOutlined /><span>证据工作底稿</span></button>
          <button className="nav-item"><TeamOutlined /><span>Agent 团队</span></button>
          <button className="nav-item"><LinkOutlined /><span>决策审计链</span></button>
        </nav>
        <div className="sidebar-bottom">
          <button className="nav-item"><SettingOutlined /><span>系统设置</span></button>
          <div className="foundation-badge">
            <SafetyCertificateOutlined />
            <div><small>POWERED BY</small><strong>CyberGuard</strong></div>
          </div>
        </div>
      </aside>

      <main className="main-shell">
        <header className="topbar">
          <div className="topbar-left">
            <Button type="text" icon={<MenuFoldOutlined />} />
            <span className="breadcrumb">审计项目 / {state.case_id}</span>
          </div>
          <div className="topbar-right">
            <div className={`connection-pill ${state.governance.connected ? 'connected' : 'offline'}`}>
              <i /> {state.governance.connected ? 'CyberGuard 在线' : 'CyberGuard 离线'}
            </div>
            <Button type="text" icon={<BellOutlined />} />
            <div className="user-block"><Avatar icon={<UserOutlined />} /><div><strong>林岚</strong><span>财务总监 · 审批人</span></div></div>
          </div>
        </header>

        <div className="content">
          {error && (
            <Alert
              className="global-alert"
              type="error"
              showIcon
              closable
              message="治理服务调用失败"
              description={error}
              action={<Button size="small" icon={<ReloadOutlined />} onClick={() => void refresh()}>重试</Button>}
            />
          )}

          <section className="engagement-header">
            <div>
              <div className="engagement-eyebrow"><span>ACTIVE ENGAGEMENT</span><Tag color="red">重大风险</Tag></div>
              <h1>{state.title}</h1>
              <p>{state.company} · {state.period} · 重要性水平 {money(state.materiality)}</p>
            </div>
            <div className="engagement-status">
              <span>当前阶段</span>
              <strong>{phaseLabel(state.phase)}</strong>
              <small>CASE {state.case_id}</small>
            </div>
          </section>

          <section className="phase-rail">
            {phases.map(([key, label], index) => (
              <div className={`phase-step ${index <= currentPhase ? 'reached' : ''} ${index === currentPhase ? 'current' : ''}`} key={key}>
                <div>{index < currentPhase ? <CheckCircleFilled /> : String(index + 1).padStart(2, '0')}</div>
                <span>{label}</span>
              </div>
            ))}
            <Progress percent={(currentPhase / (phases.length - 1)) * 100} showInfo={false} strokeColor="#246bfd" trailColor="#e6eaf0" />
          </section>

          <section className="metric-grid">
            <MetricCard label="审计交易总体" value={money(state.total_amount)} note={`${state.population_count.toLocaleString('zh-CN')} 笔全量分析`} icon={<DatabaseOutlined />} />
            <MetricCard label="高风险金额" value={money(state.high_risk_amount)} note={`${state.high_risk_count} 笔 · ${riskRate}% 人口占比`} icon={<WarningFilled />} tone="red" />
            <MetricCard label="待人工审批" value={state.phase === 'awaiting_approval' ? '1' : '0'} note="L2 高风险处置" icon={<UserOutlined />} tone="amber" />
            <MetricCard label="证据覆盖率" value={`${state.evidence_coverage.toFixed(0)}%`} note={`${state.evidence.length} 组 Evidence ID`} icon={<FileProtectOutlined />} tone="green" />
            <MetricCard label="审计链状态" value={state.governance.audit_valid ? 'VALID' : 'OFFLINE'} note={`Head ${shortHash(state.governance.audit_head)}`} icon={<ApiOutlined />} tone="purple" />
          </section>

          <div className="workspace-grid">
            <div className="primary-column">
              <RiskAnalytics state={state} />
              <AgentActivity agents={state.agents} />
            </div>
            <ApprovalWorkbench
              state={state}
              busy={busy}
              onRun={() => void act('run-to-approval', undefined, '七 Agent 调查完成，止付提案已进入人工审批')}
              onApprove={() => setApprovalOpen(true)}
              onExecute={() => void act('execute', undefined, 'CyberGuard 已执行受控止付')}
              onVerify={() => void act('verify', undefined, '独立复核通过')}
              onRollback={() => setRollbackOpen(true)}
              onReset={() => void act('reset', undefined, '演示案件已重置')}
            />
          </div>

          <TransactionTable transactions={state.transactions} />
          <EvidenceChain events={state.audit_events} governance={state.governance} />
        </div>
      </main>

      <Modal
        title="人工批准止付"
        open={approvalOpen}
        okText="确认批准当前提案"
        cancelText="返回检查"
        confirmLoading={busy}
        onCancel={() => setApprovalOpen(false)}
        onOk={async () => {
          const ok = await act('approve', { approver }, '人工批准已与提案哈希绑定')
          if (ok) setApprovalOpen(false)
        }}
      >
        <div className="decision-modal">
          <Alert type="warning" showIcon message="本次批准只对当前提案哈希有效" description={`Proposal SHA-256: ${state.proposal?.record_sha256 ?? '—'}`} />
          <label>审批人</label>
          <Input value={approver} onChange={(event) => setApprover(event.target.value)} />
          <dl>
            <div><dt>动作</dt><dd>暂停异常付款</dd></div>
            <div><dt>范围</dt><dd>3 / {state.population_count} 笔</dd></div>
            <div><dt>金额</dt><dd>{money(294000)}</dd></div>
            <div><dt>有效期</dt><dd>15 分钟</dd></div>
          </dl>
        </div>
      </Modal>

      <Modal
        title="发起受控回滚"
        open={rollbackOpen}
        okText="确认释放付款止付"
        okButtonProps={{ danger: true }}
        cancelText="取消"
        confirmLoading={busy}
        onCancel={() => setRollbackOpen(false)}
        onOk={async () => {
          const ok = await act('rollback', { approver, reason: rollbackReason }, '止付已回滚，原复核结论失效')
          if (ok) setRollbackOpen(false)
        }}
      >
        <div className="decision-modal">
          <Alert type="error" showIcon message="回滚会使当前 VERIFIED 结论失效" description={`执行记录将绑定到回滚审计节点，历史记录不会被删除。`} />
          <label>回滚批准人</label>
          <Input value={approver} onChange={(event) => setApprover(event.target.value)} />
          <label>回滚理由</label>
          <Input.TextArea rows={3} value={rollbackReason} onChange={(event) => setRollbackReason(event.target.value)} />
        </div>
      </Modal>
    </div>
  )
}

export default App
