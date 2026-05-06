"""Shared judge-call utilities for the Beyond Recall study.

Single import path for every judge invocation. New judging code MUST go
through this module rather than rolling its own httpx / SDK call. The
historical motivation is the GPT-5.x ``max_tokens`` vs ``max_completion_tokens``
incident on 2026-04-25 (see ``docs/reviews/v11_gpt54_batch_failures_diagnostic_rerun_20260425.md``).

Public surface
--------------
    call_judge(provider, model, system, user, **kwargs) -> dict
    JudgeAPIError

Provider routing
----------------
    "openai"     -> openai_judge_call.call_openai_judge
    "anthropic"  -> anthropic_judge_call.call_anthropic_judge
    "gemini"     -> gemini_judge_call.call_gemini_judge

Or pass ``provider=None`` and the dispatcher will route by model id prefix:
    gpt-*, o1-*, o3-*  -> openai
    claude-*           -> anthropic
    gemini-*           -> gemini
"""

from __future__ import annotations

from typing import Any

from .anthropic_judge_call import call_anthropic_judge
from .gemini_judge_call import call_gemini_judge
from .openai_judge_call import (
    JudgeAPIError,
    call_openai_judge,
    call_openai_judge_user_only,
)


def _provider_from_model(model: str) -> str:
    m = model.lower().strip()
    if m.startswith(("gpt-", "o1", "o3")):
        return "openai"
    if m.startswith("claude"):
        return "anthropic"
    if m.startswith("gemini"):
        return "gemini"
    raise JudgeAPIError(f"Cannot infer provider from model id: {model!r}",
                        failure_type="UNKNOWN")


def call_judge(
    provider: str | None,
    model: str,
    system: str,
    user: str,
    **kwargs: Any,
) -> dict[str, Any]:
    """Provider-agnostic judge dispatcher.

    Parameters
    ----------
    provider : ``"openai"`` | ``"anthropic"`` | ``"gemini"`` | ``None``.
        If None, the provider is inferred from the model id prefix.
    model : Model id, e.g. ``gpt-5.4``, ``claude-haiku-4-5``, ``gemini-2.5-flash``.
    system : System-prompt string. Pass empty for none.
    user : User-prompt string carrying the rubric and inputs.
    **kwargs : Forwarded to the underlying provider call.

    Returns
    -------
    Structured result dict with ``score``, ``raw_text``, ``tokens``,
    ``latency_ms``, ``error_type``, ``model``, ``param_used``, ``prompt_hash``.

    Raises
    ------
    JudgeAPIError on any unrecoverable failure.
    """
    p = (provider or _provider_from_model(model)).lower()
    if p == "openai":
        return call_openai_judge(model, system, user, **kwargs)
    if p == "anthropic":
        return call_anthropic_judge(model, system, user, **kwargs)
    if p == "gemini":
        return call_gemini_judge(model, system, user, **kwargs)
    raise JudgeAPIError(f"Unknown provider: {provider!r}", failure_type="UNKNOWN")


__all__ = [
    "JudgeAPIError",
    "call_judge",
    "call_openai_judge",
    "call_openai_judge_user_only",
    "call_anthropic_judge",
    "call_gemini_judge",
]
