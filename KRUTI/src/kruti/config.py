from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import yaml


@dataclass(frozen=True)
class GuardrailsConfig:
    allowed_tools: List[str]
    tool_timeout_seconds: int


@dataclass(frozen=True)
class RagConfig:
    docs_path: str
    top_k: int


@dataclass(frozen=True)
class AgentConfig:
    max_steps: int
    system_prompt: str


@dataclass(frozen=True)
class LLMConfig:
    provider: str


@dataclass(frozen=True)
class AppConfig:
    name: str
    log_level: str


@dataclass(frozen=True)
class Config:
    app: AppConfig
    agent: AgentConfig
    guardrails: GuardrailsConfig
    rag: RagConfig
    llm: LLMConfig


def load_config(path: str | None = None) -> Config:
    cfg_path = path or os.getenv("KRUTI_CONFIG", "configs/kruti.yaml")
    data: Dict[str, Any] = yaml.safe_load(Path(cfg_path).read_text(encoding="utf-8"))

    return Config(
        app=AppConfig(**data["app"]),
        agent=AgentConfig(**data["agent"]),
        guardrails=GuardrailsConfig(**data["guardrails"]),
        rag=RagConfig(**data["rag"]),
        llm=LLMConfig(**data["llm"]),
    )
