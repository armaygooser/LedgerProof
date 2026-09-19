import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    governance_url: str
    executor_token: str
    approval_secret: str
    audit_reader_token: str
    verifier_token: str


def load_settings() -> Settings:
    return Settings(
        governance_url=os.getenv("LEDGERPROOF_GOVERNANCE_URL", "http://127.0.0.1:18805").rstrip("/"),
        executor_token=os.getenv(
            "LEDGERPROOF_EXECUTOR_TOKEN", "ledgerproof-demo-executor-token-change-me"
        ),
        approval_secret=os.getenv(
            "LEDGERPROOF_APPROVAL_SECRET", "ledgerproof-demo-approval-secret-change-me"
        ),
        audit_reader_token=os.getenv(
            "LEDGERPROOF_AUDIT_READER_TOKEN", "ledgerproof-demo-audit-reader-token-change-me"
        ),
        verifier_token=os.getenv(
            "LEDGERPROOF_VERIFIER_TOKEN", "ledgerproof-demo-verifier-token-change-me"
        ),
    )
