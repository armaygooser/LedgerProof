from __future__ import annotations

from typing import Any, Protocol

import httpx

from .config import Settings


class GovernanceError(RuntimeError):
    pass


class GovernancePort(Protocol):
    async def health(self) -> dict[str, Any]: ...
    async def propose(self, payload: dict[str, Any]) -> dict[str, Any]: ...
    async def approve(self, action_id: str, approver: str) -> dict[str, Any]: ...
    async def execute(self, action_id: str) -> dict[str, Any]: ...
    async def record_verification(self, action_id: str, payload: dict[str, Any]) -> dict[str, Any]: ...
    async def rollback(self, action_id: str, approver: str, reason: str) -> dict[str, Any]: ...
    async def action_history(self, action_id: str) -> dict[str, Any]: ...
    async def audit_verify(self) -> dict[str, Any]: ...
    async def finance_state(self, target: str) -> dict[str, Any]: ...


class CyberGuardClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = httpx.AsyncClient(base_url=settings.governance_url, timeout=8.0)

    async def close(self) -> None:
        await self.client.aclose()

    @property
    def executor_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.settings.executor_token}"}

    @property
    def reader_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.settings.audit_reader_token}"}

    async def request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        try:
            response = await self.client.request(method, path, **kwargs)
        except httpx.HTTPError as exc:
            raise GovernanceError(f"CyberGuard unavailable: {exc}") from exc
        if response.status_code >= 400:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text
            raise GovernanceError(f"CyberGuard {response.status_code}: {detail}")
        return response.json()

    async def health(self) -> dict[str, Any]:
        return await self.request("GET", "/health")

    async def propose(self, payload: dict[str, Any]) -> dict[str, Any]:
        return await self.request(
            "POST", "/finance/actions/propose", headers=self.executor_headers, json=payload
        )

    async def approve(self, action_id: str, approver: str) -> dict[str, Any]:
        headers = {**self.executor_headers, "X-Approval-Secret": self.settings.approval_secret}
        return await self.request(
            "POST",
            "/actions/approve",
            headers=headers,
            json={"action_id": action_id, "approver": approver, "expires_minutes": 15},
        )

    async def execute(self, action_id: str) -> dict[str, Any]:
        return await self.request(
            "POST", f"/finance/actions/{action_id}/execute", headers=self.executor_headers
        )

    async def record_verification(self, action_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.settings.verifier_token}"}
        return await self.request(
            "POST", f"/finance/actions/{action_id}/verification", headers=headers, json=payload
        )

    async def rollback(self, action_id: str, approver: str, reason: str) -> dict[str, Any]:
        headers = {**self.executor_headers, "X-Approval-Secret": self.settings.approval_secret}
        return await self.request(
            "POST",
            f"/finance/actions/{action_id}/rollback",
            headers=headers,
            json={"approver": approver, "reason": reason},
        )

    async def action_history(self, action_id: str) -> dict[str, Any]:
        return await self.request(
            "GET", f"/actions/{action_id}", headers=self.executor_headers
        )

    async def audit_verify(self) -> dict[str, Any]:
        return await self.request("GET", "/audit/verify", headers=self.executor_headers)

    async def finance_state(self, target: str) -> dict[str, Any]:
        return await self.request(
            "GET", f"/finance/state/{target}", headers=self.reader_headers
        )
