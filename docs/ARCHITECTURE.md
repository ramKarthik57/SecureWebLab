# SecureJobLab: System Architecture & Defensive Design
**Course Code:** 20CYS403 — Web Application Security  
**Student:** Ram Karthik G  
**Application Architecture:** Modular PHP 8.x + MySQLi / MariaDB + Apache (XAMPP) + Bootstrap 5  
**Core Target Scope:** Exactly 5 Application Security Vulnerabilities (CWE-89, CWE-79, CWE-78, CWE-22, CWE-1021)

---

## 1. Architectural Overview

SecureJobLab is engineered as a full-featured recruitment web portal featuring an integrated educational AppSec laboratory. The application employs a **Dual-Mode Security Engine** that enables developers and evaluators to observe the exact operational contrast between vulnerable implementations and enterprise-grade defensive mitigations.

```
                      +---------------------------------------+
                      |         Web Client / Evaluator        |
                      +---------------------------------------+
                                          |
                                HTTP GET / POST Requests
                                          v
                      +---------------------------------------+
                      |       Apache HTTP Server (XAMPP)      |
                      +---------------------------------------+
                                          |
                      +-------------------+-------------------+
                      |                                       |
                      v                                       v
         +-------------------------+             +-------------------------+
         |  Dual-Mode Controller   |             | Centralized Config      |
         |  (vulnerable vs secure) |             | (config.php)            |
         +-------------------------+             +-------------------------+
                      |                                       |
          +-----------+-----------+                           v
          |                       |              +-------------------------+
          v                       v              | MariaDB / MySQL         |
    🔴 Vulnerable           🟢 Secure             | (Strict MySQLi Engine)  |
    Execution Engine        Defensive Engine     +-------------------------+
    (CWE-89, CWE-79,        (Prepared Stmts,
     CWE-78, CWE-22,         htmlspecialchars,
     CWE-1021)               escapeshellarg,
                             basename+whitelist,
                             X-Frame-Options)
```

---

## 2. Directory Structure

```
SecureWebLab/
├── config.php                  # Centralized database & session bootstrap
├── config.example.php          # Template for environment configuration
├── database.sql                # Complete MariaDB relational schema & seed data
├── index.php                   # Core portal UI, job board, & in-page laboratory
├── api.php                     # Central state-changing AJAX endpoint & upload handler
├── login.php                   # Authentication gateway (bcrypt password_verify)
├── view_resume.php             # Canonical Path Traversal (CWE-22) target
├── view_document.php           # Canonical 302 forwarder to view_resume.php
├── diagnostics.php             # Canonical OS Command Injection (CWE-78) gateway
├── clickjack_target.php        # Canonical Clickjacking (CWE-1021) target endpoint
├── clickjack.php               # Standalone clickjacking sandbox
├── lab_private_target.txt      # Synthetic sensitive target for traversal labs
├── uploads/
│   └── resumes/                # Safe resume storage directory
├── images/                     # Project screenshots, diagrams, and UI assets
├── docs/                       # Academic documentation & test matrices
│   ├── DEMO_RUNBOOK.md         # Evaluator step-by-step demonstration runbook
│   ├── TEST_MATRIX.md          # Comprehensive vulnerability & defense test matrix
│   └── ARCHITECTURE.md         # System architecture & defensive design
├── scripts/                    # Report generation and validation tooling
│   ├── generate_report.py      # Primary academic DOCX report builder
│   ├── convert_to_pdf.py       # Word COM-based PDF conversion script
│   ├── render_pdf_pages.py     # PDF visual validation & screenshot renderer
│   └── validate_project.py     # Comprehensive codebase automated audit tool
└── README.md                   # Primary project presentation and documentation
```

---

## 3. The Dual-Mode Execution Architecture

The core philosophy of SecureJobLab is **comparative side-by-side evaluation**. The application implements an explicit parameter:

```php
$mode = isset($_GET['mode']) ? $_GET['mode'] : (isset($_COOKIE['lab_mode']) ? $_COOKIE['lab_mode'] : 'vulnerable');
$is_vuln = ($mode === 'vulnerable');
```

When evaluated, every vulnerability module executes through branch logic that demonstrates the vulnerability when `$is_vuln` is true, and demonstrates enterprise defense when false.

### Database Abstraction: MySQLi Exclusivity
The project strictly employs PHP's native **MySQLi procedural and object-oriented driver** (`mysqli_*`), avoiding PDO abstraction to demonstrate low-level parameter binding:
- **Prepared Statements:** `mysqli_prepare($conn, $sql)`
- **Parameter Binding:** `mysqli_stmt_bind_param($stmt, 's', $param)`
- **Execution:** `mysqli_stmt_execute($stmt)`
- **Result Extraction:** `mysqli_stmt_get_result($stmt)`

---

## 4. Supporting Platform Security Architecture

Outside of the 5 targeted vulnerability demonstrations, SecureJobLab implements platform defense-in-depth:

1. **Authentication:**
   - Plaintext passwords are strictly rejected.
   - All passwords use `password_hash($pass, PASSWORD_BCRYPT)` and verify via `password_verify()`.
   - `session_regenerate_id(true)` prevents session fixation attacks upon authentication.
2. **Access Control:**
   - Role boundaries are enforced server-side.
   - Self-registration is restricted to the `candidate` role.
   - Privileged operations (`add_job`, `delete_job`, `reseed_db`) verify session role before processing.
3. **File Upload Hardening:**
   - Maximum upload size restricted to 5 Megabytes.
   - Safe extension whitelist: `.pdf`, `.txt`, `.docx`.
   - Cryptographic random filenames via `bin2hex(random_bytes(16))` to prevent filesystem collisions and directory traversal on disk.
   - MIME verification using `finfo_file(finfo_open(FILEINFO_MIME_TYPE), $tmp_path)`.
