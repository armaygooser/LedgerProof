from __future__ import annotations

import json
import urllib.request


BASE = "http://127.0.0.1:18866"


def request(path: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        BASE + path,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST" if data is not None or path != "/api/demo" else "GET",
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.load(response)


def main() -> None:
    request("/api/demo/reset", {})
    proposed = request("/api/demo/run-to-approval", {})
    assert proposed["phase"] == "awaiting_approval"
    assert proposed["governance"]["connected"] is True
    approved = request("/api/demo/approve", {"approver": "财务总监 林岚"})
    assert approved["approval"]["proposal_record_sha256"] == approved["proposal"]["record_sha256"]
    executed = request("/api/demo/execute", {})
    assert executed["phase"] == "executed"
    verified = request("/api/demo/verify", {})
    assert verified["phase"] == "verified"
    assert verified["governance"]["audit_valid"] is True
    rolled_back = request(
        "/api/demo/rollback",
        {"approver": "财务总监 林岚", "reason": "演示回滚：解除临时止付并重新进入复核"},
    )
    assert rolled_back["phase"] == "rolled_back"
    assert rolled_back["verification"]["invalidated_by_rollback"] is True
    print(json.dumps({
        "case": rolled_back["case_id"],
        "phase": rolled_back["phase"],
        "audit_records": rolled_back["governance"]["audit_records"],
        "audit_head": rolled_back["governance"]["audit_head"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
