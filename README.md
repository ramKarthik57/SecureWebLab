# SecureJobLab: Modern Web Application Security Evaluation & Defensive Engineering
**Course Code:** 20CYS403 — Web Application Security  
**Student:** Ram Karthik G  
**Institution:** Amrita Vishwa Vidyapeetham  
**Repository:** [https://github.com/ramKarthik57/SecureWebLab](https://github.com/ramKarthik57/SecureWebLab)

---

## Executive Overview

**SecureJobLab** (also referenced as **SecureWebLab**) is an enterprise recruitment platform engineered for comparative web application security research and academic laboratory evaluation. Built on a modular PHP 8.x stack with Apache and MariaDB, the platform features a real-time **Dual-Mode Security Engine** that contrasts vulnerable software implementations against industry-standard defensive controls.

The platform provides live demonstrations for **exactly 7 core application security vulnerabilities**:
1. **SQL Injection (SQLi)** — CWE-89
2. **Cross-Site Scripting (XSS)** — CWE-79
3. **OS Command Injection** — CWE-78
4. **Directory / Path Traversal** — CWE-22
5. **Clickjacking / UI Redressing** — CWE-1021
6. **Insecure File Upload** — CWE-434
7. **Cross-Site Request Forgery (CSRF)** — CWE-352

```mermaid
graph TD
    Client["Browser / Evaluator Client"]
    Server["Apache HTTP Server / XAMPP"]
    Engine["Dual-Mode Security Engine (lab_mode)"]
    
    VulnBranch["🔴 Vulnerable Mode"]
    SecBranch["🟢 Secure Mitigated Mode"]
    
    DB["MariaDB Database (MySQLi Driver)"]
    FS["Local Server Filesystem (lab_private_target.txt / uploads)"]
    OS["Host Operating System Shell"]
    
    Client -->|HTTP GET / POST| Server
    Server --> Engine
    
    Engine -->|mode=vulnerable| VulnBranch
    Engine -->|mode=secure| SecBranch
    
    VulnBranch -->|Raw SQL Concatenation| DB
    VulnBranch -->|Unencoded Output| Client
    VulnBranch -->|Unsanitized shell_exec| OS
    VulnBranch -->|Unrestricted readfile| FS
    VulnBranch -->|Framing Permitted| Client
    VulnBranch -->|Unrestricted .php upload| FS
    VulnBranch -->|Unprotected State Change| DB
    
    SecBranch -->|mysqli_prepare & bind_param| DB
    SecBranch -->|htmlspecialchars ENT_QUOTES| Client
    SecBranch -->|Regex Whitelist & escapeshellarg| OS
    SecBranch -->|basename & Whitelist (403)| FS
    SecBranch -->|X-Frame-Options DENY| Client
    SecBranch -->|Allowlist + finfo + hash rename| FS
    SecBranch -->|CSRF Token & Origin Verification| DB
```

---

## The 7 Core Vulnerabilities & Defense Matrix

| # | Vulnerability Class | CWE ID | Vulnerable Code Pattern | Primary Exploit Payload | Defensive Implementation |
|---|---|---|---|---|---|
| **1** | **SQL Injection (SQLi)** | CWE-89 | Raw string interpolation into SQL query | `' OR 1=1 #` | Parametric SQL queries via MySQLi prepared statements (`mysqli_prepare`, `mysqli_stmt_bind_param`) |
| **2** | **Cross-Site Scripting (XSS)** | CWE-79 | Unescaped user feedback rendered directly to HTML | `<script>alert('XSS: ' + document.domain)</script>` | Context-aware output encoding via `htmlspecialchars($val, ENT_QUOTES, 'UTF-8')` |
| **3** | **OS Command Injection** | CWE-78 | Unsanitized concatenation in `shell_exec()` | `127.0.0.1 & whoami` (via URL parameter `?host=`) | Strict regex validation (`/^[a-zA-Z0-9.\-]+$/`) combined with `escapeshellarg()` |
| **4** | **Directory / Path Traversal** | CWE-22 | Direct relative file path load without sanitization | `../lab_private_target.txt` (via URL parameter `?file=`) | Path isolation via `basename()` and strict whitelist lookup (`in_array()`) returning HTTP 403 Forbidden |
| **5** | **Clickjacking (UI Redressing)** | CWE-1021 | Missing defensive framing HTTP headers | Transparent iframe overlay over decoy "Claim Premium" button | Defensive HTTP headers: `X-Frame-Options: DENY` and `Content-Security-Policy: frame-ancestors 'none'` |
| **6** | **Insecure File Upload** | CWE-434 | Direct client filename trust & no extension validation | `shell.php` with PHP executable code | Strict extension allowlist (`pdf`, `txt`, `docx`), MIME verification via `finfo`, and cryptographic renaming (`bin2hex(random_bytes(16))`) |
| **7** | **Cross-Site Request Forgery (CSRF)** | CWE-352 | State-changing request accepted without origin or anti-CSRF token verification | Cross-origin forged POST changing candidate profile | Cryptographic anti-CSRF token generated via `random_bytes(32)`, bound to session, verified via `hash_equals()` |

---

## Evaluation & Demonstration Quickstart

### Prerequisites
- **XAMPP** (Apache 2.4+ and MariaDB/MySQL 10.4+)
- **PHP 8.0+** with `mysqli` and `fileinfo` extensions enabled

### Setup Instructions
1. Clone or copy the project into your local web root:
   ```bash
   git clone https://github.com/ramKarthik57/SecureWebLab.git C:/xampp/htdocs/SecureJobLab
   ```
2. Start **Apache** and **MySQL** via the XAMPP Control Panel.
3. Import the relational database schema:
   ```bash
   mysql -u root securejoblab < C:/xampp/htdocs/SecureJobLab/database.sql
   ```
4. Access the web application:
   - **URL:** [http://localhost/SecureJobLab/index.php](http://localhost/SecureJobLab/index.php)

---

## Seeded Evaluation Accounts

| Role | Username / Email | Password | Intended Evaluation Activity |
|:---|:---|:---|:---|
| **Candidate** | `candidate` | `candidate123` | Portal exploration, job applications, resume viewing, in-page clickjacking |
| **Recruiter** | `recruiter` | `recruiter123` | Job listing management and review verification |
| **Administrator** | `admin` | `admin123` | Diagnostic tools, database maintenance, system health checks |

*(All passwords are cryptographically hashed using standard PHP `password_hash()` with `PASSWORD_BCRYPT`.)*

---

## Step-by-Step Vulnerability Demonstrations

### 1. SQL Injection (CWE-89)
* **URL:** `http://localhost/SecureJobLab/index.php?tab=lab&vuln=1`
* **Vulnerable Test:** Set mode to **Vulnerable**. Enter `' OR 1=1 #` into the search box. Notice all database records, including administrative test listings, are dumped immediately.
* **Mitigated Test:** Switch mode to **Secure**. Submit the identical payload. Notice the query treats the payload as a literal string, returning zero matching records.

### 2. Cross-Site Scripting (CWE-79)
* **URL:** `http://localhost/SecureJobLab/index.php?tab=lab&vuln=2`
* **Vulnerable Test:** Set mode to **Vulnerable**. In the feedback form, submit `<script>alert('XSS: ' + document.domain)</script>`. An alert modal executes in the browser context.
* **Mitigated Test:** Switch to **Secure**. Submit the same script payload. The script is safely encoded as `&lt;script&gt;` and rendered as inert plain text.

### 3. OS Command Injection (CWE-78)
* **URL:** `http://localhost/SecureJobLab/diagnostics.php?mode=vulnerable&host=127.0.0.1%20%26%20whoami`
* **Vulnerable Test:** In the browser address bar, change `?host=` to `127.0.0.1 & whoami`. The server executes both the ping and `whoami`, printing the server host username to the terminal console.
* **Mitigated Test:** Change `mode=vulnerable` to `mode=secure` in the address bar. The regex whitelist flags the illegal delimiter and blocks execution, preventing the subshell from spawning.

### 4. Directory / Path Traversal (CWE-22)
* **URL:** `http://localhost/SecureJobLab/view_resume.php?mode=vulnerable&file=../lab_private_target.txt`
* **Vulnerable Test:** Passing `../lab_private_target.txt` into `?file=` escapes the `uploads/resumes/` folder and loads the synthetic secret fixture:
  ```text
  LAB_TARGET_TYPE=synthetic_training_artifact
  DEMO_SECRET=SECUREJOBLAB_FLAG{DIR_TRAVERSAL_CWE22_VERIFIED}
  ```
* **Mitigated Test:** Change `mode=vulnerable` to `mode=secure`. The script enforces `basename()` and checks an explicit document whitelist, issuing an `HTTP 403 Forbidden` response.

### 5. Clickjacking / UI Redressing (CWE-1021)
* **URL:** `http://localhost/SecureJobLab/index.php`
* **Vulnerable Test:** In the gold promotional card, observe the **"Click & Pay ₹499 to Get Premium Version"** button. Drag the opacity slider from `0%` to `100%`. The button is actually covered by an invisible iframe containing a red **"Permanently Delete Account & Wipe Data"** button from `clickjack_target.php`.
* **Mitigated Test:** Toggle to **Secure Mode**. The server transmits `X-Frame-Options: DENY` and `Content-Security-Policy: frame-ancestors 'none'`, causing modern browsers to reject framing and neutralizing the attack.

### 6. Insecure File Upload (CWE-434)
* **URL:** `http://localhost/SecureJobLab/index.php?tab=lab&vuln=6`
* **Vulnerable Test:** Set mode to **Vulnerable**. Select preset `Webshell Simulator (eval.php)` and click **Execute Upload Test**. The server accepts the executable script without validation, writes it directly into the storage directory, and displays a red telemetry alert confirming file storage.
* **Mitigated Test:** Switch to **Secure Mode**. Submit the same `.php` payload. The defensive engine inspects the file extension against the strict allowlist (`pdf`, `txt`, `docx`), detects dangerous executable signatures, rejects the upload with an HTTP 400 Bad Request, and issues a green mitigation alert.

### 7. Cross-Site Request Forgery / CSRF (CWE-352)
* **URL:** `http://localhost/SecureJobLab/index.php?tab=lab&vuln=7`
* **Vulnerable Test:** Set mode to **Vulnerable**. Trigger the simulated cross-origin state change preset. The server updates the authenticated user's job profile and preference settings without requiring or verifying an anti-CSRF token, demonstrating cross-site execution.
* **Mitigated Test:** Switch to **Secure Mode**. Attempt the unauthorized cross-origin state change. The request is rejected immediately with an HTTP 403 Forbidden because it lacks the session-bound anti-CSRF token (`hash_equals()`).

---

## Supporting Platform Security Hardening

In addition to the 7 vulnerability modules, the platform implements defense-in-depth across supporting infrastructure:
- **Centralized Database Access:** `config.php` manages connection pooling and error suppression.
- **Role-Based Signup Restrictions:** Self-registration strictly provisions `candidate` roles; elevated privileges (`admin`, `recruiter`) cannot be self-assigned.
- **Cryptographic Anti-CSRF Token Generation:** Centralized `get_csrf_token()` and `verify_csrf_token()` functions in `config.php`.
- **Data Hygiene:** No live credentials exist in the codebase. All demonstration fixtures utilize synthetic identifiers.

---

## Academic Documentation & Research Artifacts

Detailed documentation and test artifacts are provided in the repository:
- [docs/DEMO_RUNBOOK.md](docs/DEMO_RUNBOOK.md) — Comprehensive evaluator demonstration guide.
- [docs/TEST_MATRIX.md](docs/TEST_MATRIX.md) — Comparative testing matrix (vulnerable payload vs secure mitigation).
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — System architecture and defensive design.
- [SecureJobLab_Web_Application_Security_Report.pdf](SecureJobLab_Web_Application_Security_Report.pdf) — Academic project report.

---

## Author & Academic Attribution
* **Student:** Ram Karthik G  
* **Course:** 20CYS403 — Web Application Security  
* **Degree:** B.Tech. in Computer Science and Engineering (Cybersecurity)  
* **Institution:** Amrita School of Computing, Amrita Vishwa Vidyapeetham  
