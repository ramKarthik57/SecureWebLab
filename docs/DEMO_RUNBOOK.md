# SecureJobLab: Live Demonstration & Evaluation Runbook
**Course Code:** 20CYS403 — Web Application Security  
**Student:** Ram Karthik G  
**Application Architecture:** Modular PHP 8.x + MySQLi / MariaDB + Apache (XAMPP) + Bootstrap 5  
**Core Target Scope:** Exactly 5 Application Security Vulnerabilities (CWE-89, CWE-79, CWE-78, CWE-22, CWE-1021)

---

## 1. Laboratory Environment Setup

Before starting the evaluation, ensure that XAMPP Apache and MariaDB services are active:

1. **Start Apache and MySQL:**
   - Open **XAMPP Control Panel** and click **Start** on Apache and MySQL.
   - Alternatively via terminal: Ensure Apache listens on port `80` and MariaDB on port `3306`.
2. **Database Verification:**
   - Open your browser at `http://localhost/phpmyadmin/` or terminal `mysql -u root`.
   - Ensure the database `securejoblab` exists and contains tables: `users`, `jobs`, `applications`, `reviews`, `diagnostics_log`.
   - To reset or reseed at any time, run:
     ```bash
     mysql -u root securejoblab < database.sql
     ```
3. **Application URL:**
   - Open [http://localhost/SecureJobLab/index.php](http://localhost/SecureJobLab/index.php) in Google Chrome, Edge, or Firefox.

---

## 2. Default Seeded Credentials

| Role | Email / Username | Password | Purpose |
| :--- | :--- | :--- | :--- |
| **Candidate** | `candidate` | `candidate123` | Default applicant portal, browse jobs, test clickjacking |
| **Recruiter** | `recruiter` | `recruiter123` | Post and manage job listings |
| **Administrator** | `admin` | `admin123` | Platform settings, DB manager, command diagnostics |

*(All passwords are cryptographically hashed using standard PHP `password_hash()` with `PASSWORD_BCRYPT`.)*

---

## 3. The 5 Core Vulnerability Demonstrations

SecureJobLab provides an interactive **Dual-Mode Security Engine** toggleable in the top navbar:
- **🔴 Vulnerable Mode:** Direct parameter execution without sanitization.
- **🟢 Secure (Mitigated) Mode:** Strict input validation, prepared statements, regex whitelisting, and defensive HTTP headers.

---

### Module 1: SQL Injection (SQLi) — CWE-89
* **Location:** Search Bar on Job Listings Page / Lab Tab 3 (`index.php?tab=lab&vuln=1`)
* **Vulnerable Mechanism:** Raw input concatenation into SQL query:
  ```php
  $query = "SELECT * FROM jobs WHERE title = '$input'";
  $res = mysqli_query($conn, $query);
  ```
* **Attack Payload (Authentication / Filter Bypass):**
  ```sql
  ' OR 1=1 #
  ```
* **Evaluation Steps:**
  1. Set Mode to **🔴 Vulnerable**.
  2. In the Search Bar or Lab Module 1 input, paste `' OR 1=1 #` and click **Search / Execute Test**.
  3. **Observed Result:** The SQL condition evaluates to true for all rows; hidden jobs and administrative test listings are dumped immediately.
  4. Toggle Mode to **🟢 Secure**.
  5. Submit the identical payload `' OR 1=1 #'`.
  6. **Observed Defense:** `mysqli_prepare()` and `mysqli_stmt_bind_param('s', $input)` treat the payload as a literal string. 0 records match. The exploit is neutralized.

---

### Module 2: Stored Cross-Site Scripting (XSS) — CWE-79
* **Location:** Company Reviews / Feedback Section (`index.php?tab=lab&vuln=2`)
* **Vulnerable Mechanism:** Unescaped raw output rendering in HTML:
  ```php
  echo "<div class='review-body'>" . $review['content'] . "</div>";
  ```
* **Attack Payload (Script Execution & Cookie Access):**
  ```html
  <script>alert('XSS: ' + document.domain)</script>
  ```
* **Evaluation Steps:**
  1. Set Mode to **🔴 Vulnerable**.
  2. In the Candidate Feedback box, paste `<script>alert('XSS: ' + document.domain)</script>` and click **Submit Review**.
  3. **Observed Result:** An alert modal pops up displaying `XSS: localhost`. Arbitrary JavaScript execution is verified.
  4. Toggle Mode to **🟢 Secure**.
  5. Submit the same script payload.
  6. **Observed Defense:** `htmlspecialchars($content, ENT_QUOTES, 'UTF-8')` encodes `<` to `&lt;` and `>` to `&gt;`. The script is rendered harmlessly as plain text on the page.

---

### Module 3: OS Command Injection — CWE-78
* **Location:** Standalone Gateway `diagnostics.php` & Admin Database Manager (`index.php?tab=admin`)
* **Vulnerable Mechanism:** Direct shell concatenation in `shell_exec()`:
  ```php
  $output = shell_exec("ping -n 1 " . $host);
  ```
* **Attack Payload (URL Parameter Modification):**
  ```text
  http://localhost/SecureJobLab/diagnostics.php?mode=vulnerable&host=127.0.0.1%20%26%20whoami
  ```
* **Evaluation Steps:**
  1. Navigate to `http://localhost/SecureJobLab/diagnostics.php?mode=vulnerable&host=127.0.0.1`.
  2. Notice the host parameter in the browser's address bar.
  3. Append ` & whoami` to the URL so it becomes:
     `http://localhost/SecureJobLab/diagnostics.php?mode=vulnerable&host=127.0.0.1%20%26%20whoami`
  4. Press Enter.
  5. **Observed Result:** The server executes `ping -n 1 127.0.0.1` followed immediately by `whoami`. The terminal viewer displays the host operating system username (`DESKTOP-XXX\User`).
  6. Switch to Secure Mode by loading:
     `http://localhost/SecureJobLab/diagnostics.php?mode=secure&host=127.0.0.1%20%26%20whoami`
  7. **Observed Defense:** The input is validated against `/^[a-zA-Z0-9.\-]+$/` and passed to `escapeshellarg()`. The dangerous `&` delimiter is detected and rejected. A green mitigation alert is returned and no shell process is spawned.

---

### Module 4: Directory / Path Traversal — CWE-22
* **Location:** Canonical Resume Document Viewer `view_resume.php` (`index.php?tab=applications`)
* **Vulnerable Mechanism:** Direct path concatenation without directory traversal validation:
  ```php
  $path = "uploads/resumes/" . $_GET['file'];
  readfile($path);
  ```
* **Attack Payload (Synthetic Target Extraction):**
  ```text
  http://localhost/SecureJobLab/view_resume.php?mode=vulnerable&file=../lab_private_target.txt
  ```
* **Evaluation Steps:**
  1. Log in as `candidate` and go to **My Applications** (`tab=applications`).
  2. Click **"Click me to view resume"** button. The document viewer loads `resume.txt`.
  3. In the browser URL bar, edit the query parameter to:
     `http://localhost/SecureJobLab/view_resume.php?mode=vulnerable&file=../lab_private_target.txt`
  4. Press Enter.
  5. **Observed Result:** The path traversal escapes `uploads/resumes/` and dumps `lab_private_target.txt`, revealing the synthetic flag:
     `DEMO_SECRET=SECUREJOBLAB_FLAG{DIR_TRAVERSAL_CWE22_VERIFIED}`
  6. Test secure mitigation by changing mode:
     `http://localhost/SecureJobLab/view_resume.php?mode=secure&file=../lab_private_target.txt`
  7. **Observed Defense:** The endpoint isolates `basename($_GET['file'])` and checks against an explicit document whitelist (`['resume.txt', 'coverletter.txt', 'certificate.txt', 'skills.txt']`). The request returns `HTTP 403 Forbidden` with a security mitigation log.

---

### Module 5: Clickjacking / UI Redressing — CWE-1021
* **Location:** Home Dashboard Decoy Button (`index.php`) & Target Endpoint `clickjack_target.php`
* **Vulnerable Mechanism:** Missing framing headers (`X-Frame-Options` and `Content-Security-Policy: frame-ancestors`):
  ```php
  // No defensive headers emitted by vulnerable endpoint
  ```
* **Evaluation Steps:**
  1. On the home page (`index.php`), locate the attractive gold promotional box:
     **"Click & Pay ₹499 to Get Premium Version"**.
  2. By default, the embedded iframe has an opacity of `0%` (Stealth Mode).
  3. Use the **Iframe Transparency Slider** below the button to drag opacity to `50%` or `100%`.
  4. **Observed Vulnerability:** At 50% / 100%, observe that the decoy button sits directly underneath a red **"Permanently Delete Account & Wipe Data"** button served from `clickjack_target.php`.
  5. In 0% opacity mode, when the user clicks what appears to be the payment button, the browser transmits the click event to the target iframe, triggering account deletion.
  6. Toggle to **🟢 Secure Mode**.
  7. **Observed Defense:** `clickjack_target.php?mode=secure` sends:
     ```http
     X-Frame-Options: DENY
     Content-Security-Policy: frame-ancestors 'none'
     ```
     The modern browser refuses to embed the frame inside any external or parent page, rendering a gray framing blocked error and defeating UI redressing.

---

## 4. Supporting Hardening (Not Part of the 5 Labs)

- **Centralized Configuration (`config.php`):** Centralized DB connection factory and session management.
- **Strict Role-Based Signup:** Public self-registration permits only the `candidate` role. Privileged accounts (`recruiter`, `admin`) can only be provisioned via database seed.
- **Safe File Uploads:** Uploads in `api.php` enforce a 5MB limit, check MIME types via PHP `finfo`, validate against a safe extension whitelist (`pdf`, `txt`, `docx`), and store files under randomized cryptographic hashes (`bin2hex(random_bytes(16))`).
- **Data Hygiene:** No real credentials are stored in plaintext. Synthetic fixtures (`lab_private_target.txt`) are utilized for educational demonstration.
