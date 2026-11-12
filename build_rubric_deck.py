#!/usr/bin/env python3
"""
Generate Executive Presentation Deck strictly adhering to the user's rubric:
1. Overall architecture & Technologies used
2. Authentication, Authorization & API Design
3. AI Workflow & Security Improvements
4. Business Actions Implemented
5. The Bug Story (Symptoms, Root Cause, Diagnosis, Resolution)
6. Tradeoff Discussion (Performance vs Protection & Security vs Usability)
7. Summary & Wrap-up
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_rubric_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Executive Modern Dark Palette
    BG_DARK = RGBColor(11, 15, 25)          # Deep Navy/Slate #0B0F19
    BG_CARD = RGBColor(19, 27, 46)          # Card Fill #131B2E
    BG_CARD_ALT = RGBColor(24, 34, 58)      # Card Fill Elevated #18223A
    BORDER_CYAN = RGBColor(0, 210, 255)     # Primary Accent #00D2FF
    BORDER_EMERALD = RGBColor(16, 185, 129) # Success Accent #10B981
    BORDER_ROSE = RGBColor(239, 68, 68)     # Warning / Issue Accent #EF4444
    BORDER_AMBER = RGBColor(245, 158, 11)   # Tradeoff Accent #F59E0B
    BORDER_VIOLET = RGBColor(139, 92, 246)  # AI Accent #8B5CF6
    BORDER_SUBTLE = RGBColor(33, 46, 77)    # Subtle Border #212E4D

    TEXT_WHITE = RGBColor(248, 250, 252)    # Pure White #F8FAFC
    TEXT_MUTED = RGBColor(148, 163, 184)    # Cool Gray #94A3B8
    TEXT_DIM = RGBColor(100, 116, 139)      # Slate Gray #64748B

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title, category, slide_num, total_slides=6):
        # Top cyan bar
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.05))
        line.fill.solid()
        line.fill.fore_color.rgb = BORDER_CYAN
        line.line.fill.background()

        # Category
        tb_c = slide.shapes.add_textbox(Inches(0.9), Inches(0.45), Inches(8.0), Inches(0.35))
        tf_c = tb_c.text_frame
        p_c = tf_c.paragraphs[0]
        p_c.text = f"// {category.upper()} //"
        p_c.font.name = "Segoe UI"
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = BORDER_CYAN

        # Title
        tb_t = slide.shapes.add_textbox(Inches(0.9), Inches(0.75), Inches(10.2), Inches(0.7))
        tf_t = tb_t.text_frame
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

        # Slide Number
        tb_n = slide.shapes.add_textbox(Inches(11.2), Inches(0.75), Inches(1.2), Inches(0.5))
        tf_n = tb_n.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.text = f"{slide_num:02d} / {total_slides:02d}"
        p_n.font.name = "Segoe UI"
        p_n.font.size = Pt(13)
        p_n.font.bold = True
        p_n.font.color.rgb = BORDER_CYAN

    def add_card(slide, left, top, width, height, title="", title_color=TEXT_WHITE, border_color=BORDER_SUBTLE, bg_color=BG_CARD):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        if title:
            tb = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.18), Inches(width - 0.5), Inches(0.4))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Segoe UI"
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = title_color
        return card

    def add_bullets(slide, left, top, width, height, items, font_size=11.5, space_after=8):
        tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, item in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(space_after)
            p.line_spacing = 1.15

            if isinstance(item, tuple):
                r1 = p.add_run()
                r1.text = f"•  {item[0]}: "
                r1.font.name = "Segoe UI"
                r1.font.bold = True
                r1.font.size = Pt(font_size)
                r1.font.color.rgb = TEXT_WHITE

                r2 = p.add_run()
                r2.text = item[1]
                r2.font.name = "Segoe UI"
                r2.font.size = Pt(font_size)
                r2.font.color.rgb = TEXT_MUTED
            else:
                r = p.add_run()
                r.text = f"•  {item}"
                r.font.name = "Segoe UI"
                r.font.size = Pt(font_size)
                r.font.color.rgb = TEXT_MUTED

    def set_notes(slide, text):
        slide.notes_slide.notes_text_frame.text = text

    # =========================================================================
    # SLIDE 1: Title & Overview
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.4), Inches(3.6), Inches(0.42))
    pill.fill.solid()
    pill.fill.fore_color.rgb = BG_CARD
    pill.line.color.rgb = BORDER_CYAN
    tf_p = pill.text_frame
    p_p = tf_p.paragraphs[0]
    p_p.alignment = PP_ALIGN.CENTER
    p_p.text = "⚡ ENTERPRISE AI ARCHITECTURE & SECURITY"
    p_p.font.name = "Segoe UI"
    p_p.font.size = Pt(10)
    p_p.font.bold = True
    p_p.font.color.rgb = BORDER_CYAN

    tb_main = s1.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(11.5), Inches(2.2))
    tf_main = tb_main.text_frame
    tf_main.word_wrap = True

    p1 = tf_main.paragraphs[0]
    p1.text = "Secure Enterprise AI Gateway"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(10)

    p2 = tf_main.add_paragraph()
    p2.text = "FastAPI Architecture, Zero-Trust Access Control, AI Guardrails & Incident Post-Mortem"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(18)
    p2.font.color.rgb = TEXT_MUTED

    # 4 Quick Highlights
    quick_items = [
        ("Architecture", "FastAPI • Uvicorn • Pydantic V2", BORDER_CYAN),
        ("Security", "SHA-256 Hashing • Constant-Time HMAC", BORDER_EMERALD),
        ("AI Safety", "NVIDIA Meta Llama-Guard-4-12B NIM", BORDER_VIOLET),
        ("Incident Solved", "Llama-Guard S7 Privacy / RBAC Fix", BORDER_AMBER)
    ]
    for idx, (t, d, col) in enumerate(quick_items):
        c_left = 0.9 + (idx * 2.92)
        c = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(4.7), Inches(2.75), Inches(1.7))
        c.fill.solid()
        c.fill.fore_color.rgb = BG_CARD
        c.line.color.rgb = col
        c.line.width = Pt(1.5)

        tf_c = c.text_frame
        tf_c.word_wrap = True
        p_c1 = tf_c.paragraphs[0]
        p_c1.text = t
        p_c1.font.name = "Segoe UI"
        p_c1.font.size = Pt(14)
        p_c1.font.bold = True
        p_c1.font.color.rgb = col
        p_c1.space_after = Pt(4)

        p_c2 = tf_c.add_paragraph()
        p_c2.text = d
        p_c2.font.name = "Segoe UI"
        p_c2.font.size = Pt(11)
        p_c2.font.color.rgb = TEXT_WHITE

    set_notes(s1, (
        "VIDEO PRESENTER SCRIPT (SLIDE 1 - INTRO / 30s):\n"
        "\"Hello everyone! In this technical walkthrough, I am presenting the architecture, security mechanisms, "
        "and incident resolution of our Secure Enterprise AI Gateway built with FastAPI.\n\n"
        "We'll cover our overall architecture, authentication and RBAC flows, AI guardrail workflow, a real-world bug "
        "we diagnosed and resolved involving Meta Llama Guard, and finally our architectural tradeoffs between performance, "
        "protection, and usability. Let's dive in!\""
    ))

    # =========================================================================
    # SLIDE 2: Overall Architecture, Tech Stack & API Design
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "System Architecture, Tech Stack & API Design", "FOUNDATION", 2)

    # Left: Overall Architecture
    add_card(s2, 0.9, 1.5, 5.6, 5.2, title="1. Overall Architecture & Request Pipeline", title_color=BORDER_CYAN, border_color=BORDER_CYAN)
    arch_bullets = [
        ("Multi-Layer Pipeline", "Requests pass sequentially: Rate Limiter ➔ Authenticator ➔ Dual Guardrails ➔ Intent Router ➔ RBAC Gate ➔ Execution."),
        ("FastAPI Async Core", "Asynchronous HTTP handlers with non-blocking threading for external AI safety evaluation."),
        ("Strict Defense-in-Depth", "Security is enforced at every layer; failure at any gate halts execution immediately before touching backend data.")
    ]
    add_bullets(s2, 1.1, 2.15, 5.2, 4.3, arch_bullets, font_size=11.5, space_after=12)

    # Right: Technologies Used & API Design
    add_card(s2, 6.8, 1.5, 5.6, 2.5, title="2. Technologies Used", title_color=BORDER_EMERALD, border_color=BORDER_EMERALD)
    tech_bullets = [
        ("Core Framework", "Python 3.14, FastAPI, Uvicorn (ASGI server)"),
        ("Validation & Modeling", "Pydantic V2 (Strict schema, extra='forbid')"),
        ("AI Safety Engine", "Meta Llama-Guard-4-12B via NVIDIA NIM API"),
        ("Security Primitives", "hashlib (SHA-256), hmac (compare_digest)")
    ]
    add_bullets(s2, 7.0, 2.05, 5.2, 1.8, tech_bullets, font_size=10.5, space_after=5)

    add_card(s2, 6.8, 4.2, 5.6, 2.5, title="3. API Design & Input Hygiene", title_color=BORDER_VIOLET, border_color=BORDER_VIOLET)
    api_bullets = [
        ("Single Unified Endpoint", "POST /ask with JSON payload: {'question': '...', 'api_key': '...'}"),
        ("Parameter Pollution Block", "extra='forbid' rejects unexpected fields with 422 Unprocessable Content."),
        ("Zero Input Reflection", "Custom RequestValidationError masks rejected inputs; returns generic {'detail': 'Invalid request'}.")
    ]
    add_bullets(s2, 7.0, 4.75, 5.2, 1.8, api_bullets, font_size=10.5, space_after=5)

    set_notes(s2, (
        "VIDEO PRESENTER SCRIPT (SLIDE 2 - ARCHITECTURE & API / 45s):\n"
        "\"Slide 2 breaks down our core foundation.\n"
        "Our overall architecture is structured as a 5-layer pipeline: an incoming request hits our Rate Limiter, moves to Cryptographic "
        "Authentication, is sanitized by Dual Guardrails, mapped by the Intent Router, verified against RBAC permissions, and executed.\n\n"
        "On the technology side, we use Python 3.14 with FastAPI and Uvicorn for asynchronous performance, Pydantic V2 for strict modeling, "
        "and NVIDIA NIM running Meta Llama-Guard-4-12B for AI safety.\n\n"
        "Our API design is simple and hardened: a single POST /ask endpoint. We configure extra='forbid' in Pydantic to stop parameter smuggling, "
        "and we override the default 422 error handler so the server never reflects untrusted input back to the user.\""
    ))

    # =========================================================================
    # SLIDE 3: Auth Mechanism, RBAC & Business Actions
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "Authentication, Authorization & Business Actions", "SECURITY & GOVERNANCE", 3)

    # 3 Column Layout
    col_w = 3.65

    # Col 1: Authentication Mechanism
    add_card(s3, 0.9, 1.5, col_w, 5.2, title="1. Authentication Mechanism", title_color=BORDER_CYAN, border_color=BORDER_CYAN)
    auth_bullets = [
        ("No Plaintext Key Storage", "Keys are hashed at startup using SHA-256. Memory stores non-reversible digests only."),
        ("Constant-Time HMAC", "hmac.compare_digest(stored, candidate) neutralizes timing side-channel attacks."),
        ("Zero Raw Key Logging", "Raw keys are never written to disk. Logs record only a safe 8-char SHA-256 fingerprint (e.g. 'a6f632a6')."),
        ("Clean 401 Rejection", "Invalid keys write an 'auth_failed' audit entry and return 401 Unauthorized.")
    ]
    add_bullets(s3, 1.05, 2.15, 3.35, 4.3, auth_bullets, font_size=11, space_after=10)

    # Col 2: Authorization Flow (RBAC)
    add_card(s3, 4.85, 1.5, col_w, 5.2, title="2. Authorization Flow (RBAC)", title_color=BORDER_EMERALD, border_color=BORDER_EMERALD)
    rbac_bullets = [
        ("Least Privilege", "Users possess strictly scoped roles: 'analyst' vs. 'admin'."),
        ("Analyst Permissions", "Allowed: sales_report, create_ticket, fallback.\nBlocked: employee_info."),
        ("Admin Permissions", "Allowed: sales_report, create_ticket, employee_info (executive directory access), fallback."),
        ("Strict 403 Forbidden", "Analyst accessing employee_info is blocked with 403 Forbidden and logged as 'forbidden'.")
    ]
    add_bullets(s3, 5.0, 2.15, 3.35, 4.3, rbac_bullets, font_size=11, space_after=10)

    # Col 3: Business Actions
    add_card(s3, 8.8, 1.5, col_w, 5.2, title="3. Business Actions Implemented", title_color=BORDER_AMBER, border_color=BORDER_AMBER)
    biz_bullets = [
        ("sales_report", "Returns weekly revenue, orders, AOV, regional breakdown, and executive summary."),
        ("create_ticket", "Creates support tickets in an in-memory list with unique IDs (e.g. TICK-0001)."),
        ("employee_info", "Directory lookup for corporate personnel (Admin-only)."),
        ("fallback", "Helpful natural guidance for unsupported queries.")
    ]
    add_bullets(s3, 8.95, 2.15, 3.35, 4.3, biz_bullets, font_size=11, space_after=10)

    set_notes(s3, (
        "VIDEO PRESENTER SCRIPT (SLIDE 3 - AUTH, RBAC, ACTIONS / 45s):\n"
        "\"Slide 3 highlights our identity and access governance.\n"
        "First, our Authentication Mechanism eliminates three major risks: we store zero plaintext keys in memory by hashing with SHA-256; "
        "we verify keys in constant time using hmac.compare_digest to prevent timing attacks; and we never log raw keys, logging only "
        "an 8-character SHA-256 fingerprint for forensic correlation.\n\n"
        "Second, our Authorization Flow implements Role-Based Access Control. Analysts can generate sales reports and submit support tickets, "
        "but employee personnel records are restricted to administrators. When an analyst queries employee info, the system immediately returns "
        "403 Forbidden.\n\n"
        "Third, our Business Actions deliver real mock enterprise utilities: sales reports with regional breakdowns, support ticket generation, "
        "and corporate directory lookups.\""
    ))

    # =========================================================================
    # SLIDE 4: AI Workflow & Security Improvements
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "AI Safety Workflow & Security Hardening", "PROTECTION", 4)

    # Left: AI Workflow
    add_card(s4, 0.9, 1.5, 5.6, 5.2, title="1. AI Workflow & Guardrails", title_color=BORDER_VIOLET, border_color=BORDER_VIOLET)
    ai_bullets = [
        ("Dual-Tier Shield", "Combines high-speed local regex filters with external neural AI safety classification."),
        ("Tier 1: Sub-Millisecond Regex", "Instantly filters known injection patterns: 'ignore previous instructions', 'reveal system prompt', and SQL injection 'union select', 'drop table'."),
        ("Tier 2: Meta Llama-Guard-4-12B", "Cloud inference via NVIDIA NIM evaluates semantic prompt safety across 14 safety categories."),
        ("Non-Blocking Execution", "External NIM calls are offloaded via asyncio.to_thread to keep FastAPI's async event loop responsive.")
    ]
    add_bullets(s4, 1.1, 2.15, 5.2, 4.3, ai_bullets, font_size=11.5, space_after=12)

    # Right: Security Improvements
    add_card(s4, 6.8, 1.5, 5.6, 5.2, title="2. Key Security Improvements Implemented", title_color=BORDER_EMERALD, border_color=BORDER_EMERALD)
    sec_bullets = [
        ("Secrets Decoupling (.env)", "Eliminated all hardcoded API keys from code. All keys load dynamically from .env, protected by .gitignore, with a safe .env.example."),
        ("Sliding-Window Rate Limiting", "Thread-safe sliding window tracking per client IP (5 req / 60s). Drops DoS bursts with 429 Too Many Requests."),
        ("Tamper-Evident Audit Logging", "Structured JSON Lines stream to audit.log with UTC timestamps, event types, user identities, roles, and client IPs."),
        ("Global Zero-Traceback Catch-All", "Catches unhandled exceptions, emits 'server_error', and returns a minimal 500 without leaking stack traces.")
    ]
    add_bullets(s4, 7.0, 2.15, 5.2, 4.3, sec_bullets, font_size=11.5, space_after=12)

    set_notes(s4, (
        "VIDEO PRESENTER SCRIPT (SLIDE 4 - AI & SECURITY IMPROVEMENTS / 45s):\n"
        "\"Slide 4 covers our AI Safety Workflow and Security Hardening.\n"
        "Our AI workflow uses a dual-tier approach: Tier 1 is a local regex filter that stops common prompt injections in microseconds. "
        "Tier 2 connects to Meta Llama-Guard-4-12B on NVIDIA NIM to evaluate deep semantic safety. To prevent network latency from blocking "
        "concurrent requests, we run the guardrail call inside asyncio.to_thread.\n\n"
        "We also implemented several critical security improvements: we decoupled all credentials into a gitignored .env file; "
        "we built an in-memory sliding window rate limiter enforcing 5 requests per minute; we structured all audit events into JSON Lines; "
        "and we registered a global exception handler that prevents stack trace leaks.\""
    ))

    # =========================================================================
    # SLIDE 5: The Bug Story: Diagnosis & Resolution
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Incident Post-Mortem: The Llama-Guard RBAC Bug", "DEBUGGING & INCIDENT RESOLUTION", 5)

    # 4 Sequential Cards
    bug_steps = [
        ("1. Symptoms", [
            "Test 2.3 failed: 'Lookup employee info for Alice' returned HTTP 400 Bad Request instead of expected 403 Forbidden.",
            "Admin users were completely blocked from accessing employee directory queries (also returned 400)."
        ], BORDER_ROSE),
        ("2. Root Cause", [
            "Meta Llama-Guard classifies employee lookups as 'unsafe\\nS7' (Category S7: Privacy / PII).",
            "Because the guardrail ran BEFORE RBAC and treated any unsafe response as a prompt attack, it blanket-blocked legitimate lookups."
        ], BORDER_AMBER),
        ("3. How Diagnosed", [
            "Isolated the NVIDIA NIM API endpoint using standalone curl and Python scripts.",
            "Inspected exact model response body: confirmed 'unsafe\\nS7'. Traced audit.log which recorded 'injection_blocked' prematurely."
        ], BORDER_CYAN),
        ("4. How Resolved", [
            "Updated verify_ai_guardrail to parse specific Llama-Guard categories.",
            "If the flag is solely S7 (Privacy), the gateway delegates authorization to RBAC. Admins get 200 OK; Analysts get 403 Forbidden!"
        ], BORDER_EMERALD)
    ]

    for idx, (b_title, b_items, col) in enumerate(bug_steps):
        row = idx // 2
        c_idx = idx % 2
        c_left = 0.9 + (c_idx * 5.9)
        c_top = 1.6 + (row * 2.65)

        card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(c_top), Inches(5.6), Inches(2.45))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = col
        card.line.width = Pt(1.5)

        tb = s5.shapes.add_textbox(Inches(c_left + 0.2), Inches(c_top + 0.15), Inches(5.2), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = b_title
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = col
        p_t.space_after = Pt(6)

        for item in b_items:
            p_i = tf.add_paragraph()
            p_i.text = f"•  {item}"
            p_i.font.name = "Segoe UI"
            p_i.font.size = Pt(11)
            p_i.font.color.rgb = TEXT_MUTED
            p_i.space_after = Pt(4)

    set_notes(s5, (
        "VIDEO PRESENTER SCRIPT (SLIDE 5 - THE BUG STORY / 60s):\n"
        "\"Now I want to walk you through a critical real-world incident we diagnosed and resolved.\n\n"
        "SYMPTOMS: When executing our automated test suite, Test 2.3—where an analyst asks for employee info—unexpectedly returned "
        "HTTP 400 Bad Request instead of 403 Forbidden. Worse, when an authorized admin queried the employee directory, they were also "
        "blocked with 400 Bad Request!\n\n"
        "ROOT CAUSE: We discovered that Meta Llama Guard has 14 safety categories. Category S7 is Privacy/PII. When someone asks 'Lookup employee info for Alice', "
        "Llama Guard flags it as unsafe under S7. Because our guardrail ran before the Intent Router and treated any unsafe response as an injection attack, "
        "it blocked the request before RBAC could even evaluate it.\n\n"
        "HOW WE DIAGNOSED IT: We called the NVIDIA NIM endpoint in isolation and inspected the raw response. We saw 'unsafe\\nS7'. Looking at audit.log, "
        "we noticed 'injection_blocked' was triggering instead of 'forbidden'.\n\n"
        "HOW WE RESOLVED IT: We refactored the guardrail parser. When Llama Guard flags solely category S7, the gateway permits the request to proceed "
        "to the RBAC layer. If the user is an analyst, RBAC stops them with 403 Forbidden. If the user is an admin, they receive the employee record with 200 OK. "
        "This completely restored proper role governance!\""
    ))

    # =========================================================================
    # SLIDE 6: Tradeoff Discussion (Performance vs Protection & Usability)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Architectural Tradeoffs (1–2 Minute Discussion)", "TRADEOFF ANALYSIS", 6)

    # 2 Main Tradeoff Cards
    add_card(s6, 0.9, 1.5, 5.6, 5.2, title="Tradeoff 1: Performance vs. Protection", title_color=BORDER_AMBER, border_color=BORDER_AMBER)
    t1_bullets = [
        ("The Dilemma", "Calling external neural guardrails (Llama-Guard NIM) adds ~150-250ms of network latency per request compared to sub-millisecond local regex."),
        ("The Risk", "Synchronous HTTP calls inside async FastAPI routes block the entire event loop, destroying server concurrency."),
        ("Our Architectural Choice", "1. Hybrid Execution: Local regex filters obvious syntax attacks instantly.\n2. Non-Blocking I/O: External NIM call offloaded via asyncio.to_thread.\n3. Fail-Open with Observability: Network timeouts fall back safely to local rules to protect availability."),
        ("The Verdict", "We accepted small semantic evaluation latency in exchange for enterprise-grade defense against sophisticated jailbreaks.")
    ]
    add_bullets(s6, 1.1, 2.15, 5.2, 4.3, t1_bullets, font_size=11, space_after=10)

    add_card(s6, 6.8, 1.5, 5.6, 5.2, title="Tradeoff 2: Security vs. Usability (PII & RBAC)", title_color=BORDER_CYAN, border_color=BORDER_CYAN)
    t2_bullets = [
        ("The Dilemma", "A zero-tolerance AI safety guardrail would blanket-ban all prompts mentioning employee names or directory lookups (Category S7)."),
        ("The Usability Impact", "Legitimate business functions (HR directory, staff lookup for admins) become completely unusable."),
        ("Our Architectural Choice", "Instead of a blunt firewall drop, we delegated Privacy (S7) governance to the Role-Based Access Control layer."),
        ("The Verdict", "Security must enable the business, not paralyze it. Admins get seamless usability; analysts remain strictly contained.")
    ]
    add_bullets(s6, 7.0, 2.15, 5.2, 4.3, t2_bullets, font_size=11, space_after=10)

    set_notes(s6, (
        "VIDEO PRESENTER SCRIPT (SLIDE 6 - TRADEOFF DISCUSSION / 60–90s):\n"
        "\"To wrap up our technical evaluation, let's discuss the key engineering tradeoffs we made.\n\n"
        "Our primary tradeoff was Performance vs. Protection. Running an external neural model like Meta Llama Guard introduces roughly "
        "200 milliseconds of network overhead. If implemented naively, calling an external synchronous API inside an async FastAPI route "
        "freezes the entire Python event loop, grinding concurrent traffic to a halt.\n"
        "We resolved this with a hybrid approach: local regex stops known attacks in microseconds without network calls, and the external "
        "AI guardrail is offloaded into a worker thread using asyncio.to_thread. If the external NIM API times out, it gracefully falls back "
        "to local rules, maintaining high availability.\n\n"
        "Our second tradeoff was Security vs. Usability. Strict safety filters treat asking for employee details as a privacy violation. "
        "If we left it at that, authorized administrators couldn't do their jobs. By delegating S7 privacy evaluations to RBAC rather than "
        "treating it as an attack, we achieved both: complete protection against unauthorized staff and seamless usability for administrators.\n\n"
        "This proves that effective enterprise AI engineering is about defense-in-depth, clear boundaries, and balanced tradeoffs. "
        "Thank you for watching!\""
    ))

    output_path = "/home/ubuntu/fluid_ai/Executive_Presentation.pptx"
    prs.save(output_path)
    print(f"Executive presentation created at: {output_path}")

if __name__ == "__main__":
    create_rubric_deck()
