export type Phase =
  | 'detected'
  | 'investigating'
  | 'findings_ready'
  | 'awaiting_approval'
  | 'approved'
  | 'executed'
  | 'verified'
  | 'rolled_back'

export interface Transaction {
  transaction_id: string
  invoice_id: string
  vendor_id: string
  vendor_name: string
  amount: number
  currency: string
  submitted_at: string
  approver: string
  payment_account: string
  risk_score: number
  risk_level: 'high' | 'medium' | 'low'
  triggers: string[]
}

export interface EvidenceRecord {
  evidence_id: string
  kind: string
  label: string
  source: string
  sha256: string
  integrity: 'verified'
}

export interface Finding {
  finding_id: string
  agent_id: string
  title: string
  summary: string
  severity: 'critical' | 'high' | 'medium' | 'info'
  evidence_ids: string[]
  control_points: string[]
  output_sha256: string
}

export interface AgentRun {
  agent_id: string
  sequence: number
  name: string
  role: string
  status: 'pending' | 'running' | 'complete' | 'verified' | 'invalidated'
  permission: string
  started_at: string | null
  completed_at: string | null
  summary: string
  tool: string
  input_evidence_ids: string[]
  output_sha256: string | null
}

export interface GovernanceStatus {
  connected: boolean
  image: string
  service: string
  mode: string
  audit_valid: boolean
  audit_records: number
  audit_head: string | null
  error: string | null
}

export interface AuditEvent {
  status: string
  record_sha256: string
  previous_record_sha256: string | null
  record_hmac_sha256: string | null
  recorded_at: string
  action_id: string | null
  proposal_record_sha256: string | null
  approval_record_sha256: string | null
  execution_record_sha256: string | null
  detail: Record<string, unknown>
}

export interface DemoState {
  case_id: string
  phase: Phase
  title: string
  company: string
  period: string
  materiality: number
  population_count: number
  total_amount: number
  high_risk_count: number
  high_risk_amount: number
  medium_risk_count: number
  evidence_coverage: number
  transactions: Transaction[]
  evidence: EvidenceRecord[]
  findings: Finding[]
  agents: AgentRun[]
  relationship_graph: {
    nodes: Array<{ id: string; name: string; category: string; risk: number }>
    links: Array<{ source: string; target: string; label: string }>
  }
  control_points: Array<{ name: string; score: number; severity: string }>
  proposal: Record<string, any> | null
  approval: Record<string, any> | null
  execution: Record<string, any> | null
  verification: Record<string, any> | null
  rollback: Record<string, any> | null
  audit_events: AuditEvent[]
  governance: GovernanceStatus
}
