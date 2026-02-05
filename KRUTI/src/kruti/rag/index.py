from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


@dataclass(frozen=True)
class Doc:
    doc_id: str
    text: str


class TinyIndex:
    """A deliberately simple local index: keyword scoring over plain text files.

    This keeps dependencies low and gives you a working retrieval loop you can swap later
    for BM25/vector embeddings.
    """

    def __init__(self, docs: List[Doc]):
        self.docs = docs

    @classmethod
    def from_folder(cls, folder: str) -> "TinyIndex":
        p = Path(folder)
        docs: List[Doc] = []
        for fp in sorted(p.rglob("*.txt")):
            docs.append(Doc(doc_id=str(fp.relative_to(p)), text=fp.read_text(encoding="utf-8")))
        return cls(docs)

    def search(self, query: str, top_k: int = 3) -> List[Tuple[Doc, float]]:
        q = query.lower()
        terms = [t for t in q.split() if len(t) >= 3]
        scored: List[Tuple[Doc, float]] = []
        for d in self.docs:
            text = d.text.lower()
            score = 0.0
            for t in terms:
                score += text.count(t)
            if score > 0:
                scored.append((d, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]
