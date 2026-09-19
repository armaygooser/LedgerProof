import { describe, expect, it } from 'vitest'
import { money, phaseLabel, shortHash } from './format'

describe('financial display helpers', () => {
  it('keeps hashes recognizable without exposing an unreadable wall of text', () => {
    expect(shortHash('a'.repeat(64))).toBe('aaaaaaaa…aaaaaa')
  })

  it('formats audit amounts and phases consistently', () => {
    expect(money(294000)).toBe('¥294K')
    expect(phaseLabel('awaiting_approval')).toBe('等待人工审批')
  })
})
