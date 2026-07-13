"""
role: gtw-router
purpose: zero-cost acceptance router (EVOLUTION.md Round 2 #7) — try the cheapest
         tier first, machine-score the response with cheap heuristics (no LLM judge),
         and escalate only on evidence of a bad answer. Hard override rules for
         security/money/auth/PII/cross-layer/spec-review-class tasks run BEFORE any
         classifier, forcing the gatekeeper/deep tier regardless of score — "escalate
         on evidence only" (00-operating-system.md) made mechanical, not a discipline
         agents must remember.
gate: cross (every route decision passes through this before a spawn/response is
      accepted; wraps routing.route_for, never replaces it)
inputs: response_text (str, the candidate output to score), expect_json (bool),
        score/threshold (float in [0,1]), task_text (str, the task/ticket brief used
        to test OVERRIDE_RULES), role/priority (routing.route_for passthrough)
outputs: none on disk — pure functions; callers (dispatcher/CLI) log the routed
         decision via runlog.log if they choose to
exit: functions raise no exceptions on well-formed input (score() and
      route_with_acceptance() are total over str inputs); __main__ demo prints PASS
      and exits 0

Signals scored (each cheap: regex/len, no model call — see `score()` docstring for
the exact weight table). This is the "acceptance" half of budgeted autonomy: a
cheap tier's output is trusted unless it exhibits a concrete failure signature,
not because the caller "felt" it was probably fine.
"""
from __future__ import annotations

import json
import re

from . import routing

# ── Signal patterns (cheap, deterministic — no model call) ────────────────────

# A model declining/refusing the task outright.
_REFUSAL_RE = re.compile(
    r"(?i)\b("
    r"i (?:can'?t|cannot|won'?t|will not) (?:help|assist|do that|comply)|"
    r"i'?m (?:not able|unable) to|"
    r"as an ai (?:language model|assistant)|"
    r"i don'?t have (?:the ability|access) to|"
    r"i'?m sorry,? (?:but )?i (?:can'?t|cannot)"
    r")\b"
)

# A response that was visibly cut off mid-thought.
_TRUNCATION_RE = re.compile(
    r"(?:\.\.\.$|,$|:$|\bcontinued\b\s*$|\[truncated\]|\btoken limit\b|\bmax tokens\b)",
    re.I,
)

# The model echoing back an error/exception instead of doing the task.
_ERROR_ECHO_RE = re.compile(
    r"(?i)\b("
    r"traceback \(most recent call last\)|"
    r"(?:error|exception)\s*:\s*\S|"
    r"undefined is not a function|"
    r"internal server error|"
    r"segmentation fault|"
    r"null pointer exception"
    r")\b"
)

# A floor below which a response is almost certainly a non-answer (stub/empty).
_MIN_LEN_FLOOR = 20

# ── OVERRIDE_RULES: (regex, forced_tier) — checked BEFORE any classifier ───────
# Category → forced tier. These fire on the TASK text, not the response, and
# short-circuit acceptance scoring entirely: a security/money/auth/PII/
# cross-layer/spec-review-class task never gets the cheap-tier treatment, no
# matter how confident a low-tier response looks.
OVERRIDE_RULES: list[tuple[re.Pattern, str]] = [
    (re.compile(r"(?i)\b(password|credential|secret[_-]?key|api[_-]?key|token leak|"
                r"auth(?:entication|orization)?|login|session hijack|privilege escalat)\b"),
     "gatekeeper"),
    (re.compile(r"(?i)\b(payment|refund|invoice|billing|wire transfer|payout|"
                r"credit card|bank account|money|pricing change)\b"),
     "gatekeeper"),
    (re.compile(r"(?i)\b(pii|personally identifiable|ssn|social security|gdpr|"
                r"date of birth|medical record)\b"),
     "gatekeeper"),
    (re.compile(r"(?i)\b(sql injection|xss|csrf|rce|remote code execution|"
                r"pentest|penetration test|vulnerabilit(?:y|ies)|exploit)\b"),
     "deep"),
    (re.compile(r"(?i)\b(cross[- ]layer|race condition|spec[- ]review|"
                r"architectural arbitration|hard gate)\b"),
     "gatekeeper"),
]


def score(response_text: str, expect_json: bool = False) -> float:
    """Score a response in [0,1] — higher is more acceptable. No LLM involved.

    Signals (each a deduction from a 1.0 baseline; floors at 0.0):
      - empty/whitespace-only                  -> 0.0 flat (nothing to accept)
      - shorter than _MIN_LEN_FLOOR chars       -> -0.5 (likely a stub/non-answer)
      - refusal marker matched                  -> -0.6 (declined the task)
      - truncation marker matched                -> -0.4 (cut off mid-answer)
      - error-echo pattern matched                -> -0.5 (leaked a stack trace/error
                                                     instead of doing the task)
      - expect_json=True and json.loads() fails  -> -0.7 (contract violation: caller
                                                     asked for structured output)
    Deductions stack (a response can be both truncated AND an error echo).
    """
    if response_text is None or not response_text.strip():
        return 0.0

    text = response_text.strip()
    s = 1.0

    if len(text) < _MIN_LEN_FLOOR:
        s -= 0.5
    if _REFUSAL_RE.search(text):
        s -= 0.6
    if _TRUNCATION_RE.search(text):
        s -= 0.4
    if _ERROR_ECHO_RE.search(text):
        s -= 0.5
    if expect_json:
        try:
            json.loads(text)
        except (json.JSONDecodeError, ValueError):
            s -= 0.7

    return max(0.0, min(1.0, s))


def should_escalate(score: float, threshold: float = 0.80) -> bool:
    """True when the acceptance score falls short of the bar — evidence to escalate."""
    return score < threshold


def override_tier(task_text: str) -> str | None:
    """Return the forced tier if any OVERRIDE_RULES pattern matches task_text, else None.

    First match wins (rules list is checked top-to-bottom); callers that want the
    dearest applicable tier should keep OVERRIDE_RULES ordered cheapest-forced-tier
    first only if that matters to them — here we simply return on first hit.
    """
    if not task_text:
        return None
    for pattern, tier in OVERRIDE_RULES:
        if pattern.search(task_text):
            return tier
    return None


def route_with_acceptance(role: str, task_text: str, priority: str | None = None) -> dict:
    """Compose routing.route_for with the override rules.

    An OVERRIDE_RULES hit on task_text forces the route's model tier to the
    matched tier (never downgrades below what routing.route_for already resolved)
    and stamps `overridden`/`override_reason` on the result. Otherwise the normal
    cheapest-that-clears-bar route from routing.yaml applies untouched.
    """
    route = routing.route_for(role, priority)
    forced = override_tier(task_text)
    if forced is None:
        route["overridden"] = False
        route["override_reason"] = ""
        return route

    current = route["model"]
    if current in routing.MODEL_ORDER and forced in routing.MODEL_ORDER:
        if routing.MODEL_ORDER.index(forced) > routing.MODEL_ORDER.index(current):
            route["model"] = forced
            route["model_id"] = routing.MODEL_IDS.get(forced, forced)
            route["tier"] = routing.MODEL_TIER.get(forced, "")
    route["overridden"] = True
    route["override_reason"] = "OVERRIDE_RULES match on task text (security/money/auth/PII/cross-layer/spec-review)"
    return route


if __name__ == "__main__":
    # ── Self-test: a good response scores high, a refusal scores low and
    # escalates, a money-keyword task forces the top-clearing tier. ──────────
    good = "Here is the completed function: def add(a, b): return a + b. Tests pass."
    refusal = "I'm sorry, but I can't help with that request."
    truncated_json = '{"status": "ok", "items": [1, 2, 3'  # cut off, invalid JSON

    good_score = score(good)
    refusal_score = score(refusal)
    json_score = score(truncated_json, expect_json=True)

    assert good_score >= 0.80, f"expected good response to score high, got {good_score}"
    assert not should_escalate(good_score), "good response should NOT escalate"

    assert refusal_score < 0.80, f"expected refusal to score low, got {refusal_score}"
    assert should_escalate(refusal_score), "refusal should escalate"

    assert should_escalate(json_score), "truncated/invalid JSON should escalate"

    assert override_tier("please rotate the API key and check the login flow") == "gatekeeper"
    assert override_tier("process a refund for the customer's payment") == "gatekeeper"
    assert override_tier("write a haiku about autumn") is None

    money_route = route_with_acceptance("bck-api-engineer", "issue a refund for this payment")
    assert money_route["overridden"] is True
    assert routing.MODEL_ORDER.index(money_route["model"]) >= routing.MODEL_ORDER.index("gatekeeper"), (
        f"money-keyword task should force gatekeeper-or-higher tier, got {money_route['model']}"
    )

    plain_route = route_with_acceptance("bck-api-engineer", "add a unit test for the parser")
    assert plain_route["overridden"] is False

    print(
        f"good={good_score:.2f} refusal={refusal_score:.2f} json_fail={json_score:.2f} "
        f"money_route={money_route['model']} plain_route={plain_route['model']}"
    )
    print("PASS")
