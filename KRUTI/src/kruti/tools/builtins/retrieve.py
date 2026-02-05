from __future__ import annotations

from typing import Any, Dict

from kruti.rag.index import TinyIndex
from kruti.tools.base import Tool, ToolSpec


class RetrieveTool(Tool):
    spec = ToolSpec(
        name="retrieve",
        description="Search local docs (examples/local_docs) using tiny keyword index.",
        args_schema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
    )

    def __init__(self) -> None:
        # default docs folder used in repo; CLI can reindex via config.
        self.index = TinyIndex.from_folder("examples/local_docs")

    def run(self, args: Dict[str, Any], timeout_seconds: int = 10) -> str:
        query = str(args.get("query", "")).strip()
        if not query:
            return "error: empty query"
        hits = self.index.search(query, top_k=3)
        if not hits:
            return "no_results"
        parts = []
        for doc, score in hits:
            snippet = doc.text.strip().replace("\n", " ")
            if len(snippet) > 280:
                snippet = snippet[:280] + "…"
            parts.append(f"[{doc.doc_id} | score={int(score)}] {snippet}")
        return "\n".join(parts)
