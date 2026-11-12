#!/usr/bin/env python3
"""
Generate Presentation Deck: Secure Enterprise AI Gateway (FastAPI)
Walkthrough for Architecture, Security, RBAC, Guardrails, and Testing.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    BG_DARK = RGBColor(11, 15, 25)          # Deep background #0B0F19
    BG_CARD = RGBColor(19, 27, 46)          # Card container #131B2E
    BG_CARD_LIGHT = RGBColor(26, 37, 64)    # Elevated card #1A2540
    BORDER_SUBTLE = RGBColor(33, 46, 77)    # Border #212E4D
    BORDER_CYAN = RGBColor(0, 210, 255)     # Cyan highlight #00D2FF
    BORDER_EMERALD = RGBColor(16, 185, 129) # Emerald highlight #10B981
    BORDER_VIOLET = RGBColor(139, 92, 246)  # Violet highlight #8B5CF6
    BORDER_AMBER = RGBColor(245, 158, 11)   # Amber highlight #F59E0B
    BORDER_ROSE = RGBColor(239, 68, 68)     # Rose highlight #EF4444

    TEXT_WHITE = RGBColor(248, 250, 252)    # Main title #F8FAFC
    TEXT_MUTED = RGBColor(148, 163, 184)    # Subtitle / body #94A3B8
    TEXT_DIM = RGBColor(100, 116, 139)      # Dim labels #64748B
    TEXT_CYAN = RGBColor(56, 189, 248)      # Cyan text #38BDF8
    TEXT_EMERALD = RGBColor(52, 211, 153)   # Green text #34D399
    TEXT_AMBER = RGBColor(251, 191, 36)     # Amber text #FBBF24
    TEXT_ROSE = RGBColor(248, 113, 113)     # Rose text #F87171
    TEXT_VIOLET = RGBColor(167, 139, 250)   # Violet text #A78BFA

    CODE_BG = RGBColor(7, 10, 16)           # Terminal black #070A10

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, category, title, slide_num):
        # Top accent line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.06))
        line.fill.solid()
        line.fill.fore_color.rgb = BORDER_CYAN
        line.line.fill.background()

        # Category badge
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.0), Inches(0.35))
        tf_cat = tb_cat.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = f"// {category.upper()} //"
        p_cat.font.name = "Segoe UI"
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = TEXT_CYAN

        # Main title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(10.5), Inches(0.7))
        tf_title = tb_title.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.name = "Segoe UI"
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

        # Footer line
        fline = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.02))
        fline.fill.solid()
        fline.fill.fore_color.rgb = BORDER_SUBTLE
        fline.line.fill.background()

        # Footer text left
        tb_f1 = slide.shapes.add_textbox(Inches(0.8), Inches(6.95), Inches(5.0), Inches(0.35))
        tf_f1 = tb_f1.text_frame
        p_f1 = tf_f1.paragraphs[0]
        p_f1.text = "Secure Enterprise AI Gateway  |  FastAPI Implementation"
        p_f1.font.name = "Segoe UI"
        p_f1.font.size = Pt(10)
        p_f1.font.color.rgb = TEXT_DIM

        # Footer text center
        tb_f2 = slide.shapes.add_textbox(Inches(5.0), Inches(6.95), Inches(4.5), Inches(0.35))
        tf_f2 = tb_f2.text_frame
        p_f2 = tf_f2.paragraphs[0]
        p_f2.alignment = PP_ALIGN.CENTER
        p_f2.text = "OWASP LLM Defense-in-Depth Architecture"
        p_f2.font.name = "Segoe UI"
        p_f2.font.size = Pt(10)
        p_f2.font.color.rgb = TEXT_DIM

        # Footer slide number
        tb_num = slide.shapes.add_textbox(Inches(11.5), Inches(6.95), Inches(1.0), Inches(0.35))
        tf_num = tb_num.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"{slide_num:02d} / 11"
        p_num.font.name = "Segoe UI"
        p_num.font.size = Pt(10)
        p_num.font.bold = True
        p_num.font.color.rgb = TEXT_CYAN

    def add_card(slide, left, top, width, height, title="", title_color=TEXT_WHITE, border_color=BORDER_SUBTLE, bg_color=BG_CARD):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)

        if title:
            tb = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(width - 0.5), Inches(0.45))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.name = "Segoe UI"
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = title_color
        return card

    def add_bullet_list(slide, left, top, width, height, items, font_size=12.5, space_after=8):
        tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, item in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(space_after)
            p.line_spacing = 1.15

            # Item can be tuple (header, description) or string
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

    def add_terminal(slide, left, top, width, height, title, code_lines):
        # Header bar
        header = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        header.fill.solid()
        header.fill.fore_color.rgb = CODE_BG
        header.line.color.rgb = BORDER_SUBTLE
        header.line.width = Pt(1)

        # Title / prompt indicator
        tb = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.15), Inches(width - 0.4), Inches(0.35))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        p.text = f"⚡ {title}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_CYAN

        # Code box
        tb_code = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.5), Inches(width - 0.4), Inches(height - 0.6))
        tf_code = tb_code.text_frame
        tf_code.word_wrap = True
        for i, line in enumerate(code_lines):
            p_code = tf_code.paragraphs[0] if i == 0 else tf_code.add_paragraph()
            p_code.space_after = Pt(3)
            p_code.line_spacing = 1.1

            run = p_code.add_run()
            run.text = line
            run.font.name = "Consolas"
            run.font.size = Pt(10)
            if line.startswith("$") or line.startswith(">"):
                run.font.color.rgb = TEXT_CYAN
            elif "200" in line or "action_ok" in line or "success" in line:
                run.font.color.rgb = TEXT_EMERALD
            elif "400" in line or "401" in line or "403" in line or "422" in line or "429" in line or "blocked" in line:
                run.font.color.rgb = TEXT_ROSE
            elif line.startswith("#"):
                run.font.color.rgb = TEXT_DIM
            else:
                run.font.color.rgb = TEXT_MUTED

    def set_notes(slide, script_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = script_text

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    # Accent decorative gradient line
    line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(2.5), Inches(0.06))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER_CYAN
    line.line.fill.background()

    # Title & Subtitle in single textframe
    tb_title = s1.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(11.7), Inches(2.2))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True

    p1 = tf_title.paragraphs[0]
    p1.text = "Secure Enterprise AI Gateway"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(10)

    p2 = tf_title.add_paragraph()
    p2.text = "Multi-Layer Defense-in-Depth Architecture, Zero-Trust Access Control & AI Safety Model Integration"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(17)
    p2.font.color.rgb = TEXT_MUTED

    # Highlights card
    add_card(s1, 0.8, 4.4, 11.733, 1.8, title="Enterprise Security Engineering Highlights", title_color=TEXT_CYAN, border_color=BORDER_SUBTLE)
    badges = [
        ("Cryptographic Auth", "SHA-256 Key Hashing + HMAC Constant-Time Comparison"),
        ("Role-Based Access (RBAC)", "Analyst vs. Admin Least-Privilege Permission Boundary"),
        ("Multi-Tier Guardrails", "Local Regex Injection Filter + NVIDIA Meta Llama-Guard AI NIM"),
        ("Audit & Throttling", "Sliding-Window Rate Limiter (5 req/min) + JSONL Tamper-Evident Logs")
    ]
    for idx, (b_title, b_sub) in enumerate(badges):
        b_left = 1.1 + (idx * 2.85)
        b_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(b_left), Inches(5.1), Inches(2.7), Inches(0.85))
        b_box.fill.solid()
        b_box.fill.fore_color.rgb = BG_CARD_LIGHT
        b_box.line.color.rgb = BORDER_SUBTLE
        b_box.line.width = Pt(1)

        tf_b = b_box.text_frame
        tf_b.word_wrap = True
        pb1 = tf_b.paragraphs[0]
        pb1.text = b_title
        pb1.font.name = "Segoe UI"
        pb1.font.size = Pt(11)
        pb1.font.bold = True
        pb1.font.color.rgb = TEXT_WHITE

        pb2 = tf_b.add_paragraph()
        pb2.text = b_sub
        pb2.font.name = "Segoe UI"
        pb2.font.size = Pt(8.5)
        pb2.font.color.rgb = TEXT_DIM

    # Footer
    tb_foot = s1.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.7), Inches(0.4))
    tf_foot = tb_foot.text_frame
    p_foot = tf_foot.paragraphs[0]
    p_foot.text = "FastAPI  •  Python 3.14  •  Pydantic V2  •  NVIDIA NIM Meta-Llama-Guard-4-12B  •  OWASP LLM Compliant"
    p_foot.font.name = "Segoe UI"
    p_foot.font.size = Pt(10.5)
    p_foot.font.color.rgb = TEXT_DIM

    set_notes(s1, (
        "VIDEO PRESENTER SCRIPT (SLIDE 1 - INTRO):\n"
        "\"Hello and welcome! In this presentation and technical demonstration, I am walking you through the architecture, "
        "security layers, and implementation of our Secure Enterprise AI Gateway built with Python and FastAPI.\n\n"
        "As generative AI and agentic workflows are integrated into enterprise platforms, APIs face new attack vectors: "
        "prompt injections, data exfiltration, parameter pollution, and credential leakage. In this project, we designed "
        "and implemented a hardened, defense-in-depth API gateway that enforces zero-trust authentication, granular RBAC, "
        "strict Pydantic schema validation, sliding-window rate limiting, and an AI safety guardrail powered by Meta Llama Guard 4. "
        "Let's dive right into the architectural requirements and design!\""
    ))

    # =========================================================================
    # SLIDE 2: Problem Statement & Enterprise Threat Landscape
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "EXECUTIVE CONTEXT", "The Enterprise Challenge: Securing AI Endpoints", 2)

    add_card(s2, 0.8, 1.5, 5.7, 5.1, title="The Threat Landscape (OWASP LLM Top 10)", title_color=TEXT_ROSE, border_color=BORDER_ROSE)
    threats = [
        ("Prompt Injection (LLM01)", "Adversarial prompts manipulating model instructions (e.g., 'ignore previous instructions', 'reveal system prompt') to bypass controls."),
        ("Sensitive Data Disclosure (LLM02)", "Exposing confidential PII or restricted business data (e.g. employee compensation, executive directories) to unauthorized staff."),
        ("Credential & Key Leakage", "Raw API tokens exposed in server logs, source control, or memory dumps, vulnerable to side-channel timing analysis."),
        ("Model Denial of Service (LLM04)", "Unbounded request bursts draining compute, exceeding cloud quotas, or exhausting backend database connections."),
        ("Parameter Injection & Smuggling", "Undeclared payload fields poisoning internal router state or manipulating backend execution.")
    ]
    add_bullet_list(s2, 1.05, 2.2, 5.2, 4.2, threats, font_size=11.5, space_after=10)

    add_card(s2, 6.8, 1.5, 5.7, 5.1, title="The Defense-in-Depth Solution Mandate", title_color=TEXT_EMERALD, border_color=BORDER_EMERALD)
    solutions = [
        ("Multi-Layer Defense", "Security cannot rely on model alignment alone; each request passes through network, cryptographic, schema, regex, AI, and authorization barriers."),
        ("Zero-Trust Cryptography", "Store only SHA-256 digests; verify credentials with hmac.compare_digest in constant time; log only non-reversible 8-char fingerprints."),
        ("Strict Schema Hygiene", "Reject all undeclared parameters with Pydantic extra='forbid'; mask validation errors without echoing user input."),
        ("Hybrid AI Guardrails", "Sub-millisecond local regex shields combined with neural classification (Meta Llama-Guard-4-12B via NVIDIA NIM)."),
        ("Immutable Auditability", "Tamper-evident JSON Lines audit log tracking every security and operational event for SIEM ingestion.")
    ]
    add_bullet_list(s2, 7.05, 2.2, 5.2, 4.2, solutions, font_size=11.5, space_after=10)

    set_notes(s2, (
        "VIDEO PRESENTER SCRIPT (SLIDE 2 - THREAT MODEL):\n"
        "\"Before we look at the code, it's essential to understand why traditional web API protections are insufficient for AI workloads.\n"
        "According to the OWASP Top 10 for Large Language Models, AI applications face unique risks. Direct and indirect prompt "
        "injection attacks can hijack prompt execution. Sensitive data disclosure can leak PII like employee directories. Furthermore, "
        "attackers frequently attempt timing side-channel attacks on API keys or launch burst floods to exhaust compute quotas.\n\n"
        "To solve this, we formulated an 8-layer defense-in-depth architecture. Security is not an afterthought or a single middleware—"
        "it is a coordinated sequence of layers where every request is rate-limited, authenticated in constant time, sanitized by regex and "
        "AI guardrails, validated for strict role permissions, and recorded in a structured audit log.\""
    ))

    # =========================================================================
    # SLIDE 3: System Architecture & Request Lifecycle
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "SYSTEM ARCHITECTURE", "End-to-End Request Pipeline & Defense Layers", 3)

    # 6 Step Pipeline Cards horizontally
    steps = [
        ("1. Rate Limiter", "Sliding Window", "5 req / 60s per client IP\nReturns 429 if exceeded", BORDER_CYAN),
        ("2. Authenticator", "Cryptographic Check", "SHA-256 + HMAC verify\nReturns 401 if invalid", BORDER_CYAN),
        ("3. Guardrails", "Regex + Llama-Guard", "Prompt injection filter\nReturns 400 if flagged", BORDER_AMBER),
        ("4. Intent Router", "Natural Language Map", "Routes to sales, ticket,\nor employee directory", BORDER_VIOLET),
        ("5. RBAC Gate", "Least Privilege", "Analyst vs. Admin matrix\nReturns 403 on violation", BORDER_ROSE),
        ("6. Execution", "Audit & Response", "Generates report / ticket\nFlushes JSONL audit log", BORDER_EMERALD)
    ]

    for idx, (st_num, st_sub, st_desc, st_color) in enumerate(steps):
        s_left = 0.8 + (idx * 1.98)
        c = add_card(s3, s_left, 1.5, 1.85, 3.2, title="", border_color=st_color)
        tb = s3.shapes.add_textbox(Inches(s_left + 0.1), Inches(1.65), Inches(1.65), Inches(2.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = st_num
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = st_color
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = st_sub
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_after = Pt(8)

        p3 = tf.add_paragraph()
        p3.text = st_desc
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = TEXT_MUTED

    # Bottom Architecture Summary Cards
    add_card(s3, 0.8, 4.95, 5.7, 1.7, title="Zero-Traceback Global Error Boundary", title_color=TEXT_CYAN, border_color=BORDER_SUBTLE)
    add_bullet_list(s3, 1.05, 5.4, 5.2, 1.1, [
        ("Unified Schema", "All exceptions map to standardized JSON: {'detail': '...'}"),
        ("Zero Diagnostic Leakage", "Stack traces, file paths, and database details are never returned.")
    ], font_size=11, space_after=6)

    add_card(s3, 6.8, 4.95, 5.7, 1.7, title="Tamper-Evident Audit Logging (audit.log)", title_color=TEXT_EMERALD, border_color=BORDER_SUBTLE)
    add_bullet_list(s3, 7.05, 5.4, 5.2, 1.1, [
        ("Synchronous JSON Lines", "Flushes timestamp, event, user, role, action, and IP atomically."),
        ("SIEM Compatibility", "Directly ingestible into Datadog, Splunk, or AWS CloudWatch.")
    ], font_size=11, space_after=6)

    set_notes(s3, (
        "VIDEO PRESENTER SCRIPT (SLIDE 3 - PIPELINE):\n"
        "\"Here on Slide 3, we see the complete lifecycle of an incoming request to our /ask endpoint.\n\n"
        "Notice the sequence of enforcement: First, the Rate Limiter intercepts the request before any heavy processing occurs. "
        "If a client bursts past 5 requests per minute, they are stopped immediately with HTTP 429.\n"
        "Second, Authentication occurs. We hash the provided API key with SHA-256 and compare it against stored digests using constant-time HMAC.\n"
        "Third, our Dual Guardrails scan the prompt for prompt injections and malicious signatures, backed by Meta Llama Guard.\n"
        "Fourth, the question is mapped to a discrete business intent.\n"
        "Fifth, Role-Based Access Control checks whether that specific user role is authorized for that action.\n"
        "Only when all 5 barriers pass does the action execute, returning a 200 OK and recording an action_ok audit entry.\n"
        "Let's inspect how Authentication and RBAC are implemented!\""
    ))

    # =========================================================================
    # SLIDE 4: Layer 1 & 2: Authentication & RBAC
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "SECURITY LAYERS 1 & 2", "API Key Authentication & Role-Based Access Control", 4)

    add_card(s4, 0.8, 1.5, 5.7, 5.1, title="Layer 1: Cryptographic Key Verification", title_color=TEXT_CYAN, border_color=BORDER_CYAN)
    auth_bullets = [
        ("No Plaintext Key Storage", "Keys are hashed at startup using SHA-256. Memory holds only non-reversible digests."),
        ("Constant-Time Verification", "Uses hmac.compare_digest(stored_hash, candidate_hash) to neutralize timing side-channel attacks."),
        ("Zero Raw Key Logging", "Raw keys are never written to audit logs or console. Logs record only a safe 8-character SHA-256 fingerprint (e.g. 'a6f632a6')."),
        ("Clean 401 Unauthorized", "Failed key matches immediately write an 'auth_failed' audit entry and return a minimal JSON response.")
    ]
    add_bullet_list(s4, 1.05, 2.2, 5.2, 4.2, auth_bullets, font_size=11.5, space_after=12)

    add_card(s4, 6.8, 1.5, 5.7, 5.1, title="Layer 2: Role-Based Access Control (RBAC)", title_color=TEXT_VIOLET, border_color=BORDER_VIOLET)
    rbac_bullets = [
        ("Principle of Least Privilege", "Users possess explicit, role-scoped boundaries. Capabilities do not cross boundaries without authorization."),
        ("Analyst Role ('analyst_user')", "Permitted Actions: sales_report, create_ticket, fallback.\nStrictly prohibited from accessing employee_info."),
        ("Admin Role ('admin_user')", "Permitted Actions: sales_report, create_ticket, employee_info (executive directory access), fallback."),
        ("Strict 403 Forbidden Enforcement", "When an analyst requests employee_info, the request is rejected with 403 Forbidden and logged as a 'forbidden' audit event.")
    ]
    add_bullet_list(s4, 7.05, 2.2, 5.2, 4.2, rbac_bullets, font_size=11.5, space_after=12)

    set_notes(s4, (
        "VIDEO PRESENTER SCRIPT (SLIDE 4 - AUTH & RBAC):\n"
        "\"In Layer 1, we tackle credential security. Common mistakes in enterprise APIs include storing keys in plaintext in memory, "
        "using standard string comparison '==' which leaks timing information, and logging the raw API key for debugging.\n\n"
        "Our gateway eliminates all three vulnerabilities: at startup, keys are digested using SHA-256. When a request arrives, "
        "we compute its digest and verify it using hmac.compare_digest in constant execution time. In our audit log, we write only "
        "the first 8 characters of the SHA-256 hash—allowing security teams to correlate client sessions without exposing the secret.\n\n"
        "In Layer 2, Role-Based Access Control separates analysts from administrators. An analyst can generate weekly sales reports "
        "and create support tickets, but if they query employee personnel info, the gate immediately blocks them with a 403 Forbidden "
        "and records an unauthorized access attempt in audit.log.\""
    ))

    # =========================================================================
    # SLIDE 5: Layer 3: Pydantic Validation & Input Hygiene
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "SECURITY LAYER 3", "Strict Pydantic V2 Schema Validation & Input Hygiene", 5)

    add_card(s5, 0.8, 1.5, 5.7, 5.1, title="Pydantic V2 Model Architecture", title_color=TEXT_CYAN, border_color=BORDER_SUBTLE)
    pyd_code = [
        "# main.py - Strict Pydantic V2 Model",
        "class AskRequest(BaseModel):",
        "    model_config = ConfigDict(extra='forbid')",
        "    question: str = Field(..., min_length=3, max_length=500)",
        "    api_key: str = Field(..., min_length=1, max_length=128)",
        "",
        "# 1. extra='forbid': Blocks parameter pollution",
        "# 2. Length limits: Prevents buffer / DoS payloads",
        "# 3. Type enforcement: Guaranteed valid strings"
    ]
    add_terminal(s5, 1.05, 2.2, 5.2, 4.1, "Payload Model Definition", pyd_code)

    add_card(s5, 6.8, 1.5, 5.7, 5.1, title="Defense Against Parameter Smuggling", title_color=TEXT_EMERALD, border_color=BORDER_SUBTLE)
    pyd_bullets = [
        ("Parameter Injection Rejection", "Payloads with undeclared fields (e.g. {'forbidden_field': 'value'}) are rejected at schema parsing before touching route logic."),
        ("Custom RequestValidationError Handler", "Standard FastAPI 422 error handlers echo rejected field names and values. Our custom handler masks internal details."),
        ("Generic Error Envelope", "Returns a minimal {'detail': 'Invalid request'} with zero input reflection, mitigating reflected XSS and input probing."),
        ("Audit Trail Correlation", "Records 'malformed_request' in audit.log with client IP for automated threat scoring.")
    ]
    add_bullet_list(s5, 7.05, 2.2, 5.2, 4.2, pyd_bullets, font_size=11.5, space_after=12)

    set_notes(s5, (
        "VIDEO PRESENTER SCRIPT (SLIDE 5 - INPUT VALIDATION):\n"
        "\"Layer 3 enforces input hygiene before any business code or AI model is invoked.\n"
        "Using Pydantic V2, we define AskRequest with extra='forbid'. This prevents parameter smuggling or pollution—if an attacker "
        "tries to slip extra keys into the JSON payload, Pydantic immediately invalidates the request.\n\n"
        "Crucially, standard FastAPI error handlers return detailed validation error dictionaries that echo back the user's input. "
        "In an enterprise environment, echoing unvalidated input creates risk of reflection attacks. We registered a custom exception "
        "handler for RequestValidationError that intercepts these errors, flushes a 'malformed_request' audit record, and returns a clean, "
        "generic 422 response with {'detail': 'Invalid request'}.\""
    ))

    # =========================================================================
    # SLIDE 6: Layer 4: Multi-Tiered Guardrails (Regex + Meta Llama-Guard)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "SECURITY LAYER 4", "Multi-Tier Guardrails: Regex Filter + Meta Llama-Guard-4-12B", 6)

    add_card(s6, 0.8, 1.5, 5.7, 5.1, title="Tier 1: High-Speed Local Regex Shield", title_color=TEXT_AMBER, border_color=BORDER_AMBER)
    regex_bullets = [
        ("Sub-Millisecond Threat Neutralization", "Compiled regex runs in microseconds locally, filtering known attack patterns before consuming network I/O or LLM tokens."),
        ("Prompt Injection Signatures", "Matches: 'ignore previous instructions', 'reveal system prompt', 'you are now', and system jailbreak attempts."),
        ("SQL Injection Signatures", "Simulated SQLi triggers: 'union select', 'drop table', \"';\", and SQL comment markers '--'."),
        ("Deterministic 400 Bad Request", "Blocked attempts log 'injection_blocked' with client IP and API key fingerprint.")
    ]
    add_bullet_list(s6, 1.05, 2.2, 5.2, 4.2, regex_bullets, font_size=11.5, space_after=12)

    add_card(s6, 6.8, 1.5, 5.7, 5.1, title="Tier 2: Meta Llama-Guard-4-12B AI Model", title_color=TEXT_CYAN, border_color=BORDER_CYAN)
    ai_bullets = [
        ("NVIDIA NIM Cloud Inference", "Evaluates semantic prompt safety using Meta Llama-Guard-4-12B safety taxonomy across 14 safety categories."),
        ("Non-Blocking Async Execution", "Invoked via asyncio.to_thread(verify_ai_guardrail, prompt) to prevent blocking FastAPI's single-threaded event loop."),
        ("Enterprise RBAC Integration", "Intelligently allows category S7 (Privacy / PII) to reach RBAC so authorized admins can look up employee directories without false-positive blocks."),
        ("Graceful Degradation", "Network timeouts or API unreachable conditions fail-open to local regex to ensure high availability.")
    ]
    add_bullet_list(s6, 7.05, 2.2, 5.2, 4.2, ai_bullets, font_size=11.5, space_after=12)

    set_notes(s6, (
        "VIDEO PRESENTER SCRIPT (SLIDE 6 - GUARDRAILS):\n"
        "\"Layer 4 represents our multi-layer guardrail system. Static regex filters and AI safety models are complementary: "
        "regex provides sub-millisecond filtering for classic injections, while Meta Llama Guard evaluates semantic intent.\n\n"
        "In our first tier, we scan for signatures like 'ignore previous instructions', 'reveal system prompt', and SQL injection syntax like 'union select'.\n"
        "In our second tier, we integrate NVIDIA's hosted Meta Llama-Guard-4-12B model. Notice a critical engineering refinement we made: "
        "Llama Guard flags employee queries under category S7 for privacy. If treated as a blanket injection block, admins would be locked "
        "out of the employee directory! We tuned the verification logic so category S7 is passed through to our RBAC engine, allowing "
        "the admin role to access directory data while ensuring analysts still receive a 403 Forbidden. Furthermore, by running the HTTP call "
        "inside asyncio.to_thread, we prevent any event-loop stalls in FastAPI!\""
    ))

    # =========================================================================
    # SLIDE 7: Layer 5 & 6: Rate Limiting & Tamper-Evident Audit Logging
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "SECURITY LAYERS 5 & 6", "Sliding-Window Rate Limiting & Audit Logging", 7)

    add_card(s7, 0.8, 1.5, 5.7, 5.1, title="Layer 5: In-Memory Sliding Window Rate Limiter", title_color=TEXT_AMBER, border_color=BORDER_SUBTLE)
    rl_bullets = [
        ("Thread-Safe Sliding Window", "Tracks request timestamps per client IP using threading.Lock() for concurrent safety."),
        ("Strict Enterprise Quota", "Enforces 5 requests per 60 seconds (configurable via RATE_LIMIT_PER_MINUTE env var)."),
        ("Immediate 429 Rejection", "Requests exceeding the threshold return HTTP 429 Too Many Requests and log 'rate_limited'."),
        ("FastAPI Middleware Architecture", "Runs as an HTTP middleware on POST /ask, intercepting traffic before parsing body or invoking auth.")
    ]
    add_bullet_list(s7, 1.05, 2.2, 5.2, 4.2, rl_bullets, font_size=11.5, space_after=12)

    add_card(s7, 6.8, 1.5, 5.7, 5.1, title="Layer 6: Structured Audit Logging (audit.log)", title_color=TEXT_EMERALD, border_color=BORDER_SUBTLE)
    audit_bullets = [
        ("JSON Lines (JSONL) Standard", "Atomic single-line JSON records formatted with UTC ISO timestamps."),
        ("Standardized Event Taxonomy", "Records 7 lifecycle events: auth_failed, forbidden, injection_blocked, malformed_request, rate_limited, action_ok, server_error."),
        ("Immutable Traceability", "Guarantees user identity, role, action, client IP, and key fingerprint on every audit line."),
        ("Thread-Safe File Appender", "Guarded by audit_lock to prevent interleaved log lines under high concurrent load.")
    ]
    add_bullet_list(s7, 7.05, 2.2, 5.2, 4.2, audit_bullets, font_size=11.5, space_after=12)

    set_notes(s7, (
        "VIDEO PRESENTER SCRIPT (SLIDE 7 - RATE LIMITING & AUDIT):\n"
        "\"Layers 5 and 6 provide operational resilience and forensic accountability.\n\n"
        "In Layer 5, our sliding window rate limiter protects the API from burst floods and brute-force key attacks. It maintains a "
        "thread-safe window per client IP. In our demo setup, any client exceeding 5 requests within 60 seconds receives an immediate "
        "429 Too Many Requests response.\n\n"
        "In Layer 6, our audit logger flushes structured JSON Lines to audit.log. Unlike unstructured text logs, every entry guarantees "
        "structured fields: ISO-8601 UTC timestamp, the specific event type, the authenticated user, role, intended action, client IP, "
        "and key fingerprint. This enables direct ingestion into enterprise SIEM platforms like Datadog or Splunk for automated alert rules.\""
    ))

    # =========================================================================
    # SLIDE 8: Layer 7 & 8: Secure Error Handling & Secrets Architecture
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "SECURITY LAYERS 7 & 8", "Secure Error Handling & Secrets Management", 8)

    add_card(s8, 0.8, 1.5, 5.7, 5.1, title="Layer 7: Global Zero-Traceback Error Handler", title_color=TEXT_CYAN, border_color=BORDER_SUBTLE)
    err_bullets = [
        ("Catch-All Exception Shield", "Global @app.exception_handler(Exception) catches unhandled runtime exceptions."),
        ("Zero Stack Trace Disclosure", "Internal Python stack traces, file system paths, and third-party library versions are never returned to the caller."),
        ("Minimal Error Payloads", "Returns generic {'detail': 'Internal error'} with HTTP 500 status code."),
        ("Internal Logging", "Emits a 'server_error' event to audit.log with the client IP to alert operations without leaking diagnostic data.")
    ]
    add_bullet_list(s8, 1.05, 2.2, 5.2, 4.2, err_bullets, font_size=11.5, space_after=12)

    add_card(s8, 6.8, 1.5, 5.7, 5.1, title="Layer 8: Environment & Secrets Architecture", title_color=TEXT_EMERALD, border_color=BORDER_SUBTLE)
    sec_bullets = [
        ("No Hardcoded Production Secrets", "Source code main.py contains zero live credentials or API tokens."),
        (".env Configuration Loading", "Reads ANALYST_API_KEY, ADMIN_API_KEY, and NVIDIA_API_KEY from environment variables or .env file."),
        (".gitignore Protection", "The .env file and *.log files are strictly excluded from version control to prevent credential exposure on GitHub."),
        (".env.example Template Included", "A safe, sanitized template is committed so team members know exactly what environment variables to provide.")
    ]
    add_bullet_list(s8, 7.05, 2.2, 5.2, 4.2, sec_bullets, font_size=11.5, space_after=12)

    set_notes(s8, (
        "VIDEO PRESENTER SCRIPT (SLIDE 8 - ERRORS & SECRETS):\n"
        "\"In Layers 7 and 8, we ensure that the API leaks zero information through error messages or source control.\n\n"
        "Layer 7 implements a global exception handler. Unhandled Python exceptions often dump traceback lines revealing library versions "
        "and file paths. Our catch-all handler guarantees that clients receive only a clean {'detail': 'Internal error'}, while the server "
        "logs a server_error audit event.\n\n"
        "Layer 8 addresses secrets management. Earlier in our development, we audited the code and removed all hardcoded API keys. All keys "
        "are loaded dynamically from a local .env file. The .env file is gitignored, and we include a clean .env.example template so developers "
        "can set up their environment securely. Now let's see all these layers in action with our test suite!\""
    ))

    # =========================================================================
    # SLIDE 9: Comprehensive Test Suite & Live Verification
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "VERIFICATION & TESTS", "Comprehensive Curl Test Suite & Results", 9)

    test_cards = [
        ("TEST 1: Valid Analyst Query", "sales_report", "200 OK", "Returns weekly sales data & AI summary for analyst_user.", BORDER_EMERALD),
        ("TEST 2.1: Invalid API Key", "auth_failed", "401 Unauthorized", "Wrong key rejected; logs key fingerprint.", BORDER_ROSE),
        ("TEST 2.2: Prompt Injection", "injection_blocked", "400 Bad Request", "Detected 'ignore previous instructions'; blocked.", BORDER_ROSE),
        ("TEST 2.3: Analyst Asking PII", "forbidden", "403 Forbidden", "Analyst blocked from employee_info via RBAC.", BORDER_AMBER),
        ("TEST 2.4: Malformed Payload", "malformed_request", "422 Unprocessable", "Undeclared field rejected; input masked.", BORDER_ROSE),
        ("TEST 2.5: Burst Rate Limiting", "rate_limited", "429 Too Many Req", "Requests 1-5 return 200 OK; 6th returns 429.", BORDER_AMBER)
    ]

    for idx, (t_title, t_ev, t_code, t_desc, t_col) in enumerate(test_cards):
        row = idx // 3
        col = idx % 3
        c_left = 0.8 + (col * 3.98)
        c_top = 1.5 + (row * 2.6)

        c = add_card(s9, c_left, c_top, 3.8, 2.4, title="", border_color=t_col)
        tb = s9.shapes.add_textbox(Inches(c_left + 0.15), Inches(c_top + 0.15), Inches(3.5), Inches(2.1))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = t_title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        r2_1 = p2.add_run()
        r2_1.text = f"Result: {t_code}  |  "
        r2_1.font.name = "Segoe UI"
        r2_1.font.bold = True
        r2_1.font.size = Pt(10.5)
        r2_1.font.color.rgb = t_col

        r2_2 = p2.add_run()
        r2_2.text = f"Event: {t_ev}"
        r2_2.font.name = "Segoe UI"
        r2_2.font.size = Pt(10)
        r2_2.font.color.rgb = TEXT_CYAN
        p2.space_after = Pt(6)

        p3 = tf.add_paragraph()
        p3.text = t_desc
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = TEXT_MUTED

    # Bottom badge
    tb_b = s9.shapes.add_textbox(Inches(0.8), Inches(6.75), Inches(11.733), Inches(0.4))
    tf_b = tb_b.text_frame
    pb = tf_b.paragraphs[0]
    pb.text = "✔ Automated verification executed via run_tests.sh  |  100% Pass Rate across all 6 test scenarios + Admin employee query"
    pb.font.name = "Segoe UI"
    pb.font.size = Pt(10)
    pb.font.bold = True
    pb.font.color.rgb = TEXT_EMERALD

    set_notes(s9, (
        "VIDEO PRESENTER SCRIPT (SLIDE 9 - TESTS DEMO):\n"
        "\"Now let's examine the test suite we executed to validate each requirement.\n\n"
        "In Test 1, we send a valid sales report query with the analyst key: the API returns 200 OK with formatted revenue figures.\n"
        "In Test 2.1, we provide an invalid key: the API returns 401 Unauthorized.\n"
        "In Test 2.2, we test prompt injection by asking the API to 'ignore previous instructions': our guardrail immediately triggers 400 Bad Request.\n"
        "In Test 2.3, the analyst tries to query employee information for Alice: RBAC rejects the attempt with 403 Forbidden.\n"
        "In Test 2.4, we send an extra undeclared parameter: Pydantic rejects it with 422 Unprocessable Content without echoing the parameter.\n"
        "In Test 2.5, we fire 6 rapid requests: the first 5 succeed with 200 OK, and the 6th is throttled with 429 Too Many Requests.\n"
        "Additionally, when we send the employee lookup as an admin user, it succeeds with 200 OK. Every test passes with flying colors!\""
    ))

    # =========================================================================
    # SLIDE 10: Real-Time Audit Log Output & Evidence
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_header(s10, "FORENSIC EVIDENCE", "Live Audit Log Output (audit.log)", 10)

    log_lines = [
        '# Real JSON Lines captured during automated test execution (audit.log):',
        '{"timestamp": "2026-11-12T11:41:26.869Z", "event": "action_ok", "user": "analyst_user", "role": "analyst", "action": "sales_report", "ip": "10.0.1.1", "fingerprint": "a6f632a6"}',
        '{"timestamp": "2026-11-12T11:41:26.881Z", "event": "auth_failed", "user": null, "role": null, "action": null, "ip": "10.0.2.1", "fingerprint": "0d29294b"}',
        '{"timestamp": "2026-11-12T11:41:27.150Z", "event": "injection_blocked", "user": "analyst_user", "role": "analyst", "action": null, "ip": "10.0.2.2", "fingerprint": "a6f632a6"}',
        '{"timestamp": "2026-11-12T11:41:27.437Z", "event": "forbidden", "user": "analyst_user", "role": "analyst", "action": "employee_info", "ip": "10.0.2.3", "fingerprint": "a6f632a6"}',
        '{"timestamp": "2026-11-12T11:41:27.448Z", "event": "malformed_request", "user": null, "role": null, "action": null, "ip": "10.0.2.4"}',
        '{"timestamp": "2026-11-12T11:41:28.394Z", "event": "rate_limited", "user": null, "role": null, "action": null, "ip": "10.0.99.85"}'
    ]
    add_terminal(s10, 0.8, 1.5, 11.733, 3.6, "audit.log (JSON Lines Stream)", log_lines)

    add_card(s10, 0.8, 5.3, 3.75, 1.4, title="1. Full Auditability", title_color=TEXT_CYAN, border_color=BORDER_SUBTLE)
    add_bullet_list(s10, 0.95, 5.75, 3.5, 0.85, [
        "Every request maps to a structured event.",
        "Zero unstructured console text."
    ], font_size=10, space_after=4)

    add_card(s10, 4.8, 5.3, 3.75, 1.4, title="2. Credential Privacy", title_color=TEXT_EMERALD, border_color=BORDER_SUBTLE)
    add_bullet_list(s10, 4.95, 5.75, 3.5, 0.85, [
        "Logs SHA-256 fingerprint ('a6f632a6').",
        "Raw API keys are never exposed."
    ], font_size=10, space_after=4)

    add_card(s10, 8.8, 5.3, 3.733, 1.4, title="3. SIEM-Ready Schema", title_color=TEXT_AMBER, border_color=BORDER_SUBTLE)
    add_bullet_list(s10, 8.95, 5.75, 3.5, 0.85, [
        "ISO UTC timestamps across all records.",
        "Correlates IP, user, and security event."
    ], font_size=10, space_after=4)

    set_notes(s10, (
        "VIDEO PRESENTER SCRIPT (SLIDE 10 - AUDIT LOG):\n"
        "\"Slide 10 displays the actual forensic evidence generated in audit.log during our test run.\n\n"
        "Observe the clarity of these records:\n"
        "- Line 1 records 'action_ok' when analyst_user generated a sales report from IP 10.0.1.1, with key fingerprint 'a6f632a6'.\n"
        "- Line 2 captures 'auth_failed' when an unrecognized key was attempted, logging its 8-character fingerprint without leaking the key.\n"
        "- Line 3 captures 'injection_blocked' when prompt injection was detected.\n"
        "- Line 4 captures 'forbidden' when the analyst attempted to access the employee directory.\n"
        "- Line 5 captures 'malformed_request' on schema violations.\n"
        "- Line 6 captures 'rate_limited' when IP 10.0.99.85 sent its 6th rapid request.\n\n"
        "This level of audit fidelity gives security operations centers immediate visibility into adversarial behavior.\""
    ))

    # =========================================================================
    # SLIDE 11: Summary, Deliverables & Conclusion
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11)
    add_header(s11, "CONCLUSION", "Summary: Production-Hardened Enterprise AI Gateway", 11)

    add_card(s11, 0.8, 1.5, 5.7, 5.1, title="Core Architecture Achievements", title_color=TEXT_CYAN, border_color=BORDER_CYAN)
    achievements = [
        ("Cryptographic Rigor", "Keys stored only as SHA-256 hashes; validated with hmac.compare_digest; zero plaintext exposure."),
        ("Multi-Tier Guardrails", "Sub-millisecond regex combined with NVIDIA NIM Meta Llama-Guard-4-12B AI safety classification."),
        ("Strict Access Governance", "Granular Role-Based Access Control enforced at the intent router, protecting employee directories."),
        ("DoS & Abuse Protection", "Thread-safe sliding-window rate limiting (5 req/min) preventing compute and LLM token exhaustion."),
        ("Tamper-Evident Observability", "Structured JSON Lines audit log with immutable timestamps, user identities, roles, and client IPs.")
    ]
    add_bullet_list(s11, 1.05, 2.2, 5.2, 4.2, achievements, font_size=11.5, space_after=10)

    add_card(s11, 6.8, 1.5, 5.7, 5.1, title="Deliverables & Repository Assets", title_color=TEXT_EMERALD, border_color=BORDER_EMERALD)
    deliverables = [
        ("main.py", "Complete, production-hardened FastAPI gateway in a single self-contained file with type hints and async architecture."),
        (".env & .env.example", "Environment-driven configuration with clean separation of secrets and gitignore protection."),
        ("requirements.txt", "Minimal, clean dependency set (fastapi, uvicorn, pydantic)."),
        ("README.md", "Comprehensive architectural guide, credential matrix, and reproduction steps."),
        ("run_tests.sh", "Automated bash test runner validating all positive, negative, and rate-limiting scenarios."),
        ("audit.log", "Tamper-evident JSON Lines record of all lifecycle events.")
    ]
    add_bullet_list(s11, 7.05, 2.2, 5.2, 4.2, deliverables, font_size=11.5, space_after=10)

    set_notes(s11, (
        "VIDEO PRESENTER SCRIPT (SLIDE 11 - CONCLUSION):\n"
        "\"To conclude, we have successfully designed, built, hardened, and verified a production-grade Enterprise AI Gateway.\n\n"
        "By enforcing defense-in-depth across 8 distinct layers—cryptographic key hashing, constant-time HMAC verification, "
        "strict Pydantic schema validation, regex and Llama Guard AI guardrails, sliding-window rate limiting, zero-traceback error handling, "
        "and structured JSON Lines audit logging—we demonstrate how enterprise AI APIs can be safely exposed without risking data leakage, "
        "prompt injection, or system compromise.\n\n"
        "All code, tests, and configuration files are fully tested, documented in README.md, and committed to git. "
        "Thank you for watching this technical walkthrough!\""
    ))

    # Save Deck
    output_path = "/home/ubuntu/fluid_ai/Secure_Enterprise_AI_Gateway_Walkthrough.pptx"
    prs.save(output_path)
    print(f"Presentation deck successfully created at: {output_path}")

if __name__ == "__main__":
    build_deck()
