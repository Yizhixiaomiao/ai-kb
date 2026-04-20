from __future__ import annotations

import argparse
import json
import re
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from build_kb_chunk_vector_index import build_chunk_vector_records
from build_kb_chunks import build_chunks
from experience_intake import (
    DEFAULT_CANDIDATES as DEFAULT_CANDIDATES_PATH,
    DEFAULT_EXPERIENCE_LOG as DEFAULT_EXPERIENCE_LOG_PATH,
    append_experience,
    assess_experience,
    build_candidate,
    count_jsonl,
    load_candidates,
    recent_experiences,
    save_candidates,
)
from kb_chunk_search import build_answer, search_chunks
from recommend_from_ticket import DEFAULT_INDEX, recommend
from vector_model import DEFAULT_DIMENSIONS, build_vector_records


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FEEDBACK_LOG = ROOT / "data" / "kb-feedback.jsonl"
DEFAULT_EXPERIENCE_LOG = DEFAULT_EXPERIENCE_LOG_PATH
DEFAULT_CANDIDATES = DEFAULT_CANDIDATES_PATH
DEFAULT_VECTOR_INDEX = ROOT / "data" / "kb-vector-index.json"
DEFAULT_CHUNKS = ROOT / "data" / "kb-chunks.json"
DEFAULT_CHUNK_VECTOR_INDEX = ROOT / "data" / "kb-chunk-vector-index.json"
WEB_DIR = ROOT / "web"


class KbService:
    def __init__(
        self,
        index_path: Path,
        feedback_log: Path,
        vector_index_path: Path | None = None,
        chunks_path: Path | None = None,
        chunk_vector_index_path: Path | None = None,
        experience_log: Path | None = None,
        candidates_path: Path | None = None,
    ):
        self.index_path = index_path
        self.feedback_log = feedback_log
        self.vector_index_path = vector_index_path
        self.chunks_path = chunks_path
        self.chunk_vector_index_path = chunk_vector_index_path
        self.experience_log = experience_log or DEFAULT_EXPERIENCE_LOG
        self.candidates_path = candidates_path or DEFAULT_CANDIDATES
        self.index = self.load_index()
        self.vector_model = "local-char-ngram-hash-v1"
        self.vector_dimensions = DEFAULT_DIMENSIONS
        self.vector_records = self.load_vector_records()
        self.chunks = self.load_chunks()
        self.chunk_vector_records = self.load_chunk_vector_records()
        self.candidates = load_candidates(self.candidates_path)

    def load_index(self) -> list[dict]:
        return json.loads(self.index_path.read_text(encoding="utf-8"))

    def reload_index(self) -> int:
        self.index = self.load_index()
        self.vector_records = self.load_vector_records()
        self.chunks = self.load_chunks()
        self.chunk_vector_records = self.load_chunk_vector_records()
        self.candidates = load_candidates(self.candidates_path)
        return len(self.index)

    def load_vector_records(self) -> list[dict]:
        if self.vector_index_path and self.vector_index_path.exists():
            body = json.loads(self.vector_index_path.read_text(encoding="utf-8"))
            self.vector_model = body.get("model", self.vector_model)
            self.vector_dimensions = int(body.get("dimensions") or DEFAULT_DIMENSIONS)
            return body.get("documents", [])
        self.vector_dimensions = DEFAULT_DIMENSIONS
        return build_vector_records(self.index, dimensions=self.vector_dimensions)

    def load_chunks(self) -> list[dict]:
        if self.chunks_path and self.chunks_path.exists():
            return json.loads(self.chunks_path.read_text(encoding="utf-8"))
        return build_chunks(self.index)

    def load_chunk_vector_records(self) -> list[dict]:
        if self.chunk_vector_index_path and self.chunk_vector_index_path.exists():
            body = json.loads(self.chunk_vector_index_path.read_text(encoding="utf-8"))
            self.vector_model = body.get("model", self.vector_model)
            self.vector_dimensions = int(body.get("dimensions") or DEFAULT_DIMENSIONS)
            return body.get("chunks", [])
        return build_chunk_vector_records(self.chunks, dimensions=self.vector_dimensions)

    def recommend(self, payload: dict) -> dict:
        ticket_id = str(payload.get("ticket_id") or "")
        title = str(payload.get("title") or "")
        description = str(payload.get("description") or "")
        resolution = str(payload.get("resolution") or "")
        mode = str(payload.get("mode") or "hybrid")
        top_k = int(payload.get("top_k") or 3)
        top_k = max(1, min(top_k, 5))

        request_text = "\n".join(part for part in [title, description] if part)
        if not request_text.strip():
            return {
                "error": {
                    "code": "EMPTY_DESCRIPTION",
                    "message": "title or description is required",
                }
            }

        recommendations = []
        for item in recommend(
            self.index,
            request_text,
            resolution,
            top_k=top_k,
            mode=mode,
            vector_records=self.vector_records,
        ):
            confidence = "high" if item["score"] >= 30 else "medium" if item["score"] >= 15 else "low"
            recommendations.append(
                {
                    "doc_id": item["doc_id"],
                    "title": item["title"],
                    "status": item["status"],
                    "score": item["score"],
                    "rule_score": item.get("rule_score", 0),
                    "vector_score": item.get("vector_score", 0),
                    "confidence": confidence,
                    "path": item["path"],
                    "reason": item["reason"],
                    "applicability": item.get("applicability", []),
                    "symptoms": item.get("symptoms", []),
                    "steps": item.get("steps", []),
                    "commands": item.get("commands", []),
                    "verification": item.get("verification", []),
                    "notes": item.get("notes", []),
                    "content_preview": item.get("content_preview", ""),
                }
            )

        return {
            "request_id": f"rec-{int(time.time())}-{uuid.uuid4().hex[:8]}",
            "ticket_id": ticket_id,
            "mode": mode,
            "vector_model": self.vector_model,
            "matched": bool(recommendations),
            "recommendations": recommendations,
            "fallback": {
                "need_clarification": not bool(recommendations),
                "questions": [
                    "请补充故障对象：电脑、打印机、业务系统、网络、安防设备或会议室设备。",
                    "请补充具体现象，例如无法登录、无法打印、无信号、离线、卡纸、黑屏。",
                ]
                if not recommendations
                else [],
            },
        }

    def search(self, payload: dict) -> dict:
        ticket_id = str(payload.get("ticket_id") or "")
        title = str(payload.get("title") or "")
        description = str(payload.get("description") or "")
        query = str(payload.get("query") or "\n".join(part for part in [title, description] if part)).strip()
        mode = str(payload.get("mode") or "hybrid")
        top_k = int(payload.get("top_k") or 8)
        if not query:
            return {
                "error": {
                    "code": "EMPTY_QUERY",
                    "message": "query, title or description is required",
                }
            }

        chunks = search_chunks(
            self.chunks,
            query,
            top_k=top_k,
            mode=mode,
            vector_records=self.chunk_vector_records,
            dimensions=self.vector_dimensions,
        )
        return {
            "request_id": f"srch-{int(time.time())}-{uuid.uuid4().hex[:8]}",
            "ticket_id": ticket_id,
            "mode": mode,
            "query": query,
            "vector_model": self.vector_model,
            "matched": bool(chunks),
            "chunks": chunks,
        }

    def answer(self, payload: dict) -> dict:
        search_body = self.search(payload)
        if "error" in search_body:
            return search_body
        answer = build_answer(search_body["query"], search_body["chunks"], self.index)
        return {
            "request_id": f"ans-{int(time.time())}-{uuid.uuid4().hex[:8]}",
            "search_request_id": search_body["request_id"],
            "ticket_id": search_body.get("ticket_id", ""),
            "mode": search_body["mode"],
            "query": search_body["query"],
            "vector_model": self.vector_model,
            "matched": search_body["matched"],
            "answer": answer,
        }

    def save_experience(self, payload: dict) -> dict:
        ticket_id = str(payload.get("ticket_id") or "").strip()
        title = str(payload.get("title") or "").strip()
        description = str(payload.get("description") or "").strip()
        resolution = str(payload.get("resolution") or "").strip()
        if not ticket_id:
            return {"error": {"code": "INVALID_REQUEST", "message": "ticket_id is required"}}
        if not title and not description:
            return {"error": {"code": "INVALID_REQUEST", "message": "title or description is required"}}
        if not resolution:
            return {"error": {"code": "INVALID_REQUEST", "message": "resolution is required"}}

        assessment = assess_experience(payload)
        recs = recommend(
            self.index,
            "\n".join(part for part in [title, description] if part),
            resolution,
            top_k=3,
            mode="hybrid",
            vector_records=self.vector_records,
        )
        matched_doc = recs[0] if recs and recs[0].get("score", 0) >= 20 else None

        if assessment["quality"] == "low":
            action = "need_more_detail"
            candidate = None
        elif matched_doc:
            action = "attach_to_existing"
            candidate = None
        else:
            action = "create_candidate"
            candidate = build_candidate(payload, assessment, matched_doc=None)
            self.candidates.append(candidate)
            save_candidates(self.candidates, self.candidates_path)

        record = dict(payload)
        record["experience_id"] = f"exp-{int(time.time())}-{uuid.uuid4().hex[:8]}"
        record["created_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        record["quality"] = assessment["quality"]
        record["quality_score"] = assessment["quality_score"]
        record["action"] = action
        record["matched_doc_id"] = matched_doc.get("doc_id") if matched_doc else ""
        record["candidate_id"] = candidate.get("candidate_id") if candidate else ""
        append_experience(record, self.experience_log)

        return {
            "saved": True,
            "experience_id": record["experience_id"],
            "quality": assessment["quality"],
            "quality_score": assessment["quality_score"],
            "signals": assessment["signals"],
            "missing_fields": assessment["missing_fields"],
            "suggested_questions": assessment["suggested_questions"],
            "matched_doc": {
                "doc_id": matched_doc.get("doc_id"),
                "title": matched_doc.get("title"),
                "score": matched_doc.get("score"),
                "path": matched_doc.get("path"),
            }
            if matched_doc
            else None,
            "action": action,
            "suggested_candidate": candidate,
        }

    def save_feedback(self, payload: dict) -> dict:
        required = ["ticket_id", "doc_id", "action"]
        missing = [field for field in required if not payload.get(field)]
        if missing:
            return {
                "error": {
                    "code": "INVALID_REQUEST",
                    "message": f"missing required fields: {', '.join(missing)}",
                }
            }

        record = dict(payload)
        record["feedback_id"] = f"fb-{int(time.time())}-{uuid.uuid4().hex[:8]}"
        record["created_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        self.feedback_log.parent.mkdir(parents=True, exist_ok=True)
        with self.feedback_log.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return {"saved": True, "feedback_id": record["feedback_id"]}

    def create_candidate_doc(self, payload: dict) -> dict:
        title = str(payload.get("title") or "").strip()
        category = str(payload.get("category") or "manual").strip().lower()
        slug = str(payload.get("slug") or "").strip().lower()
        if not title:
            return {"error": {"code": "INVALID_REQUEST", "message": "title is required"}}
        if not slug:
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or f"kb-{int(time.time())}"
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,80}", slug):
            return {"error": {"code": "INVALID_REQUEST", "message": "slug must use lowercase letters, numbers and hyphen"}}
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,60}", category):
            return {"error": {"code": "INVALID_REQUEST", "message": "category must use lowercase letters, numbers and hyphen"}}

        def list_value(name: str, default: str = "") -> list[str]:
            value = payload.get(name)
            if isinstance(value, list):
                return [str(item).strip() for item in value if str(item).strip()]
            value = str(value or default)
            return [item.strip() for item in value.split(",") if item.strip()]

        def md_list(items) -> str:
            if isinstance(items, str):
                items = [line.strip() for line in items.splitlines() if line.strip()]
            if not items:
                return "- 待补充。"
            return "\n".join(f"- {item}" for item in items)

        def md_steps(items) -> str:
            if isinstance(items, str):
                items = [line.strip() for line in items.splitlines() if line.strip()]
            if not items:
                return "1. 待补充。"
            return "\n".join(f"{idx}. {item}" for idx, item in enumerate(items, start=1))

        def md_commands(items) -> str:
            if isinstance(items, str):
                lines = [line.strip() for line in items.splitlines() if line.strip()]
                items = [{"command": line, "purpose": "", "risk": "低"} for line in lines]
            if not items:
                return "- 待补充。"
            rows = []
            for item in items:
                if isinstance(item, dict):
                    command = str(item.get("command") or "").strip()
                    purpose = str(item.get("purpose") or "").strip()
                    risk = str(item.get("risk") or "低").strip()
                else:
                    command = str(item).strip()
                    purpose = ""
                    risk = "低"
                if command:
                    suffix = f" -- {purpose}" if purpose else ""
                    rows.append(f"- {command}{suffix}（风险：{risk}）")
            return "\n".join(rows) if rows else "- 待补充。"

        asset_types = list_value("asset_types", "server")
        systems = list_value("systems")
        issue_types = list_value("issue_types")
        tags = list_value("tags")
        status = str(payload.get("status") or "candidate").strip()
        if status not in {"candidate", "usable", "verified", "deprecated"}:
            status = "candidate"

        doc = f"""# {title}

```yaml
status: {status}
type: troubleshooting
source: manual-web
asset_types: [{", ".join(asset_types)}]
systems: [{", ".join(systems)}]
issue_types: [{", ".join(issue_types)}]
tags: [{", ".join(tags)}]
```

## 适用范围

{md_list(payload.get("applicability"))}

## 常见现象

{md_list(payload.get("symptoms"))}

## 处理步骤

{md_steps(payload.get("steps"))}

## 常用指令

{md_commands(payload.get("commands"))}

## 验证方式

{md_list(payload.get("verification"))}

## 注意事项

{md_list(payload.get("notes"))}
"""
        target_dir = ROOT / "docs" / "candidate" / category
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / f"{slug}.md"
        if target.exists():
            return {"error": {"code": "ALREADY_EXISTS", "message": str(target.relative_to(ROOT))}}
        target.write_text(doc, encoding="utf-8")
        return {"created": True, "path": str(target.relative_to(ROOT)).replace("\\", "/")}


def make_handler(service: KbService):
    class Handler(BaseHTTPRequestHandler):
        server_version = "OpsKbHttpService/0.1"

        def _send_json(self, status: int, body: dict):
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
            self.end_headers()
            self.wfile.write(data)

        def _send_file(self, path: Path):
            if not path.exists() or not path.is_file():
                self._send_json(404, {"error": {"code": "NOT_FOUND", "message": str(path)}})
                return
            suffix = path.suffix.lower()
            content_type = {
                ".html": "text/html; charset=utf-8",
                ".js": "application/javascript; charset=utf-8",
                ".css": "text/css; charset=utf-8",
                ".svg": "image/svg+xml",
            }.get(suffix, "application/octet-stream")
            data = path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _read_json(self) -> dict:
            length = int(self.headers.get("Content-Length") or "0")
            if length <= 0:
                return {}
            raw = self.rfile.read(length)
            return json.loads(raw.decode("utf-8"))

        def do_OPTIONS(self):
            self._send_json(200, {"ok": True})

        def do_GET(self):
            path = urlparse(self.path).path
            if path == "/health":
                self._send_json(
                    200,
                    {
                        "ok": True,
                        "documents": len(service.index),
                        "index_path": str(service.index_path),
                        "vector_model": service.vector_model,
                        "vector_documents": len(service.vector_records),
                        "chunks": len(service.chunks),
                        "vector_chunks": len(service.chunk_vector_records),
                        "experiences": count_jsonl(service.experience_log),
                        "candidates": len(service.candidates),
                        "vector_dimensions": service.vector_dimensions,
                    },
                )
                return
            if path == "/api/kb/index":
                self._send_json(200, {"documents": service.index})
                return
            if path == "/api/kb/chunks":
                self._send_json(200, {"chunks": service.chunks})
                return
            if path == "/api/kb/experiences":
                self._send_json(200, {"experiences": recent_experiences(service.experience_log)})
                return
            if path == "/api/kb/candidates":
                service.candidates = load_candidates(service.candidates_path)
                self._send_json(200, {"candidates": service.candidates})
                return
            if path in {"/", "/ui", "/ui/"}:
                self._send_file(WEB_DIR / "index.html")
                return
            if path.startswith("/ui/"):
                requested = (WEB_DIR / path.removeprefix("/ui/")).resolve()
                if WEB_DIR.resolve() not in requested.parents and requested != WEB_DIR.resolve():
                    self._send_json(403, {"error": {"code": "FORBIDDEN", "message": path}})
                    return
                self._send_file(requested)
                return
            self._send_json(404, {"error": {"code": "NOT_FOUND", "message": path}})

        def do_POST(self):
            path = urlparse(self.path).path
            try:
                payload = self._read_json()
            except json.JSONDecodeError as exc:
                self._send_json(400, {"error": {"code": "INVALID_JSON", "message": str(exc)}})
                return

            if path == "/api/kb/recommend":
                body = service.recommend(payload)
                status = 422 if "error" in body and body["error"]["code"] == "EMPTY_DESCRIPTION" else 200
                self._send_json(status, body)
                return
            if path == "/api/kb/search":
                body = service.search(payload)
                status = 422 if "error" in body and body["error"]["code"] == "EMPTY_QUERY" else 200
                self._send_json(status, body)
                return
            if path == "/api/kb/answer":
                body = service.answer(payload)
                status = 422 if "error" in body and body["error"]["code"] == "EMPTY_QUERY" else 200
                self._send_json(status, body)
                return
            if path == "/api/kb/feedback":
                body = service.save_feedback(payload)
                status = 400 if "error" in body else 200
                self._send_json(status, body)
                return
            if path == "/api/kb/experience":
                body = service.save_experience(payload)
                status = 400 if "error" in body else 200
                self._send_json(status, body)
                return
            if path == "/api/kb/admin/reload-index":
                count = service.reload_index()
                self._send_json(200, {"reloaded": True, "documents": count})
                return
            if path == "/api/kb/admin/create-doc":
                body = service.create_candidate_doc(payload)
                status = 400 if "error" in body else 200
                self._send_json(status, body)
                return
            self._send_json(404, {"error": {"code": "NOT_FOUND", "message": path}})

        def log_message(self, format: str, *args):
            print(f"{self.address_string()} - {format % args}")

    return Handler


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a local HTTP service for knowledge recommendations.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9100)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--vector-index", type=Path, default=DEFAULT_VECTOR_INDEX)
    parser.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS)
    parser.add_argument("--chunk-vector-index", type=Path, default=DEFAULT_CHUNK_VECTOR_INDEX)
    parser.add_argument("--feedback-log", type=Path, default=DEFAULT_FEEDBACK_LOG)
    parser.add_argument("--experience-log", type=Path, default=DEFAULT_EXPERIENCE_LOG)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    args = parser.parse_args()

    service = KbService(
        args.index,
        args.feedback_log,
        args.vector_index,
        args.chunks,
        args.chunk_vector_index,
        args.experience_log,
        args.candidates,
    )
    server = ThreadingHTTPServer((args.host, args.port), make_handler(service))
    print(f"Ops KB service listening on http://{args.host}:{args.port}")
    print(f"Loaded {len(service.index)} documents from {args.index}")
    print(f"Loaded {len(service.chunks)} chunks from {args.chunks}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
