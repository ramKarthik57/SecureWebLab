#!/usr/bin/env python3
"""
validate_project.py - Comprehensive Academic & Technical Project Validator
SecureJobLab (Course: 20CYS403 - Web Application Security)
Student: Ram Karthik G
"""

import os
import re
import sys
import subprocess

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASS = "[PASS]"
FAIL = "[FAIL]"
WARN = "[WARN]"

errors = []
warnings = []

def check(condition, message):
    if condition:
        print(f"  {PASS} {message}")
        return True
    else:
        print(f"  {FAIL} {message}")
        errors.append(message)
        return False

def warn_if(condition, message):
    if condition:
        print(f"  {WARN} {message}")
        warnings.append(message)
        return False
    else:
        print(f"  {PASS} {message}")
        return True

print("\n" + "="*70)
print("  SECUREJOBLAB AUTOMATED AUDIT & VALIDATION SUITE")
print("  Course: 20CYS403 — Web Application Security")
print("  Student: Ram Karthik G")
print("="*70 + "\n")

# 1. Check Core Required Files
print("[1] Inspecting Core Files Structure...")
core_files = [
    "config.php",
    "config.example.php",
    "database.sql",
    "index.php",
    "api.php",
    "login.php",
    "view_resume.php",
    "view_document.php",
    "diagnostics.php",
    "clickjack_target.php",
    "clickjack.php",
    "lab_private_target.txt",
    "README.md",
    "docs/DEMO_RUNBOOK.md",
    "docs/TEST_MATRIX.md",
    "docs/ARCHITECTURE.md",
    "scripts/generate_report.py",
    "scripts/convert_to_pdf.py",
    "SecureJobLab_Web_Application_Security_Report.docx",
    "SecureJobLab_Web_Application_Security_Report.pdf",
]
for cf in core_files:
    full_path = os.path.join(PROJECT_DIR, cf)
    check(os.path.exists(full_path), f"Required file exists: {cf}")

# 2. Check Data Hygiene - No plaintext credentials.txt
print("\n[2] Checking Sensitive Data Hygiene & Synthetic Fixtures...")
cred_path = os.path.join(PROJECT_DIR, "credentials.txt")
check(not os.path.exists(cred_path), "credentials.txt completely removed from working tree")

synth_target = os.path.join(PROJECT_DIR, "lab_private_target.txt")
if os.path.exists(synth_target):
    with open(synth_target, "r", encoding="utf-8") as f:
        synth_content = f.read()
    check("synthetic_training_artifact" in synth_content, "lab_private_target.txt contains synthetic marker")
    check("SECUREJOBLAB_FLAG" in synth_content, "lab_private_target.txt contains demo capture flag")
else:
    errors.append("lab_private_target.txt missing")

# 3. Check PHP Syntax Linting
print("\n[3] Linting PHP Codebases...")
php_bin = r"C:\xampp\php\php.exe"
if os.path.exists(php_bin):
    php_files = ["index.php", "api.php", "login.php", "view_resume.php", "view_document.php", "diagnostics.php", "config.php", "clickjack_target.php", "clickjack.php"]
    for pf in php_files:
        pf_path = os.path.join(PROJECT_DIR, pf)
        res = subprocess.run([php_bin, "-l", pf_path], capture_output=True, text=True)
        check(res.returncode == 0, f"PHP Syntax Clean: {pf}")
else:
    warn_if(True, "PHP binary not found at C:\\xampp\\php\\php.exe; skipping php -l lint")

# 4. Check for Prohibited Strings & Strict Constraints
print("\n[4] Enforcing Strict Constraints & Hygiene...")
scan_files = [
    "index.php", "api.php", "login.php", "view_resume.php", 
    "view_document.php", "diagnostics.php", "config.php", 
    "README.md", "docs/DEMO_RUNBOOK.md", "docs/TEST_MATRIX.md", "docs/ARCHITECTURE.md"
]

for sf in scan_files:
    p = os.path.join(PROJECT_DIR, sf)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            # Must not reference credentials.txt
            check("credentials.txt" not in content, f"No legacy 'credentials.txt' in {sf}")
            # Must not claim PDO (we use MySQLi)
            if sf.endswith(".php") and sf != "config.example.php":
                check("PDO" not in content, f"Strict MySQLi driver (No PDO references) in {sf}")
            # Must not contain hardcoded login bypasses
            if sf == "login.php":
                check("password === 'candidate123'" not in content, "No hardcoded password bypass in login.php")
                check("password === 'admin123'" not in content, "No hardcoded admin bypass in login.php")

# 5. Check Scope: Exactly 5 Vulnerabilities
print("\n[5] Scope Verification (Exactly 5 Core Vulnerabilities)...")
index_path = os.path.join(PROJECT_DIR, "index.php")
with open(index_path, "r", encoding="utf-8") as f:
    idx_content = f.read()
check("10 APPSEC" not in idx_content, "index.php cleaned of 10-vuln references")
check("$vuln_id < 1 || $vuln_id > 5" in idx_content, "index.php bounds vuln_id strictly between 1 and 5")

readme_path = os.path.join(PROJECT_DIR, "README.md")
with open(readme_path, "r", encoding="utf-8") as f:
    readme_content = f.read()
check("file:///" not in readme_content, "README.md contains zero local file:/// paths (pure relative GitHub links)")
check("Ram Karthik G" in readme_content, "README.md cites student Ram Karthik G")

# 6. Check Report Artifacts
print("\n[6] Validating Final Academic Report Artifacts...")
docx_file = os.path.join(PROJECT_DIR, "SecureJobLab_Web_Application_Security_Report.docx")
pdf_file = os.path.join(PROJECT_DIR, "SecureJobLab_Web_Application_Security_Report.pdf")

check(os.path.exists(docx_file) and os.path.getsize(docx_file) > 100000, "DOCX Report generated (>100KB)")
check(os.path.exists(pdf_file) and os.path.getsize(pdf_file) > 1000000, "PDF Report generated with high-res figures (>1MB)")

print("\n" + "="*70)
if not errors:
    print("  ALL VALIDATION AUDITS PASSED WITH ZERO ERRORS!")
    print("  Repository is ready for academic submission and GitHub release.")
else:
    print(f"  VALIDATION COMPLETED WITH {len(errors)} ERROR(S):")
    for err in errors:
        print(f"    - {err}")
print("="*70 + "\n")

if errors:
    sys.exit(1)
sys.exit(0)
