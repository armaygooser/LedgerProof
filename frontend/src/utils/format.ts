export function shortHash(value: string | null | undefined, left = 8, right = 6): string {
  if (!value) return '—'
  if (value.length <= left + right + 1) return value
  return `${value.slice(0, left)}…${value.slice(-right)}`
}

export function money(value: number): string {
  if (value >= 1_000_000) return `¥${(value / 1_000_000).toFixed(2)}M`
  if (value >= 1_000) return `¥${(value / 1_000).toFixed(value >= 100_000 ? 0 : 1)}K`
  return `¥${value.toLocaleString('zh-CN', { maximumFractionDigits: 0 })}`
}

export function phaseLabel(phase: string): string {
  const labels: Record<string, string> = {
    detected: '异常已发现',
    investigating: 'Agent 调查中',
    findings_ready: '调查完成',
    awaiting_approval: '等待人工审批',
    approved: '已批准待执行',
    executed: '止付已执行',
    verified: '独立复核通过',
    rolled_back: '已回滚',
  }
  return labels[phase] ?? phase
}
