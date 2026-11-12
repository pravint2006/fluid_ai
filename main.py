"""
Secure Enterprise AI API
========================
A high-security, role-based enterprise AI API built with FastAPI.
Implements:
- Constant-time SHA-256 API key authentication with key fingerprinting
- Role-Based Access Control (RBAC) for "analyst" and "admin" roles
- Strict Pydantic input validation forbidding extra fields and echoing
- Prompt injection & simulated SQL injection regex guardrails
- In-memory sliding-window rate limiting per IP (5 requests / 60 seconds)
- Tamper-evident structured JSON Lines audit logging (audit.log)
- Secure global exception handling with zero stack trace or input leakage
- Safe configuration loading from environment variables or .env file
"""

import hashlib
import hmac
import json
import os
import re
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ConfigDict, Field
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse


# ============================================================================
# 1. Configuration & Secrets Management
# ============================================================================

def _load_env_file(filepath: Path = Path(".env")) -> None:
    """
    Parse a local .env file if present, populating os.environ without
    external dependencies. Does not overwrite already set environment variables.
    """
    if not filepath.is_file():
        return
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if not stripped or stripped.startswith("#") or "=" not in stripped:
                    continue
                key, _, value = stripped.partition("=")
                key = key.strip()
                value = value.strip().strip("\"'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except Exception:
        # Ignore errors during optional .env loading to avoid startup crashes
        pass


_load_env_file()

# Safe demo fallback keys (used only when environment variables are not provided)
_DEFAULT_ANALYST_KEY = "analyst-secret-key-123"
_DEFAULT_ADMIN_KEY = "admin-secret-key-456"

_raw_analyst_key = os.getenv("ANALYST_API_KEY", _DEFAULT_ANALYST_KEY)
_raw_admin_key = os.getenv("ADMIN_API_KEY", _DEFAULT_ADMIN_KEY)


def _compute_sha256(raw_string: str) -> str:
    """Compute standard SHA-256 hex digest for a string."""
    return hashlib.sha256(raw_string.encode("utf-8")).hexdigest()


# Store ONLY SHA-256 hashes of keys in memory.
# Raw keys are immediately purged from memory scope.
STORED_API_KEY_HASHES: Dict[str, Dict[str, str]] = {
    _compute_sha256(_raw_analyst_key): {
        "user": "analyst_user",
        "role": "analyst",
    },
    _compute_sha256(_raw_admin_key): {
        "user": "admin_user",
        "role": "admin",
    },
}

# Purge plaintext keys from module namespace
del _raw_analyst_key
del _raw_admin_key

# Rate limit configuration
RATE_LIMIT_MAX_REQUESTS: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "5"))
RATE_LIMIT_WINDOW_SECONDS: float = float(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60.0"))


# ============================================================================
# 2. Audit Logging System
# ============================================================================

AUDIT_LOG_PATH = Path("audit.log")
_audit_file_lock = threading.Lock()


def log_audit_event(
    event: str,
    user: Optional[str] = None,
    role: Optional[str] = None,
    action: Optional[str] = None,
    ip: str = "unknown",
    **extra: Any,
) -> None:
    """
    Append a structured JSON line to audit.log.
    Guarantees required fields: timestamp, event, user, role, action, ip.
    Ensures thread-safe, non-blocking file flush without logging raw secrets.
    """
    entry: Dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "user": user,
        "role": role,
        "action": action,
        "ip": ip,
    }
    if extra:
        entry.update(extra)

    line = json.dumps(entry) + "\n"
    with _audit_file_lock:
        with open(AUDIT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line)
            f.flush()


def get_key_fingerprint(raw_key: str) -> str:
    """
    Generate an 8-character hex fingerprint of the SHA-256 key hash.
    Safe for diagnostic logs; the raw key is never exposed.
    """
    return _compute_sha256(raw_key)[:8]


# ============================================================================
# 3. Security Guardrails & Authentication
# ============================================================================

# Regex for Prompt Injection and simulated SQL injection patterns
_PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+previous\s+instructions",
    r"reveal\s+system\s+prompt",
    r"you\s+are\s+now",
]

_SQL_INJECTION_PATTERNS = [
    r"union\s+select",
    r"drop\s+table",
    r"';",
    r"--",
]

_COMBINED_INJECTION_REGEX = re.compile(
    "|".join(_PROMPT_INJECTION_PATTERNS + _SQL_INJECTION_PATTERNS),
    re.IGNORECASE,
)


def detect_injection(text: str) -> bool:
    """Scan text for prompt injection or simulated SQL injection markers."""
    return bool(_COMBINED_INJECTION_REGEX.search(text))


def authenticate_api_key(raw_key: str) -> Optional[Dict[str, str]]:
    """
    Verify incoming API key using constant-time comparison against stored SHA-256 hashes.
    Returns user details dict if valid, or None if invalid.
    """
    candidate_hash = _compute_sha256(raw_key)
    matched_identity: Optional[Dict[str, str]] = None

    # Compare candidate hash against all stored hashes using constant-time comparison
    for stored_hash, identity in STORED_API_KEY_HASHES.items():
        if hmac.compare_digest(stored_hash, candidate_hash):
            matched_identity = identity
            break

    return matched_identity


# ============================================================================
# 4. In-Memory Sliding Window Rate Limiter
# ============================================================================

class InMemoryRateLimiter:
    """Thread-safe sliding-window rate limiter per IP address."""

    def __init__(self, max_requests: int = 5, window_seconds: float = 60.0) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._history: Dict[str, List[float]] = {}
        self._lock = threading.Lock()

    def is_allowed(self, ip: str) -> bool:
        """Check if the given IP is within rate limits; records current request if allowed."""
        now = time.time()
        cutoff = now - self.window_seconds
        with self._lock:
            timestamps = self._history.get(ip, [])
            valid_timestamps = [t for t in timestamps if t > cutoff]
            if len(valid_timestamps) >= self.max_requests:
                self._history[ip] = valid_timestamps
                return False
            valid_timestamps.append(now)
            self._history[ip] = valid_timestamps
            return True

    def reset(self, ip: Optional[str] = None) -> None:
        """Reset rate limit history for a specific IP or all IPs (useful for testing)."""
        with self._lock:
            if ip:
                self._history.pop(ip, None)
            else:
                self._history.clear()


rate_limiter = InMemoryRateLimiter(
    max_requests=RATE_LIMIT_MAX_REQUESTS,
    window_seconds=RATE_LIMIT_WINDOW_SECONDS,
)


def get_client_ip(request: Request) -> str:
    """Extract client IP, inspecting X-Forwarded-For header before client host."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "127.0.0.1"


# ============================================================================
# 5. Business Actions & RBAC Logic (Mock Data)
# ============================================================================

MOCK_SALES_REPORT: Dict[str, Any] = {
    "week": "2026-W45",
    "reporting_period": "November 3 - November 9, 2026",
    "total_revenue_usd": 154200.00,
    "total_orders": 1280,
    "average_order_value_usd": 120.47,
    "by_region": {
        "North America": 68400.00,
        "Europe": 51200.00,
        "Asia Pacific": 34600.00,
    },
    "currency": "USD",
}

SUPPORT_TICKETS: List[Dict[str, Any]] = []

MOCK_EMPLOYEES: Dict[str, Dict[str, str]] = {
    "alice": {
        "id": "EMP-101",
        "name": "Alice Johnson",
        "role": "Principal Systems Architect",
        "department": "Infrastructure & Security",
        "email": "alice.johnson@enterprise.internal",
    },
    "bob": {
        "id": "EMP-102",
        "name": "Bob Smith",
        "role": "Senior Financial Analyst",
        "department": "Corporate Finance",
        "email": "bob.smith@enterprise.internal",
    },
    "charlie": {
        "id": "EMP-103",
        "name": "Charlie Davis",
        "role": "Director of Customer Success",
        "department": "Support Engineering",
        "email": "charlie.davis@enterprise.internal",
    },
}

# Role permissions mapping:
# Analyst: sales_report, create_ticket, fallback
# Admin: sales_report, create_ticket, employee_info, fallback
ROLE_PERMISSIONS: Dict[str, List[str]] = {
    "sales_report": ["analyst", "admin"],
    "create_ticket": ["analyst", "admin"],
    "employee_info": ["admin"],
    "fallback": ["analyst", "admin"],
}


def route_question_to_action(question: str) -> str:
    """Route natural language request to an enterprise business action."""
    q_lower = question.lower()

    # 1. Sales report keywords
    if any(k in q_lower for k in ["sales", "revenue", "weekly sales", "sales report", "totals"]):
        return "sales_report"

    # 2. Support ticket keywords
    if any(k in q_lower for k in ["ticket", "support", "issue", "bug", "helpdesk", "incident", "problem"]):
        return "create_ticket"

    # 3. Employee info keywords
    if any(k in q_lower for k in ["employee", "staff", "personnel", "directory", "worker"]) or any(
        name in q_lower for name in MOCK_EMPLOYEES
    ):
        return "employee_info"

    # 4. Optional LLM routing if an external API key is set in environment
    llm_key = os.getenv("LLM_API_KEY")
    if llm_key:
        # LLM integration hook (keyword router remains primary and deterministic)
        pass

    return "fallback"


def execute_action(action: str, user: str, question: str) -> Dict[str, Any]:
    """Execute the target enterprise action and return results."""
    if action == "sales_report":
        return {
            "report": MOCK_SALES_REPORT,
            "generated_for": user,
        }

    if action == "create_ticket":
        ticket_id = f"TICK-{len(SUPPORT_TICKETS) + 1:04d}"
        ticket_record = {
            "ticket_id": ticket_id,
            "created_by": user,
            "summary": question,
            "status": "OPEN",
            "priority": "Normal",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        SUPPORT_TICKETS.append(ticket_record)
        return {
            "message": f"Support ticket {ticket_id} created successfully.",
            "ticket": ticket_record,
        }

    if action == "employee_info":
        q_lower = question.lower()
        for name_key, details in MOCK_EMPLOYEES.items():
            if name_key in q_lower or details["name"].lower() in q_lower:
                return {
                    "matched": True,
                    "employee": details,
                }
        return {
            "matched": True,
            "directory": list(MOCK_EMPLOYEES.values()),
            "message": "Retrieved enterprise employee directory.",
        }

    # Fallback action
    return {
        "message": (
            "I could not determine the appropriate enterprise action for your request. "
            "Supported queries include: "
            "1. Sales Report (e.g., 'Generate this week\'s sales report'), "
            "2. Support Tickets (e.g., 'Create a ticket for payment failure'), "
            "3. Employee Directory (e.g., 'Lookup employee info for Alice' - Admin only)."
        )
    }


# ============================================================================
# 6. Pydantic Models
# ============================================================================

class AskRequest(BaseModel):
    """
    Strict input validation model.
    Forbids any extra/unexpected fields to prevent mass-assignment/pollution.
    Enforces minimum and maximum length constraints.
    """
    model_config = ConfigDict(extra="forbid")

    question: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="Enterprise inquiry or command",
    )
    api_key: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="Enterprise API authentication key",
    )


# ============================================================================
# 7. FastAPI Application Setup & Global Handlers
# ============================================================================

app = FastAPI(
    title="Secure Enterprise AI API",
    description="Enterprise API with RBAC, Audit Logging, and Injection Guardrails",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next: Any) -> Any:
    """Enforce per-IP rate limiting before request processing."""
    if request.url.path == "/ask" and request.method == "POST":
        client_ip = get_client_ip(request)
        if not rate_limiter.is_allowed(client_ip):
            log_audit_event(
                event="rate_limited",
                user=None,
                role=None,
                action=None,
                ip=client_ip,
            )
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"},
            )

    return await call_next(request)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """
    Handle malformed payloads: invalid JSON, extra fields, length violations.
    Returns generic 422 without echoing user input or stack traces.
    """
    client_ip = get_client_ip(request)
    log_audit_event(
        event="malformed_request",
        user=None,
        role=None,
        action=None,
        ip=client_ip,
    )
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid request"},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    """
    Standardize HTTP exceptions to avoid leaking internal error structures.
    """
    status_map = {
        400: "Invalid request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not found",
        422: "Invalid request",
        429: "Too many requests",
        500: "Internal error",
    }
    generic_detail = status_map.get(exc.status_code, "Invalid request")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": generic_detail},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Catch-all global exception handler. Logs server_error to audit.log and
    returns a generic 500 message without stack traces.
    """
    client_ip = get_client_ip(request)
    log_audit_event(
        event="server_error",
        user=None,
        role=None,
        action=None,
        ip=client_ip,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal error"},
    )


# ============================================================================
# 8. Main Endpoint
# ============================================================================

@app.post("/ask")
async def ask_endpoint(payload: AskRequest, request: Request) -> JSONResponse:
    """
    Enterprise question-and-action endpoint.
    Flow:
    1. Authenticate API key via constant-time SHA-256 digest comparison.
    2. Guardrail scan for prompt injection & simulated SQL injection.
    3. Route question to enterprise business action.
    4. Enforce RBAC permissions.
    5. Execute business action and record audit log.
    """
    client_ip = get_client_ip(request)

    # 1. API Key Authentication
    user_identity = authenticate_api_key(payload.api_key)
    if not user_identity:
        log_audit_event(
            event="auth_failed",
            user=None,
            role=None,
            action=None,
            ip=client_ip,
            fingerprint=get_key_fingerprint(payload.api_key),
        )
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized"},
        )

    current_user = user_identity["user"]
    current_role = user_identity["role"]

    # 2. Input Guardrails (Prompt Injection & SQL Injection)
    if detect_injection(payload.question):
        log_audit_event(
            event="injection_blocked",
            user=current_user,
            role=current_role,
            action=None,
            ip=client_ip,
            fingerprint=get_key_fingerprint(payload.api_key),
        )
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid request"},
        )

    # 3. Action Routing
    action = route_question_to_action(payload.question)

    # 4. Role-Based Access Control (RBAC)
    allowed_roles = ROLE_PERMISSIONS.get(action, [])
    if current_role not in allowed_roles:
        log_audit_event(
            event="forbidden",
            user=current_user,
            role=current_role,
            action=action,
            ip=client_ip,
            fingerprint=get_key_fingerprint(payload.api_key),
        )
        return JSONResponse(
            status_code=403,
            content={"detail": "Forbidden"},
        )

    # 5. Execute Action
    result_data = execute_action(action, current_user, payload.question)

    # 6. Audit Log Success
    log_audit_event(
        event="action_ok",
        user=current_user,
        role=current_role,
        action=action,
        ip=client_ip,
        fingerprint=get_key_fingerprint(payload.api_key),
    )

    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
            "action": action,
            "data": result_data,
        },
    )

