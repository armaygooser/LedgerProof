import type { DemoState } from './types'

async function parseResponse(response: Response): Promise<DemoState> {
  const payload = await response.json()
  if (!response.ok) {
    throw new Error(typeof payload.detail === 'string' ? payload.detail : JSON.stringify(payload.detail))
  }
  return payload as DemoState
}

export async function loadDemo(): Promise<DemoState> {
  return parseResponse(await fetch('/api/demo', { cache: 'no-store' }))
}

export async function mutateDemo(path: string, body?: object): Promise<DemoState> {
  return parseResponse(
    await fetch(`/api/demo/${path}`, {
      method: 'POST',
      headers: body ? { 'Content-Type': 'application/json' } : undefined,
      body: body ? JSON.stringify(body) : undefined,
    }),
  )
}
