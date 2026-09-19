import { useMemo, useState } from 'react'
import ReactECharts from 'echarts-for-react'
import { Segmented, Tag } from 'antd'
import type { DemoState } from '../types'
import { money } from '../utils/format'

export function RiskAnalytics({ state }: { state: DemoState }) {
  const [view, setView] = useState<string>('交易风险')
  const scatterOption = useMemo(() => {
    const sampled = state.transactions.filter(
      (transaction, index) => transaction.risk_level !== 'low' || index % 16 === 0,
    )
    return {
      animationDuration: 700,
      grid: { left: 58, right: 22, top: 28, bottom: 45 },
      tooltip: {
        trigger: 'item',
        formatter: (params: any) => {
          const tx = params.data.raw
          return `<b>${tx.transaction_id}</b><br/>${tx.vendor_name}<br/>金额 ${money(tx.amount)}<br/>风险 ${tx.risk_score}/100`
        },
      },
      xAxis: {
        name: '交易金额',
        nameLocation: 'middle',
        nameGap: 30,
        axisLabel: { formatter: (value: number) => money(value), color: '#667085' },
        splitLine: { lineStyle: { color: '#edf0f4' } },
      },
      yAxis: {
        name: '风险分',
        min: 0,
        max: 100,
        axisLabel: { color: '#667085' },
        splitLine: { lineStyle: { color: '#edf0f4' } },
      },
      series: [
        {
          type: 'scatter',
          data: sampled.map((transaction) => ({
            value: [transaction.amount, transaction.risk_score],
            raw: transaction,
            symbolSize: transaction.risk_level === 'high' ? 18 : transaction.risk_level === 'medium' ? 11 : 7,
            itemStyle: {
              color:
                transaction.risk_level === 'high'
                  ? '#d9363e'
                  : transaction.risk_level === 'medium'
                    ? '#d97706'
                    : '#7ea6ef',
              opacity: transaction.risk_level === 'low' ? 0.55 : 0.9,
            },
          })),
          markLine: {
            silent: true,
            symbol: 'none',
            label: { formatter: '高级审批阈值 ¥100K', color: '#8b5cf6' },
            lineStyle: { color: '#8b5cf6', type: 'dashed' },
            data: [{ xAxis: 100000 }],
          },
        },
      ],
    }
  }, [state.transactions])

  const graphOption = useMemo(() => {
    const colors: Record<string, string> = {
      employee: '#246bfd',
      vendor: '#d9363e',
      account: '#6e56cf',
      batch: '#d97706',
    }
    return {
      tooltip: { trigger: 'item' },
      animationDurationUpdate: 650,
      series: [
        {
          type: 'graph',
          layout: 'force',
          roam: true,
          label: { show: true, position: 'bottom', color: '#344054', fontSize: 11 },
          edgeLabel: { show: true, formatter: (params: any) => params.data.label, color: '#667085', fontSize: 10 },
          force: { repulsion: 310, edgeLength: [90, 145], gravity: 0.08 },
          lineStyle: { color: '#aeb7c4', width: 1.5, curveness: 0.08 },
          emphasis: { focus: 'adjacency', lineStyle: { width: 3 } },
          data: state.relationship_graph.nodes.map((node) => ({
            ...node,
            symbolSize: node.category === 'batch' ? 66 : 52,
            itemStyle: { color: colors[node.category] ?? '#667085', borderColor: '#fff', borderWidth: 3 },
          })),
          links: state.relationship_graph.links,
        },
      ],
    }
  }, [state.relationship_graph])

  return (
    <section className="panel analytics-panel">
      <div className="panel-header">
        <div>
          <span className="panel-kicker">FULL POPULATION ANALYSIS</span>
          <h2>全量交易风险分析</h2>
        </div>
        <Segmented options={['交易风险', '关系穿透']} value={view} onChange={(value) => setView(String(value))} />
      </div>
      <div className="analytics-body">
        <ReactECharts option={view === '交易风险' ? scatterOption : graphOption} style={{ height: 336 }} />
        <aside className="control-points">
          <div className="control-title">
            <span>触发控制点</span>
            <Tag color="red">组合风险 95</Tag>
          </div>
          {state.control_points.map((point) => (
            <div className="control-row" key={point.name}>
              <div>
                <strong>{point.name}</strong>
                <small>{point.severity.toUpperCase()}</small>
              </div>
              <b>+{point.score}</b>
            </div>
          ))}
          <div className="control-total">
            <span>综合风险评分</span>
            <strong>95<small>/100</small></strong>
          </div>
        </aside>
      </div>
    </section>
  )
}
