import { Table, Tag } from 'antd'
import type { ColumnsType } from 'antd/es/table'
import type { Transaction } from '../types'
import { money } from '../utils/format'

export function TransactionTable({ transactions }: { transactions: Transaction[] }) {
  const rows = transactions
    .filter((item) => item.risk_level !== 'low')
    .sort((a, b) => b.risk_score - a.risk_score)
    .slice(0, 18)
  const columns: ColumnsType<Transaction> = [
    { title: '交易', dataIndex: 'transaction_id', width: 128, render: (value) => <code className="tx-id">{value}</code> },
    { title: '供应商', dataIndex: 'vendor_name', width: 150 },
    { title: '发票', dataIndex: 'invoice_id', width: 108 },
    { title: '金额', dataIndex: 'amount', width: 112, align: 'right', render: (value) => <strong>{money(value)}</strong> },
    { title: '提交时间', dataIndex: 'submitted_at', width: 150 },
    {
      title: '风险',
      dataIndex: 'risk_score',
      width: 92,
      align: 'center',
      render: (value, row) => <Tag color={row.risk_level === 'high' ? 'red' : 'orange'}>{value}</Tag>,
    },
    {
      title: '触发控制点',
      dataIndex: 'triggers',
      render: (values: string[]) => (
        <div className="trigger-tags">{values.slice(0, 3).map((value) => <Tag key={value}>{value}</Tag>)}</div>
      ),
    },
  ]
  return (
    <section className="panel transaction-panel">
      <div className="panel-header">
        <div>
          <span className="panel-kicker">RISK-PRIORITIZED REVIEW</span>
          <h2>高风险交易队列</h2>
        </div>
        <span className="table-note">按风险分降序 · 全量 {transactions.length.toLocaleString('zh-CN')} 笔</span>
      </div>
      <Table<Transaction>
        rowKey="transaction_id"
        columns={columns}
        dataSource={rows}
        pagination={false}
        size="small"
        scroll={{ x: 970 }}
        rowClassName={(row) => (row.risk_level === 'high' ? 'high-risk-row' : '')}
      />
    </section>
  )
}
