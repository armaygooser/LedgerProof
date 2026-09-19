from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import load_settings
from .engine import DemoEngine
from .governance import CyberGuardClient, GovernanceError, GovernancePort
from .models import ApprovalInput, DemoState, RollbackInput


def create_app(governance: GovernancePort | None = None) -> FastAPI:
    owned_client: CyberGuardClient | None = None
    if governance is None:
        owned_client = CyberGuardClient(load_settings())
        governance = owned_client
    engine = DemoEngine(governance)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        yield
        if owned_client is not None:
            await owned_client.close()

    app = FastAPI(
        title="LedgerProof Financial Audit Console",
        version="0.1.0",
        docs_url="/api/docs",
        lifespan=lifespan,
    )
    app.state.engine = engine
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

    @app.exception_handler(GovernanceError)
    async def governance_error_handler(_, exc: GovernanceError):
        from fastapi.responses import JSONResponse

        return JSONResponse(status_code=503, content={"detail": str(exc), "source": "cyberguard"})

    @app.get("/health")
    async def health() -> dict:
        await engine.refresh_governance()
        return {
            "status": "ok" if engine.state.governance.connected else "degraded",
            "service": "ledgerproof-api",
            "governance": engine.state.governance.model_dump(),
        }

    @app.get("/api/demo", response_model=DemoState)
    async def demo() -> DemoState:
        return await engine.snapshot()

    @app.post("/api/demo/investigate", response_model=DemoState)
    async def investigate() -> DemoState:
        return await engine.investigate()

    @app.post("/api/demo/propose", response_model=DemoState)
    async def propose() -> DemoState:
        return await engine.propose()

    @app.post("/api/demo/run-to-approval", response_model=DemoState)
    async def run_to_approval() -> DemoState:
        if engine.state.phase == "detected":
            await engine.investigate()
        if engine.state.phase == "findings_ready":
            await engine.propose()
        if engine.state.phase != "awaiting_approval":
            raise HTTPException(status_code=409, detail="demo is not at approval phase")
        return engine.state

    @app.post("/api/demo/approve", response_model=DemoState)
    async def approve(payload: ApprovalInput) -> DemoState:
        return await engine.approve(payload.approver)

    @app.post("/api/demo/execute", response_model=DemoState)
    async def execute() -> DemoState:
        return await engine.execute()

    @app.post("/api/demo/verify", response_model=DemoState)
    async def verify() -> DemoState:
        return await engine.verify()

    @app.post("/api/demo/rollback", response_model=DemoState)
    async def rollback(payload: RollbackInput) -> DemoState:
        return await engine.rollback(payload.approver, payload.reason)

    @app.post("/api/demo/reset", response_model=DemoState)
    async def reset() -> DemoState:
        return await engine.reset()

    return app


app = create_app()
