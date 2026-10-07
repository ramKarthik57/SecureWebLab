import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    # Try system fonts
    font_paths = [
        "C:\\Windows\\Fonts\\segoeui" + ("b.ttf" if bold else ".ttf"),
        "C:\\Windows\\Fonts\\calibri" + ("b.ttf" if bold else ".ttf"),
        "C:\\Windows\\Fonts\\arial" + ("bd.ttf" if bold else ".ttf"),
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    x1, y1, x2, y2 = bbox
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow(draw, start, end, color, width=3, arrow_size=10):
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=color, width=width)
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - arrow_size * math.cos(angle - math.pi / 6), y2 - arrow_size * math.sin(angle - math.pi / 6))
    p2 = (x2 - arrow_size * math.cos(angle + math.pi / 6), y2 - arrow_size * math.sin(angle + math.pi / 6))
    draw.polygon([end, p1, p2], fill=color)

# ==============================================================================
# 1. SYSTEM ARCHITECTURE DIAGRAM
# ==============================================================================
def create_architecture_diagram(out_path):
    W, H = 1600, 950
    im = Image.new("RGB", (W, H), "#F8FAFC")
    draw = ImageDraw.Draw(im)

    font_title = get_font(32, bold=True)
    font_subtitle = get_font(18, bold=False)
    font_tier = get_font(20, bold=True)
    font_card_title = get_font(18, bold=True)
    font_body = get_font(14, bold=False)
    font_badge = get_font(12, bold=True)

    # Title Banner
    draw.rectangle([0, 0, W, 80], fill="#0A2540")
    draw.text((40, 18), "SecureJobLab — System Architecture & Execution Flow", fill="#FFFFFF", font=font_title)
    draw.text((40, 52), "Course: 20CYS403 Web Application Security | Dual-Mode AppSec Platform", fill="#94A3B8", font=font_subtitle)

    # 4 Architecture Columns / Tiers
    tiers = [
        {"title": "1. Client & Presentation Tier", "sub": "Browser / UI Layer", "x": 50, "w": 330},
        {"title": "2. Security Gateway & Mode Switcher", "sub": "Session & Defense Controller", "x": 420, "w": 350},
        {"title": "3. Application & API Engine", "sub": "Backend Controller Tier (PHP)", "x": 810, "w": 360},
        {"title": "4. Data & Subsystem Tier", "sub": "Database & Host Subsystems", "x": 1210, "w": 340},
    ]

    for t in tiers:
        # Tier boundary
        draw_rounded_rect(draw, [t["x"], 110, t["x"] + t["w"], 900], radius=12, fill="#FFFFFF", outline="#E2E8F0", width=2)
        # Tier header
        draw_rounded_rect(draw, [t["x"], 110, t["x"] + t["w"], 165], radius=12, fill="#F1F5F9", outline="#CBD5E1", width=1)
        draw.text((t["x"] + 15, 120), t["title"], fill="#0F172A", font=font_tier)
        draw.text((t["x"] + 15, 145), t["sub"], fill="#64748B", font=font_body)

    # --- Tier 1 Components ---
    cards_t1 = [
        {"y": 185, "h": 140, "title": "Job Recruitment Portal UI", "lines": ["• Modern Jobpilot SaaS Theme", "• Instant AJAX Job Search", "• Candidate Application Form", "• Document & Resume Viewer"], "badge": "UI Tier", "bcolor": "#0284C7"},
        {"y": 345, "h": 140, "title": "Authentication Portal (login.php)", "lines": ["• Role-Based Access (Candidate/Admin)", "• Persona: Ram Karthik", "• Sign In & Registration", "• Session Token Management"], "badge": "Auth UI", "bcolor": "#0284C7"},
        {"y": 505, "h": 170, "title": "AppSec Testing Suite (Tab 3)", "lines": ["• 5 Core Vulnerability Modules", "• Real-time Security Telemetry", "• Live Attack & Defense Presets", "• UI Redressing Sandbox Overlay", "• Native Alert Dialog Capture"], "badge": "Lab UI", "bcolor": "#DC2626"},
        {"y": 695, "h": 160, "title": "Live Diagnostics & Tools", "lines": ["• Network Gateway Latency Tool", "• Resume & Document Inspector", "• Account Security & Settings", "• 1-Click Database Reset Tool"], "badge": "Utilities", "bcolor": "#0284C7"},
    ]
    for c in cards_t1:
        draw_rounded_rect(draw, [65, c["y"], 365, c["y"] + c["h"]], radius=8, fill="#F8FAFC", outline="#CBD5E1", width=1)
        draw.text((80, c["y"] + 12), c["title"], fill="#1E293B", font=font_card_title)
        draw_rounded_rect(draw, [285, c["y"] + 10, 355, c["y"] + 28], radius=4, fill=c["bcolor"])
        draw.text((292, c["y"] + 12), c["badge"], fill="#FFFFFF", font=font_badge)
        y_text = c["y"] + 38
        for line in c["lines"]:
            draw.text((80, y_text), line, fill="#475569", font=font_body)
            y_text += 22

    # --- Tier 2 Components (Gateway & Switcher) ---
    cards_t2 = [
        {"y": 185, "h": 170, "title": "Global Mode Switcher", "lines": ["• Toggle: ?mode=vulnerable / secure", "• State stored in $_SESSION['appsec_mode']", "• Visual Status Indicator (Navbar)", "• Live Mode Synchronization", "• Affects all 5 Lab Modules"], "badge": "Controller", "bcolor": "#7C3AED"},
        {"y": 375, "h": 220, "title": "Vulnerable Execution Engine", "lines": ["• Unsanitized SQL Concatenation", "• Raw Script Reflection in DOM", "• Direct shell_exec() invocation", "• Unrestricted relative path inclusion", "• Missing X-Frame-Options / CSP", "• Exploit Telemetry Extraction"], "badge": "VULNERABLE (RED)", "bcolor": "#DC2626"},
        {"y": 615, "h": 240, "title": "Secure Mitigated Engine", "lines": ["• Parameterized Prepared Statements", "• Contextual htmlspecialchars()", "• Regex Whitelist & escapeshellarg()", "• basename() + Whitelist Array", "• X-Frame-Options: DENY", "• CSP: frame-ancestors 'none'", "• Defense-in-Depth Telemetry"], "badge": "SECURE (GREEN)", "bcolor": "#16A34A"},
    ]
    for c in cards_t2:
        draw_rounded_rect(draw, [435, c["y"], 755, c["y"] + c["h"]], radius=8, fill="#F8FAFC", outline="#CBD5E1", width=1)
        draw.text((450, c["y"] + 12), c["title"], fill="#1E293B", font=font_card_title)
        draw_rounded_rect(draw, [620, c["y"] + 10, 745, c["y"] + 28], radius=4, fill=c["bcolor"])
        draw.text((628, c["y"] + 12), c["badge"], fill="#FFFFFF", font=font_badge)
        y_text = c["y"] + 38
        for line in c["lines"]:
            draw.text((450, y_text), line, fill="#475569", font=font_body)
            y_text += 24

    # --- Tier 3 Components (Backend API Engine) ---
    cards_t3 = [
        {"y": 185, "h": 140, "title": "REST/AJAX Engine (api.php)", "lines": ["• Centralized Action Router", "• JSON Telemetry Formatter", "• Execution Metrics & Status Code", "• Application CRUD Controller"], "badge": "API Core", "bcolor": "#0284C7"},
        {"y": 345, "h": 170, "title": "The 5 AppSec Lab Handlers", "lines": ["1. SQLi Engine (CWE-89)", "2. XSS Engine (CWE-79)", "3. Command Injection Engine (CWE-78)", "4. Directory Traversal Engine (CWE-22)", "5. Clickjacking Endpoint (CWE-1021)"], "badge": "5 Modules", "bcolor": "#0284C7"},
        {"y": 535, "h": 170, "title": "Clickjacking Target (clickjack_target.php)", "lines": ["• High-Impact Destructive Action", "• 'Permanent Account Deletion'", "• Target Account: Ram Karthik", "• Dynamic Framing Defense Headers", "• CSRF & UI Redressing Sandbox"], "badge": "Target Endpoint", "bcolor": "#DC2626"},
        {"y": 725, "h": 130, "title": "Job Board Business Logic", "lines": ["• search_jobs (Instant AJAX Filter)", "• apply_job (Resume Attachment)", "• add_job / edit_job / delete_job", "• reseed_db (Pristine DB Reset)"], "badge": "Business Logic", "bcolor": "#0284C7"},
    ]
    for c in cards_t3:
        draw_rounded_rect(draw, [825, c["y"], 1155, c["y"] + c["h"]], radius=8, fill="#F8FAFC", outline="#CBD5E1", width=1)
        draw.text((840, c["y"] + 12), c["title"], fill="#1E293B", font=font_card_title)
        draw_rounded_rect(draw, [1040, c["y"] + 10, 1145, c["y"] + 28], radius=4, fill=c["bcolor"])
        draw.text((1048, c["y"] + 12), c["badge"], fill="#FFFFFF", font=font_badge)
        y_text = c["y"] + 38
        for line in c["lines"]:
            draw.text((840, y_text), line, fill="#475569", font=font_body)
            y_text += 22

    # --- Tier 4 Components (Data & Subsystem) ---
    cards_t4 = [
        {"y": 185, "h": 220, "title": "MySQL Database (securejoblab)", "lines": ["• users: Auth & RBAC Records", "• jobs: 5 Verified Cybersecurity Roles", "• applications: Candidate Submissions", "• feedback: Recruiter Endorsements", "• UTF-8 / utf8mb4 encoding", "• ₹ (INR) Salary Packaging"], "badge": "Relational DB", "bcolor": "#0F766E"},
        {"y": 425, "h": 220, "title": "Operating System Shell", "lines": ["• Host OS: Microsoft Windows", "• Shell Environment: cmd.exe / PowerShell", "• System Binary: ping.exe", "• Delimiters Tested: &, |, ;", "• Command Chaining: whoami, dir", "• Sandbox Boundary Enforcement"], "badge": "OS Subsystem", "bcolor": "#B45309"},
        {"y": 665, "h": 200, "title": "Local Storage & Filesystem", "lines": ["• lab_files/ Directory (Isolated)", "• resume.txt, coverletter.txt", "• secret_flag.txt (Lab Canary)", "• uploads/resumes/ (Candidate storage)", "• Traversal Target: database.sql"], "badge": "Filesystem", "bcolor": "#B45309"},
    ]
    for c in cards_t4:
        draw_rounded_rect(draw, [1225, c["y"], 1535, c["y"] + c["h"]], radius=8, fill="#F8FAFC", outline="#CBD5E1", width=1)
        draw.text((1240, c["y"] + 12), c["title"], fill="#1E293B", font=font_card_title)
        draw_rounded_rect(draw, [1425, c["y"] + 10, 1525, c["y"] + 28], radius=4, fill=c["bcolor"])
        draw.text((1433, c["y"] + 12), c["badge"], fill="#FFFFFF", font=font_badge)
        y_text = c["y"] + 38
        for line in c["lines"]:
            draw.text((1240, y_text), line, fill="#475569", font=font_body)
            y_text += 24

    # Connectors
    draw_arrow(draw, (365, 255), (435, 255), "#64748B", width=2)
    draw_arrow(draw, (365, 590), (435, 480), "#DC2626", width=2)
    draw_arrow(draw, (365, 590), (435, 730), "#16A34A", width=2)
    draw_arrow(draw, (755, 480), (825, 430), "#DC2626", width=2)
    draw_arrow(draw, (755, 730), (825, 430), "#16A34A", width=2)
    draw_arrow(draw, (1155, 290), (1225, 290), "#0F766E", width=2)
    draw_arrow(draw, (1155, 430), (1225, 530), "#B45309", width=2)
    draw_arrow(draw, (1155, 430), (1225, 760), "#B45309", width=2)

    im.save(out_path, quality=95)
    print("Saved architecture diagram to:", out_path)

# ==============================================================================
# 2. DUAL-ENGINE FLOW DIAGRAM (Comparative Attack vs Defense)
# ==============================================================================
def create_dual_engine_diagram(out_path):
    W, H = 1600, 750
    im = Image.new("RGB", (W, H), "#F8FAFC")
    draw = ImageDraw.Draw(im)

    font_title = get_font(30, bold=True)
    font_subtitle = get_font(17, bold=False)
    font_card_title = get_font(18, bold=True)
    font_body = get_font(14, bold=False)
    font_badge = get_font(13, bold=True)

    # Title Banner
    draw.rectangle([0, 0, W, 75], fill="#0A2540")
    draw.text((40, 16), "SecureJobLab — Dual-Engine Security Execution Model", fill="#FFFFFF", font=font_title)
    draw.text((40, 48), "Comparative Request Pipeline: 🔴 Vulnerable Mode vs. 🟢 Secure Mitigated Mode", fill="#94A3B8", font=font_subtitle)

    # Top Half: Vulnerable Pipeline (RED)
    draw_rounded_rect(draw, [40, 95, W - 40, 395], radius=12, fill="#FFF1F0", outline="#FFA39E", width=2)
    draw.text((60, 110), "🔴 VULNERABLE MODE PIPELINE (CWE Exploit Path)", fill="#CF1322", font=font_card_title)
    draw_rounded_rect(draw, [W - 260, 108, W - 60, 134], radius=4, fill="#CF1322")
    draw.text((W - 250, 112), "EXPLOIT SUCCEEDS", fill="#FFFFFF", font=font_badge)

    v_steps = [
        {"x": 60, "w": 260, "title": "1. Untrusted Input", "sub": "Raw Attack Payload", "desc": ["• ' OR 1=1 #", "• <script>alert()</script>", "• 127.0.0.1 & whoami", "• ../database.sql", "• Transparent Iframe"]},
        {"x": 370, "w": 260, "title": "2. Insecure Handling", "sub": "Missing Validation", "desc": ["• Direct string concat", "• Raw DOM interpolation", "• Unescaped shell_exec", "• Unrestricted relative path", "• Missing frame headers"]},
        {"x": 680, "w": 260, "title": "3. Dangerous Sink", "sub": "Execution Layer", "desc": ["• mysqli_query() parser", "• Browser DOM parser", "• cmd.exe / OS Shell", "• file_get_contents()", "• Third-party origin frame"]},
        {"x": 990, "w": 260, "title": "4. Security Weakness", "sub": "Integrity Breached", "desc": ["• SQL Grammar broken", "• JavaScript executed", "• Shell chained with &", "• Path boundary crossed", "• UI redressed / hijacked"]},
        {"x": 1300, "w": 240, "title": "5. Attack Impact", "sub": "Compromised State", "desc": ["❌ Secret data leaked", "❌ Session cookie stolen", "❌ Host takeover", "❌ Sensitive files read", "❌ Account deleted"]},
    ]

    for s in v_steps:
        draw_rounded_rect(draw, [s["x"], 150, s["x"] + s["w"], 370], radius=8, fill="#FFFFFF", outline="#FFCCC7", width=1)
        draw.text((s["x"] + 15, 165), s["title"], fill="#CF1322", font=font_card_title)
        draw.text((s["x"] + 15, 192), s["sub"], fill="#78350F", font=get_font(13, bold=True))
        y = 225
        for d in s["desc"]:
            draw.text((s["x"] + 15, y), d, fill="#374151", font=font_body)
            y += 24

    for i in range(len(v_steps) - 1):
        x_from = v_steps[i]["x"] + v_steps[i]["w"]
        x_to = v_steps[i + 1]["x"]
        draw_arrow(draw, (x_from + 5, 260), (x_to - 5, 260), "#CF1322", width=3)

    # Bottom Half: Secure Pipeline (GREEN)
    draw_rounded_rect(draw, [40, 420, W - 40, 720], radius=12, fill="#F6FFED", outline="#B7EB8F", width=2)
    draw.text((60, 435), "🟢 SECURE MITIGATED PIPELINE (OWASP Defensive Controls)", fill="#276749", font=font_card_title)
    draw_rounded_rect(draw, [W - 260, 433, W - 60, 459], radius=4, fill="#2E7D32")
    draw.text((W - 250, 437), "ATTACK NEUTRALIZED", fill="#FFFFFF", font=font_badge)

    s_steps = [
        {"x": 60, "w": 260, "title": "1. Untrusted Input", "sub": "Same Attack Payload", "desc": ["• ' OR 1=1 #", "• <script>alert()</script>", "• 127.0.0.1 & whoami", "• ../database.sql", "• Transparent Iframe"]},
        {"x": 370, "w": 260, "title": "2. Defense Control", "sub": "Sanitization & Whitelist", "desc": ["• Parameterized bind", "• htmlspecialchars()", "• Regex IP validation", "• basename() extraction", "• X-Frame-Options: DENY"]},
        {"x": 680, "w": 260, "title": "3. Secure Gateway", "sub": "Compilation Layer", "desc": ["• Prepared statement AST", "• HTML entity encoding", "• escapeshellarg()", "• Whitelist array match", "• CSP frame-ancestors none"]},
        {"x": 990, "w": 260, "title": "4. Enforced Boundary", "sub": "Isolation Preserved", "desc": ["• Input treated as string", "• Tags rendered harmless", "• Chained commands rejected", "• Traversal paths blocked", "• Browser rejects frame"]},
        {"x": 1300, "w": 240, "title": "5. Defense Result", "sub": "Protected State", "desc": ["✅ Query logic intact", "✅ Script rendered as text", "✅ Shell execution denied", "✅ Unauthorized file blocked", "✅ UI redressing thwarted"]},
    ]

    for s in s_steps:
        draw_rounded_rect(draw, [s["x"], 475, s["x"] + s["w"], 695], radius=8, fill="#FFFFFF", outline="#D9F99D", width=1)
        draw.text((s["x"] + 15, 490), s["title"], fill="#15803D", font=font_card_title)
        draw.text((s["x"] + 15, 517), s["sub"], fill="#166534", font=get_font(13, bold=True))
        y = 550
        for d in s["desc"]:
            draw.text((s["x"] + 15, y), d, fill="#374151", font=font_body)
            y += 24

    for i in range(len(s_steps) - 1):
        x_from = s_steps[i]["x"] + s_steps[i]["w"]
        x_to = s_steps[i + 1]["x"]
        draw_arrow(draw, (x_from + 5, 585), (x_to - 5, 585), "#15803D", width=3)

    im.save(out_path, quality=95)
    print("Saved dual engine diagram to:", out_path)

# ==============================================================================
# 3. DATABASE RELATIONAL SCHEMA DIAGRAM
# ==============================================================================
def create_database_schema_diagram(out_path):
    W, H = 1600, 750
    im = Image.new("RGB", (W, H), "#F8FAFC")
    draw = ImageDraw.Draw(im)

    font_title = get_font(30, bold=True)
    font_subtitle = get_font(17, bold=False)
    font_table_name = get_font(19, bold=True)
    font_field = get_font(14, bold=False)
    font_pk = get_font(14, bold=True)
    font_badge = get_font(12, bold=True)

    # Title Banner
    draw.rectangle([0, 0, W, 75], fill="#0A2540")
    draw.text((40, 16), "SecureJobLab — Relational Database Schema & Data Dictionary", fill="#FFFFFF", font=font_title)
    draw.text((40, 48), "Database: securejoblab | Engine: InnoDB | Character Set: utf8mb4 | Collation: utf8mb4_unicode_ci", fill="#94A3B8", font=font_subtitle)

    tables = [
        {
            "name": "users", "badge": "AUTHENTICATION & RBAC", "bcolor": "#0284C7",
            "x": 60, "y": 110, "w": 340, "h": 580,
            "fields": [
                ("id", "INT AUTO_INCREMENT", "PRIMARY KEY"),
                ("username", "VARCHAR(50)", "UNIQUE, NOT NULL"),
                ("password", "VARCHAR(255)", "BCRYPT HASH"),
                ("full_name", "VARCHAR(100)", "NOT NULL"),
                ("email", "VARCHAR(120)", "NOT NULL"),
                ("role", "VARCHAR(20)", "DEFAULT 'candidate'"),
                ("created_at", "TIMESTAMP", "DEFAULT CURRENT_TIME"),
            ],
            "records": "3 Seed Users:\n• candidate (Ram Karthik)\n• recruiter (Sarah Jenkins)\n• admin (System Administrator)"
        },
        {
            "name": "jobs", "badge": "JOB POSTINGS & SQLI TARGET", "bcolor": "#DC2626",
            "x": 440, "y": 110, "w": 360, "h": 580,
            "fields": [
                ("id", "INT AUTO_INCREMENT", "PRIMARY KEY"),
                ("title", "VARCHAR(120)", "NOT NULL (SQLi Vector)"),
                ("company", "VARCHAR(120)", "NOT NULL"),
                ("location", "VARCHAR(100)", "NOT NULL"),
                ("salary", "VARCHAR(60)", "NOT NULL (INR ₹)"),
                ("job_type", "VARCHAR(50)", "DEFAULT 'Full-time'"),
                ("department", "VARCHAR(80)", "DEFAULT 'Engineering'"),
                ("description", "TEXT", "NOT NULL"),
                ("secret_notes", "TEXT", "CONFIDENTIAL DATA"),
                ("created_at", "TIMESTAMP", "DEFAULT CURRENT_TIME"),
            ],
            "records": "5 Production Roles:\n• Senior Cybersecurity Engineer (AWS)\n• AppSec Specialist (Stripe)\n• Cloud SecOps Analyst (Microsoft)\n• Full Stack Sec Engineer (Razorpay)\n• DevSecOps Automation (CRED)"
        },
        {
            "name": "applications", "badge": "APPLICATION TRACKER", "bcolor": "#16A34A",
            "x": 840, "y": 110, "w": 360, "h": 580,
            "fields": [
                ("id", "INT AUTO_INCREMENT", "PRIMARY KEY"),
                ("job_title", "VARCHAR(120)", "NOT NULL"),
                ("company", "VARCHAR(120)", "NOT NULL"),
                ("applicant_name", "VARCHAR(100)", "NOT NULL"),
                ("email", "VARCHAR(120)", "NOT NULL"),
                ("phone", "VARCHAR(30)", "NOT NULL"),
                ("experience", "VARCHAR(50)", "NOT NULL"),
                ("cover_note", "TEXT", "NOT NULL"),
                ("resume_file", "VARCHAR(255)", "LOCAL PATH"),
                ("status", "VARCHAR(50)", "DEFAULT 'In Review'"),
                ("applied_at", "TIMESTAMP", "DEFAULT CURRENT_TIME"),
            ],
            "records": "Candidate Applications:\n• AWS Senior Cybersecurity Eng\n  Status: 'Interview Scheduled'\n• Stripe AppSec Specialist\n  Status: 'Under Review'\n• Candidate: Ram Karthik"
        },
        {
            "name": "feedback", "badge": "ENDORSEMENTS & REVIEWS", "bcolor": "#D97706",
            "x": 1240, "y": 110, "w": 300, "h": 580,
            "fields": [
                ("id", "INT AUTO_INCREMENT", "PRIMARY KEY"),
                ("author", "VARCHAR(100)", "NOT NULL"),
                ("comment", "TEXT", "NOT NULL"),
                ("created_at", "TIMESTAMP", "DEFAULT CURRENT_TIME"),
            ],
            "records": "Evaluation Feedback:\n• Tech Recruiter (AWS):\n  'Outstanding technical depth\n   in secure code review'\n• Lead Sec Architect (Stripe):\n  'Solid OWASP defense skills'"
        },
    ]

    for t in tables:
        draw_rounded_rect(draw, [t["x"], t["y"], t["x"] + t["w"], t["y"] + t["h"]], radius=10, fill="#FFFFFF", outline="#CBD5E1", width=2)
        # Header
        draw_rounded_rect(draw, [t["x"], t["y"], t["x"] + t["w"], t["y"] + 55], radius=10, fill="#0F172A", outline="#0F172A", width=1)
        draw.text((t["x"] + 15, t["y"] + 15), t["name"], fill="#FFFFFF", font=font_table_name)
        # Badge
        draw_rounded_rect(draw, [t["x"] + 15, t["y"] + 65, t["x"] + t["w"] - 15, t["y"] + 88], radius=4, fill=t["bcolor"])
        draw.text((t["x"] + 25, t["y"] + 69), t["badge"], fill="#FFFFFF", font=font_badge)

        # Fields
        y = t["y"] + 105
        for field, ftype, constraint in t["fields"]:
            is_pk = "PRIMARY KEY" in constraint
            is_secret = "CONFIDENTIAL" in constraint or "SQLi" in constraint
            bg_field = "#FEF2F2" if is_secret else ("#EFF6FF" if is_pk else "#F8FAFC")
            draw_rounded_rect(draw, [t["x"] + 10, y, t["x"] + t["w"] - 10, y + 28], radius=4, fill=bg_field)
            col_font = font_pk if is_pk else font_field
            text_color = "#DC2626" if is_secret else ("#1D4ED8" if is_pk else "#1E293B")
            draw.text((t["x"] + 18, y + 5), f"{field}", fill=text_color, font=col_font)
            draw.text((t["x"] + 125, y + 5), f"{ftype}", fill="#64748B", font=font_field)
            if is_pk:
                draw.text((t["x"] + t["w"] - 85, y + 5), "[PK]", fill="#1D4ED8", font=font_pk)
            y += 33

        # Records sample box
        draw_rounded_rect(draw, [t["x"] + 10, t["y"] + 440, t["x"] + t["w"] - 10, t["y"] + t["h"] - 15], radius=6, fill="#F1F5F9", outline="#E2E8F0", width=1)
        draw.text((t["x"] + 18, t["y"] + 448), "Live Seed Data Sample:", fill="#0F172A", font=get_font(13, bold=True))
        y_rec = t["y"] + 472
        for line in t["records"].split("\n"):
            draw.text((t["x"] + 18, y_rec), line, fill="#475569", font=get_font(12, bold=False))
            y_rec += 18

    # Relationships
    draw_arrow(draw, (400, 240), (440, 240), "#0284C7", width=2)
    draw_arrow(draw, (800, 280), (840, 280), "#16A34A", width=2)

    im.save(out_path, quality=95)
    print("Saved database schema diagram to:", out_path)

if __name__ == "__main__":
    out_dir = r"C:\Users\Ram\Desktop\SecureWebLab"
    create_architecture_diagram(os.path.join(out_dir, "diagram_architecture.png"))
    create_dual_engine_diagram(os.path.join(out_dir, "diagram_dual_engine.png"))
    create_database_schema_diagram(os.path.join(out_dir, "diagram_db_schema.png"))
