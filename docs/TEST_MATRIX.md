# SecureJobLab: Vulnerability & Defense Test Matrix
**Course Code:** 20CYS403 — Web Application Security  
**Student:** Ram Karthik G  
**Target Scope:** Exactly 5 Application Security Vulnerabilities (CWE-89, CWE-79, CWE-78, CWE-22, CWE-1021)

---

## Comparative Verification Matrix

| # | Vulnerability Class | CWE ID | Vulnerable Code Pattern | Test Exploit Payload | Expected Vulnerable Result | Defensive Implementation | Expected Secure Result |
|---|---|---|---|---|---|---|---|
| **1** | **SQL Injection (SQLi)** | CWE-89 | Raw SQL string interpolation (`"SELECT * FROM jobs WHERE title = '$input'"`) | `' OR 1=1 #` | Authentication / filter bypass; returns all database rows including administrative test records. | Parametric SQL queries via MySQLi prepared statements (`mysqli_prepare()`, `mysqli_stmt_bind_param('s', $val)`). | Payload interpreted strictly as literal parameter; zero SQL syntax manipulation; 0 unexpected records. |
| **2** | **Stored Cross-Site Scripting (XSS)** | CWE-79 | Direct output of user input into HTML document without encoding (`echo $review_content;`) | `<script>alert('XSS: ' + document.domain)</script>` | Payload executes in browser JavaScript engine; displays popup alert reading `XSS: localhost`. | Context-aware entity encoding via `htmlspecialchars($content, ENT_QUOTES, 'UTF-8')`. | Characters `<>` encoded to `&lt;&gt;`; rendered harmlessly as plain text in the DOM. |
| **3** | **OS Command Injection** | CWE-78 | Unsanitized concatenation of parameter into shell execution (`shell_exec("ping -n 1 " . $host)`) | `127.0.0.1 & whoami` (via URL parameter `?host=`) | Delimiter `&` chains secondary command; terminal displays host OS username (`NT AUTHORITY\SYSTEM` or local user). | Strict regex validation (`/^[a-zA-Z0-9.\-]+$/`) combined with `escapeshellarg()`. | Dangerous shell delimiters rejected with HTTP 400 status; no shell process executed. |
| **4** | **Directory / Path Traversal** | CWE-22 | Direct file path concatenation without directory traversal validation (`readfile("uploads/resumes/" . $file)`) | `../lab_private_target.txt` (via URL parameter `?file=`) | Relative path sequences escape directory and output synthetic target secrets from parent directory. | Path normalization via `basename()` and strict whitelist lookup (`in_array($file, $allowed_docs)`). | Path traversal sequences stripped; non-whitelisted paths rejected with HTTP 403 Forbidden. |
| **5** | **Clickjacking (UI Redressing)** | CWE-1021 | Target sensitive action rendered without frame protection headers | Embedded iframe in transparent overlay (0% opacity) covering decoy "Claim Premium" button | Clicks intended for decoy button are intercepted by hidden iframe, executing unauthorized account deletion. | Defensive HTTP response headers: `X-Frame-Options: DENY` and `Content-Security-Policy: frame-ancestors 'none'`. | Modern browsers refuse framing; displays frame blocked error; UI redressing impossible. |

---

## Supporting Security Defense Matrix

*The following defensive controls protect the application platform but are NOT part of the 5 core vulnerability demonstration labs:*

| Supporting Domain | Threat Addressed | Implementation Detail | Reference Code |
|---|---|---|---|
| **Centralized Database** | Connection leaks & inconsistent error handling | Singleton-style connection factory with automated UTF-8 charset initialization and generic error handling. | `config.php: get_db_connection()` |
| **Password Storage** | Credential exposure & cracking | Strict `password_hash()` with `PASSWORD_BCRYPT` and verification via `password_verify()`. No plaintext bypasses. | `login.php`, `database.sql` |
| **Session Security** | Session fixation & hijacking | Strict session initiation, `session_regenerate_id(true)` upon successful login, clean session destruction on logout. | `login.php`, `config.php` |
| **Privilege Escalation** | Self-assigning administrator role | Registration endpoint hardcoded to assign role `candidate` only. Privileged accounts (`recruiter`, `admin`) can only be provisioned via database seed. | `login.php: action=register` |
| **File Upload Defense** | Remote code execution via webshells | 5MB size limit, extension whitelist (`['pdf', 'txt', 'docx']`), MIME inspection using `finfo_file()`, and randomized cryptographic filenames (`bin2hex(random_bytes(16))`). | `api.php: apply_job` |
| **Data Hygiene** | Credential exposure in repository | Purely synthetic training fixtures in `lab_private_target.txt` with mock secrets (`DEMO_SECRET=SECUREJOBLAB_FLAG{...}`). | `lab_private_target.txt` |
