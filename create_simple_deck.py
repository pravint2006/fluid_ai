#!/usr/bin/env python3
"""
Create a minimal, clean, high-impact 5-slide presentation deck.
Designed specifically for a clear, 3-minute video recording demo.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_simple_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Clean Modern Palette
    BG_DARK = RGBColor(15, 23, 42)          # Deep Slate #0F172A
    BG_CARD = RGBColor(30, 41, 59)          # Slate Card #1E293B
    BORDER_CYAN = RGBColor(56, 189, 248)    # Sky Cyan #38BDF8
    BORDER_GREEN = RGBColor(52, 211, 153)   # Mint Emerald #34D399
    BORDER_RED = RGBColor(248, 113, 113)    # Coral Red #F87171
    BORDER_AMBER = RGBColor(251, 191, 36)   # Amber #FBBF24
    BORDER_SUBTLE = RGBColor(51, 65, 85)    # Slate Border #334155

    TEXT_WHITE = RGBColor(248, 250, 252)    # Pure White #F8FAFC
    TEXT_MUTED = RGBColor(203, 213, 225)    # Light Slate #CBD5E1
    TEXT_DIM = RGBColor(148, 163, 184)      # Dim Gray #94A3B8

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title, category="SECURE ENTERPRISE AI API", slide_num=1):
        # Category
        tb_cat = slide.shapes.add_textbox(Inches(0.9), Inches(0.5), Inches(8.0), Inches(0.35))
        tf_cat = tb_cat.text_frame
        p_c = tf_cat.paragraphs[0]
        p_c.text = category.upper()
        p_c.font.name = "Segoe UI"
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = BORDER_CYAN

        # Title
        tb_t = slide.shapes.add_textbox(Inches(0.9), Inches(0.8), Inches(10.0), Inches(0.7))
        tf_t = tb_t.text_frame
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(26)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

        # Slide Number
        tb_n = slide.shapes.add_textbox(Inches(11.3), Inches(0.8), Inches(1.2), Inches(0.5))
        tf_n = tb_n.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.text = f"{slide_num} / 5"
        p_n.font.name = "Segoe UI"
        p_n.font.size = Pt(14)
        p_n.font.bold = True
        p_n.font.color.rgb = BORDER_CYAN

    def set_notes(slide, text):
        slide.notes_slide.notes_text_frame.text = text

    # =========================================================================
    # SLIDE 1: Title Slide (Punchy & Clean)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    # Cyan Accent Pill
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.5), Inches(3.2), Inches(0.4))
    pill.fill.solid()
    pill.fill.fore_color.rgb = BG_CARD
    pill.line.color.rgb = BORDER_CYAN
    tf_p = pill.text_frame
    p_p = tf_p.paragraphs[0]
    p_p.alignment = PP_ALIGN.CENTER
    p_p.text = "⚡ PRODUCTION-READY API GATEWAY"
    p_p.font.name = "Segoe UI"
    p_p.font.size = Pt(10)
    p_p.font.bold = True
    p_p.font.color.rgb = BORDER_CYAN

    # Main Headline
    tb_main = s1.shapes.add_textbox(Inches(0.9), Inches(2.1), Inches(11.5), Inches(2.2))
    tf_main = tb_main.text_frame
    tf_main.word_wrap = True

    p1 = tf_main.paragraphs[0]
    p1.text = "Secure Enterprise AI Gateway"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_after = Pt(12)

    p2 = tf_main.add_paragraph()
    p2.text = "A hardened FastAPI service enforcing Multi-Layer Defense-in-Depth, Zero-Trust Access Control & AI Safety Model Integration."
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(18)
    p2.font.color.rgb = TEXT_MUTED

    # 3 Stat Cards at Bottom
    stats = [
        ("Zero Plaintext Keys", "SHA-256 Hashing + Constant-Time HMAC", BORDER_CYAN),
        ("Granular RBAC", "Analyst vs. Admin Least Privilege", BORDER_GREEN),
        ("Hybrid Guardrails", "Local Regex + Meta Llama-Guard-4 AI", BORDER_AMBER)
    ]
    for idx, (st_t, st_sub, col) in enumerate(stats):
        c_left = 0.9 + (idx * 3.9)
        c = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(4.7), Inches(3.7), Inches(1.6))
        c.fill.solid()
        c.fill.fore_color.rgb = BG_CARD
        c.line.color.rgb = col
        c.line.width = Pt(1.5)

        tf_c = c.text_frame
        tf_c.word_wrap = True
        p_c1 = tf_c.paragraphs[0]
        p_c1.text = st_t
        p_c1.font.name = "Segoe UI"
        p_c1.font.size = Pt(16)
        p_c1.font.bold = True
        p_c1.font.color.rgb = TEXT_WHITE
        p_c1.space_after = Pt(6)

        p_c2 = tf_c.add_paragraph()
        p_c2.text = st_sub
        p_c2.font.name = "Segoe UI"
        p_c2.font.size = Pt(12)
        p_c2.font.color.rgb = TEXT_MUTED

    set_notes(s1, (
        "VIDEO SCRIPT (SLIDE 1 - 30s):\n"
        "\"Hi everyone! Today I'm showcasing our Secure Enterprise AI Gateway built with FastAPI.\n"
        "When exposing AI endpoints in production, you need defense-in-depth to protect against prompt injection, "
        "data leakage, and unauthorized access. We built a hardened single-file API that combines cryptographic authentication, "
        "strict role-based access control, sliding-window rate limiting, and an AI safety guardrail powered by Meta Llama Guard 4. "
        "Let's see what we built!\""
    ))

    # =========================================================================
    # SLIDE 2: What We Built (3 Core Pillars)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "System Overview & Core Capabilities", "REQUIREMENTS & ARCHITECTURE", 2)

    pillars = [
        ("1. Business Capabilities", [
            "Single Endpoint: POST /ask",
            "Sales Report: Weekly revenue metrics",
            "Support Ticket: In-memory issue creation",
            "Employee Info: Directory (Admin only)",
            "Intent Routing: Intelligent keyword map"
        ], BORDER_CYAN),
        ("2. Two Roles (RBAC)", [
            "Analyst User ('analyst_user'):",
            "  ✔ sales_report",
            "  ✔ create_ticket",
            "  ❌ employee_info (Returns 403)",
            "Admin User ('admin_user'):",
            "  ✔ Full access to all actions"
        ], BORDER_GREEN),
        ("3. Defense-in-Depth", [
            "Rate Limiting: 5 requests / 60 seconds",
            "Input Hygiene: Pydantic extra='forbid'",
            "AI Guardrail: Meta Llama-Guard-4-12B",
            "Zero Leaks: Generic error envelopes",
            "Audit Trail: Tamper-evident audit.log"
        ], BORDER_AMBER)
    ]

    for idx, (p_title, p_items, col) in enumerate(pillars):
        c_left = 0.9 + (idx * 3.9)
        c = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(1.6), Inches(3.7), Inches(5.2))
        c.fill.solid()
        c.fill.fore_color.rgb = BG_CARD
        c.line.color.rgb = col
        c.line.width = Pt(1.5)

        tb = s2.shapes.add_textbox(Inches(c_left + 0.2), Inches(1.8), Inches(3.3), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = p_title
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(16)
        p_t.font.bold = True
        p_t.font.color.rgb = col
        p_t.space_after = Pt(12)

        for item in p_items:
            p_i = tf.add_paragraph()
            p_i.text = item
            p_i.font.name = "Segoe UI"
            p_i.font.size = Pt(12.5)
            p_i.font.color.rgb = TEXT_WHITE if item.startswith("  ✔") or item.startswith("Analyst") or item.startswith("Admin") else TEXT_MUTED
            p_i.space_after = Pt(8)

    set_notes(s2, (
        "VIDEO SCRIPT (SLIDE 2 - 40s):\n"
        "\"Here is what we built at a glance.\n"
        "First, our business capabilities: through a single POST /ask endpoint, users can generate sales reports, create support tickets, "
        "or look up employees.\n"
        "Second, Role-Based Access Control: we strictly separate Analyst from Admin. Analysts can see sales and create tickets, but employee "
        "records are strictly restricted to administrators. Any unauthorized attempt returns a 403 Forbidden.\n"
        "Third, our defense-in-depth: every request is rate-limited to 5 requests per minute, validated against a strict Pydantic schema, "
        "evaluated by Meta Llama Guard, and recorded in a structured audit log.\""
    ))

    # =========================================================================
    # SLIDE 3: How It Works (Visual 5-Gate Flow)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "The 5-Gate Security Pipeline", "REQUEST LIFECYCLE", 3)

    gates = [
        ("GATE 1", "Rate Limiter", "5 req / 60s window\nDrops burst floods immediately (429)", BORDER_CYAN),
        ("GATE 2", "Authentication", "SHA-256 Hash + HMAC\nConstant-time verification (401)", BORDER_CYAN),
        ("GATE 3", "Guardrails", "Regex + Llama-Guard AI\nBlocks prompt & SQL injections (400)", BORDER_AMBER),
        ("GATE 4", "RBAC Check", "Analyst vs. Admin Matrix\nRestricts sensitive directories (403)", BORDER_RED),
        ("GATE 5", "Safe Execution", "Executes business action\nFlushes audit.log (200 OK)", BORDER_GREEN)
    ]

    for idx, (g_num, g_title, g_desc, col) in enumerate(gates):
        g_left = 0.9 + (idx * 2.34)
        c = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(g_left), Inches(1.8), Inches(2.2), Inches(3.6))
        c.fill.solid()
        c.fill.fore_color.rgb = BG_CARD
        c.line.color.rgb = col
        c.line.width = Pt(1.5)

        tb = s3.shapes.add_textbox(Inches(g_left + 0.15), Inches(2.0), Inches(1.9), Inches(3.2))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = g_num
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = g_title
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(15)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_after = Pt(10)

        p3 = tf.add_paragraph()
        p3.text = g_desc
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(11)
        p3.font.color.rgb = TEXT_MUTED

    # Bottom summary box
    bot_card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(5.7), Inches(11.533), Inches(1.1))
    bot_card.fill.solid()
    bot_card.fill.fore_color.rgb = BG_CARD
    bot_card.line.color.rgb = BORDER_SUBTLE
    tf_bot = bot_card.text_frame
    tf_bot.word_wrap = True
    p_b = tf_bot.paragraphs[0]
    p_b.alignment = PP_ALIGN.CENTER
    p_b.text = "🔒 Zero Information Leakage: All errors return generic envelopes {'detail': '...'} with zero stack traces or input echoing."
    p_b.font.name = "Segoe UI"
    p_b.font.size = Pt(13)
    p_b.font.bold = True
    p_b.font.color.rgb = BORDER_CYAN

    set_notes(s3, (
        "VIDEO SCRIPT (SLIDE 3 - 40s):\n"
        "\"This is how every request flows through our 5 security gates.\n"
        "Gate 1: The rate limiter checks the client IP before doing any heavy work. If a client sends more than 5 requests in 60 seconds, "
        "they are stopped with a 429.\n"
        "Gate 2: We verify the API key. We never store keys in plaintext—we hash them with SHA-256 and use constant-time HMAC comparison.\n"
        "Gate 3: Our guardrails scan for prompt injections and malicious payloads, backed by Meta Llama Guard.\n"
        "Gate 4: RBAC validates permissions. An analyst querying employee records is immediately blocked with 403 Forbidden.\n"
        "Gate 5: Only when all gates pass does the action run, returning 200 OK and recording an audit record.\n"
        "Now let's look at the test results!\""
    ))

    # =========================================================================
    # SLIDE 4: Live Test Results (Clean Scorecard)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Automated Curl Test Suite (run_tests.sh)", "VERIFICATION SCORECARD", 4)

    tests = [
        ("Test 1: Valid Analyst Query", "Generate weekly sales report", "HTTP 200 OK", "Returned report & AI summary", BORDER_GREEN),
        ("Test 2.1: Invalid API Key", "Attempt with wrong secret key", "HTTP 401 Unauthorized", "Rejected; logged fingerprint", BORDER_RED),
        ("Test 2.2: Prompt Injection", "ignore previous instructions...", "HTTP 400 Bad Request", "Guardrail blocked attack", BORDER_RED),
        ("Test 2.3: Analyst Asking PII", "Analyst requesting employee info", "HTTP 403 Forbidden", "RBAC blocked unauthorized role", BORDER_AMBER),
        ("Test 2.4: Malformed Payload", "Extra forbidden field injected", "HTTP 422 Invalid Request", "Pydantic extra='forbid' blocked", BORDER_RED),
        ("Test 2.5: Burst Rate Limit", "6 rapid requests in 1 second", "HTTP 429 Too Many Req", "Requests 1-5 OK, 6th throttled", BORDER_AMBER),
    ]

    for idx, (t_name, t_input, t_code, t_result, col) in enumerate(tests):
        row = idx // 3
        c_idx = idx % 3
        c_left = 0.9 + (c_idx * 3.9)
        c_top = 1.7 + (row * 2.5)

        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(c_top), Inches(3.7), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = col
        card.line.width = Pt(1.5)

        tb = s4.shapes.add_textbox(Inches(c_left + 0.15), Inches(c_top + 0.15), Inches(3.4), Inches(1.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = t_name
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = f"Input: \"{t_input}\""
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_DIM
        p2.space_after = Pt(6)

        p3 = tf.add_paragraph()
        r3_1 = p3.add_run()
        r3_1.text = f"{t_code}\n"
        r3_1.font.name = "Segoe UI"
        r3_1.font.bold = True
        r3_1.font.size = Pt(12)
        r3_1.font.color.rgb = col

        r3_2 = p3.add_run()
        r3_2.text = f"✔ {t_result}"
        r3_2.font.name = "Segoe UI"
        r3_2.font.size = Pt(10.5)
        r3_2.font.color.rgb = TEXT_MUTED

    set_notes(s4, (
        "VIDEO SCRIPT (SLIDE 4 - 40s):\n"
        "\"To prove this in action, we executed an automated test script covering all required scenarios.\n"
        "In Test 1, a valid analyst request returns 200 OK with sales metrics.\n"
        "In Test 2.1, an invalid key is rejected with 401 Unauthorized.\n"
        "In Test 2.2, a prompt injection attack is caught by our guardrail and returns 400 Bad Request.\n"
        "In Test 2.3, when an analyst queries employee information, RBAC blocks it with 403 Forbidden.\n"
        "In Test 2.4, an unexpected payload parameter is rejected with 422 without echoing the input.\n"
        "And in Test 2.5, sending 6 rapid requests allows the first 5 and throttles the 6th with 429 Too Many Requests.\n"
        "Every single test passes deterministically!\""
    ))

    # =========================================================================
    # SLIDE 5: Audit Log Evidence & Conclusion
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Forensic Proof & Key Takeaways", "AUDIT LOG & CONCLUSION", 5)

    # Terminal card with real audit.log entries
    term = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(1.6), Inches(11.533), Inches(3.2))
    term.fill.solid()
    term.fill.fore_color.rgb = RGBColor(7, 10, 16)
    term.line.color.rgb = BORDER_SUBTLE
    term.line.width = Pt(1)

    tb_t = s5.shapes.add_textbox(Inches(1.1), Inches(1.75), Inches(11.1), Inches(2.9))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True

    p_th = tf_t.paragraphs[0]
    p_th.text = "⚡ Real forensic entries flushed to audit.log during test execution:"
    p_th.font.name = "Segoe UI"
    p_th.font.size = Pt(11)
    p_th.font.bold = True
    p_th.font.color.rgb = BORDER_CYAN
    p_th.space_after = Pt(6)

    log_examples = [
        ('{"event": "action_ok", "user": "analyst_user", "action": "sales_report", "ip": "10.0.1.1", "fingerprint": "a6f632a6"}', BORDER_GREEN),
        ('{"event": "auth_failed", "user": null, "action": null, "ip": "10.0.2.1", "fingerprint": "0d29294b"}', BORDER_RED),
        ('{"event": "injection_blocked", "user": "analyst_user", "action": null, "ip": "10.0.2.2", "fingerprint": "a6f632a6"}', BORDER_RED),
        ('{"event": "forbidden", "user": "analyst_user", "action": "employee_info", "ip": "10.0.2.3", "fingerprint": "a6f632a6"}', BORDER_AMBER),
        ('{"event": "rate_limited", "user": null, "action": null, "ip": "10.0.99.85"}', BORDER_AMBER),
    ]

    for line_text, col in log_examples:
        p_l = tf_t.add_paragraph()
        run = p_l.add_run()
        run.text = line_text
        run.font.name = "Consolas"
        run.font.size = Pt(9.5)
        run.font.color.rgb = col
        p_l.space_after = Pt(4)

    # 3 Summary takeaway cards
    takeaways = [
        ("Cryptographic Rigor", "Keys stored only as SHA-256 hashes; zero raw keys logged.", BORDER_CYAN),
        ("Zero Information Leakage", "Strict error masks and sanitized 422/500 JSON responses.", BORDER_GREEN),
        ("Production Deliverables", "main.py, .env, requirements.txt, and automated run_tests.sh.", BORDER_AMBER)
    ]
    for idx, (t_title, t_desc, col) in enumerate(takeaways):
        c_left = 0.9 + (idx * 3.9)
        c = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(c_left), Inches(5.1), Inches(3.7), Inches(1.7))
        c.fill.solid()
        c.fill.fore_color.rgb = BG_CARD
        c.line.color.rgb = col
        c.line.width = Pt(1.5)

        tf_c = c.text_frame
        tf_c.word_wrap = True
        p1 = tf_c.paragraphs[0]
        p1.text = t_title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_after = Pt(4)

        p2 = tf_c.add_paragraph()
        p2.text = t_desc
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED

    set_notes(s5, (
        "VIDEO SCRIPT (SLIDE 5 - 30s):\n"
        "\"Finally, on Slide 5, you see our forensic audit log. Every single request flushes a structured JSON line "
        "recording the timestamp, event code, user identity, action, and IP. Notice that raw API keys are never stored or logged—"
        "we record only an 8-character fingerprint like 'a6f632a6'.\n\n"
        "In summary, we have built a robust, enterprise-grade AI Gateway that is secure by default, fully auditable, and ready for production. "
        "Thank you for watching!\""
    ))

    output_path = "/home/ubuntu/fluid_ai/Simple_Presentation.pptx"
    prs.save(output_path)
    print(f"Simple presentation created at: {output_path}")

if __name__ == "__main__":
    build_simple_deck()
