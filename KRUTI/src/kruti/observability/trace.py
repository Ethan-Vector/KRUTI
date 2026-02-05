from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Span:
    name: str
    start: float
    meta: Dict[str, Any]

    def end(self, **meta: Any) -> Dict[str, Any]:
        end = time.time()
        payload = {
            "span": self.name,
            "t_ms": int((end - self.start) * 1000),
            "meta": {**self.meta, **meta},
        }
        return payload


def start_span(name: str, **meta: Any) -> Span:
    return Span(name=name, start=time.time(), meta=dict(meta))


def log_event(event: str, **fields: Any) -> None:
    payload = {"event": event, **fields}
    print(json.dumps(payload, ensure_ascii=False))
