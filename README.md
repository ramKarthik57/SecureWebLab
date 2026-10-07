# 🛡️ SecureJobLab (SecureWebLab)
### Full-Stack Web Application Security Dual-Engine Exploitation & Defense Lab

[![Course](https://img.shields.io/badge/Course-20CYS403%20Web%20Application%20Security-blue.svg)](https://github.com/ramKarthik57)
[![PHP](https://img.shields.io/badge/PHP-8.1%2B-777BB4.svg?logo=php&logoColor=white)](https://www.php.net/)
[![Database](https://img.shields.io/badge/Database-MySQL%20%2F%20MariaDB-4479A1.svg?logo=mysql&logoColor=white)](https://mariadb.org/)
[![Server](https://img.shields.io/badge/Server-Apache%20%2F%20XAMPP-D22128.svg?logo=apache&logoColor=white)](https://www.apachefriends.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Overview

**SecureJobLab** is a comprehensive, production-grade cybersecurity training and demonstration web application developed for **20CYS403 Web Application Security**. Designed around a modern high-scale corporate recruitment portal persona (*Ram Karthik, Candidate & AppSec Specialist*), the platform features a real-time **Dual-Engine Architecture** that allows security analysts, educators, and students to switch instantly between **🔴 Intentionally Vulnerable** and **🟢 Mitigated / Secured** runtime modes.

Every security control is mapped directly to standard **Common Weakness Enumerations (CWE)** and **OWASP Top 10** categories with side-by-side terminal logs, URL parameter manipulation interfaces, and exploit verification telemetry.

---

## 🏛️ System Architecture

```
                                  +---------------------------------------+
                                  |         Client Web Browser            |
                                  |  (Address Bar Parameter Manipulation) |
                                  +-------------------+-------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |         Apache HTTP Server            |
                                  |       (XAMPP Web Root: /htdocs)       |
                                  +-------------------+-------------------+
                                                      |
                   +----------------------------------+----------------------------------+
                   |                                                                     |
                   v                                                                     v
    +------------------------------+                                      +------------------------------+
    |   🔴 VULNERABLE ENGINE       |                                      |     🟢 SECURE ENGINE         |
    |   (Live Attack Demonstrations|                                      |   (Defense-in-Depth Defenses)|
    +------------------------------+                                      +------------------------------+
    | * Raw Concatenated SQL       |                                      | * PDO Prepared Statements    |
    | * Raw innerHTML / Reflected  |                                      | * htmlspecialchars() + CSP  |
    | * Relative Path Traversal    |                                      | * basename() + Whitelist     |
    | * shell_exec() Unsanitized   |                                      | * Command Whitelist Policy   |
    | * Framing Permitted          |                                      | * X-Frame-Options: DENY      |
    | * Direct ID Object Binding   |                                      | * Strict RBAC Ownership      |
    +------------------------------+                                      +------------------------------+
                   |                                                                     |
                   +----------------------------------+----------------------------------+
                                                      |
                                                      v
                                  +---------------------------------------+
                                  |        MariaDB / MySQL Database       |
                                  |    (securejoblab & Credentials)       |
                                  +---------------------------------------+
```

---

## 🎯 Top Vulnerability Demonstrations & Realtime Controls

### 1. 📂 Path / Directory Traversal (CWE-22)
* **Realtime Interface**: [view_resume.php](file:///C:/Users/Ram/Desktop/SecureWebLab/view_resume.php)
* **How It Works**: The application loads candidate documentation via URL address bar parameter (`?file=resume.txt`).
* **🔴 Vulnerable Mode**: Passing parent traversal sequences (`?file=../credentials.txt`) escapes the root storage directory and exposes the server's confidential credential vault:
  ```http
  GET /SecureJobLab/view_resume.php?file=../credentials.txt
  ```
  *Result*: All 12 system usernames and passwords are dump-reflected directly on screen.
* **🟢 Secure Mode**: Canonical path resolution with `basename()` and whitelist verification intercepts directory climbing, immediately returning `403 Forbidden`.

---

### 2. ⚡ OS Command Injection (CWE-78)
* **Realtime Interface**: Database Manager Tab (`index.php?tab=admin`)
* **How It Works**: Clicking **`[Check whether DB is alive and connected]`** executes a local network ping probe, displaying the executed command directly in the browser's URL:
  ```http
  GET /SecureJobLab/index.php?tab=admin&cmd=ping -n 1 127.0.0.1
  ```
* **🔴 Vulnerable Mode**: The user alters the URL address bar to inject secondary shell commands:
  ```http
  GET /SecureJobLab/index.php?tab=admin&cmd=whoami
  # or using delimiter:
  GET /SecureJobLab/index.php?tab=admin&cmd=ping -n 1 127.0.0.1 & whoami
  ```
  *Result*: Windows shell executes `whoami` and reflects host server identity (e.g. `laptop-6m028ulj\ram`) inside the live terminal console.
* **🟢 Secure Mode**: A strict command whitelist intercepts the request. Any command diverging from `ping -n 1 127.0.0.1` is rejected without invoking system shell utilities.

---

### 3. 🎭 Clickjacking / UI Redressing (CWE-1021)
* **Realtime Interface**: [index.php](file:///C:/Users/Ram/Desktop/SecureWebLab/index.php) (Integrated Promotion Card)
* **Target Endpoint**: [clickjack_target.php](file:///C:/Users/Ram/Desktop/SecureWebLab/clickjack_target.php)
* **How It Works**: An attractive promotional decoy card (*"⭐ Get Premium Version of This App! Pay ₹499"*) is displayed on the index page. An invisible `<iframe>` is overlaid directly on top at **0% stealth opacity by default**.
* **Pixel-Perfect Alignment**: Both buttons share identical absolute coordinates:
  ```css
  position: absolute;
  bottom: 25px;
  left: 50%;
  transform: translateX(-50%);
  width: 440px;
  height: 46px;
  border-radius: 50px;
  ```
* **🔴 Vulnerable Mode**: When an unsuspecting user clicks the decoy button, their click is secretly consumed by the transparent iframe's `⚠️ Permanently Delete Account & Wipe Data` button, triggering immediate fabricated account destruction and live alert feedback.
* **Slider Inspection**: Demonstrators can drag the transparency slider from `0%` to `100%` to expose the underlying red destructive button to reviewers.
* **🟢 Secure Mode**: `X-Frame-Options: DENY` and `Content-Security-Policy: frame-ancestors 'none'` headers prevent the browser from loading the target inside an iframe.

---

### 4. 💉 SQL Injection (CWE-89)
* **Realtime Interface**: Realtime AJAX Job Search (`index.php` & `api.php`)
* **🔴 Vulnerable Mode**: Dynamic SQL query concatenation allows authentication bypass and wildcard record leakage:
  ```sql
  SELECT * FROM jobs WHERE title LIKE '%' OR '1'='1' -- %'
  ```
* **🟢 Secure Mode**: Parameterized queries using prepared statements ensure that user input is treated strictly as literal data.

---

### 5. ☣️ Cross-Site Scripting — Stored & Reflected (CWE-79)
* **Realtime Interface**: Job Post Title Reflection & Candidate Feedback Notes
* **🔴 Vulnerable Mode**: Raw HTML insertion triggers arbitrary JavaScript execution:
  ```html
  <script>alert('XSS Exploit Triggered')</script>
  <img src=x onerror="alert(document.cookie)">
  ```
* **🟢 Secure Mode**: Strict contextual encoding (`htmlspecialchars(..., ENT_QUOTES, 'UTF-8')`) neutralizes markup.

---

## 🗂️ Repository Directory Structure

```
SecureWebLab/
├── docs/                 # Documentation & academic guides
├── images/               # Architecture diagrams and system screenshots
│   ├── diagram_architecture.png
│   ├── diagram_db_schema.png
│   ├── diagram_dual_engine.png
│   └── screenshot_*_verified.png
├── scripts/              # Python automation and report generators
│   ├── build_complete_academic_report.py
│   ├── convert_to_pdf.py
│   └── generate_diagrams.py
├── uploads/              # Document storage & candidate resume uploads
├── lab_files/            # Training/lab materials (txt documents)
├── lab_5vuln_screenshots/# Exploit verification gallery
├── api.php               # RESTful API handler (AJAX Search, CRUD, Ping)
├── clickjack.php         # Clickjack sandbox dispatcher
├── clickjack_target.php  # High-impact destructive target action
├── credentials.txt       # Confidential system credential vault (CWE-22 target)
├── database.sql          # Schema dump with 12 seed user accounts
├── diagnostics.php       # Standalone Network Ping diagnostic tool
├── index.php             # Master recruitment platform & dual-engine core
├── login.php             # Authentication portal with credential feedback
├── logout.php            # Secure session termination
├── view_document.php     # Document preview rendering engine
├── view_resume.php       # Document viewer with address bar parameter control
├── SecureJobLab_Web_Application_Security_Report.docx  # Academic Project Report (DOCX)
├── SecureJobLab_Web_Application_Security_Report.pdf   # Academic Project Report (PDF)
├── .gitignore            # Git ignore specification
├── LICENSE               # MIT Open Source License
└── README.md             # Project documentation (this file)
```

---

## 🚀 Setup & Installation Guide

### Prerequisites
* **XAMPP** (recommended) or any Apache 2.4+ / PHP 8.1+ stack with `mysqli` extension enabled.
* **MariaDB** or **MySQL** (default port: `3306`).
* Modern Web Browser (Google Chrome, Firefox, Microsoft Edge).

### Installation Steps

1. **Clone or Copy Repository**:
   Copy the repository folder into your XAMPP web root directory:
   ```bash
   # Windows XAMPP default path
   C:\xampp\htdocs\SecureJobLab
   ```

2. **Initialize Database**:
   * Open **phpMyAdmin** (`http://localhost/phpmyadmin/`) or MySQL CLI.
   * Import the [database.sql](database.sql) file:
     ```sql
     mysql -u root -p < database.sql
     ```
   * This automatically creates the `securejoblab` database and provisions all seed records.

3. **Start Apache & MySQL**:
   * Open the **XAMPP Control Panel**.
   * Start both **Apache** and **MySQL** services.

4. **Access the Application**:
   * Navigate to: [http://localhost/SecureJobLab/](http://localhost/SecureJobLab/)

---

## 🔑 Default Test Credentials

All accounts are pre-seeded in `database.sql` with hashed passwords:

| No. | Username | Password | Role | Persona Description |
|:---:|:---|:---|:---:|:---|
| 1 | `candidate` | `candidate123` | Candidate | **Ram Karthik** (Lead AppSec Specialist) |
| 2 | `ram.karthik` | `candidate123` | Candidate | Ram Karthik (Candidate Profile) |
| 3 | `admin` | `admin123` | Administrator | System Administrator |
| 4 | `recruiter` | `candidate123` | Company | Sarah Jenkins (Tech Recruiter) |
| 5 | `sarah.recruiter` | `Recruit@2026` | Company | Sarah Jenkins (Lead Talent Acquisition) |
| 6 | `vikram.sharma` | `VikramSec#2026` | Candidate | Vikram Sharma (Staff AppSec) |
| 7 | `priya.nair` | `PriyaApp#2026` | Candidate | Priya Nair (Cloud Security) |
| 8 | `arun.devsec` | `ArunSec#2026` | Candidate | Arun Kumar (DevSecOps Lead) |
| 9 | `ananya.audit` | `AnanyaPci#2026` | Company | Ananya Sen (Compliance Auditor) |
| 10 | `rohit.soc` | `RohitSoc#2026` | Candidate | Rohit Verma (SOC Analyst L2) |
| 11 | `meera.pentest` | `MeeraPen#2026` | Candidate | Meera Patel (Penetration Tester) |
| 12 | `karthik.manager` | `ManagerSec#2026` | Administrator | Karthik Rajan (Infosec Manager) |

---

## 📄 Academic Project Report

A publication-quality 31-page academic project report is bundled with this repository:
* 📑 **PDF Edition**: [SecureJobLab_Web_Application_Security_Report.pdf](SecureJobLab_Web_Application_Security_Report.pdf)
* 📝 **Word Edition**: [SecureJobLab_Web_Application_Security_Report.docx](SecureJobLab_Web_Application_Security_Report.docx)

---

## ⚖️ Legal & Educational Disclaimer

This project is created strictly for **educational, academic, and authorized defensive testing purposes** under the course syllabus of **20CYS403 Web Application Security**. All vulnerabilities and offensive capabilities are isolated within a controlled local environment. Unauthorized execution against systems without prior explicit written consent is illegal.

---

**Author**: Ram Karthik  
**Course**: 20CYS403 Web Application Security  
**Institution**: Amrita Vishwa Vidyapeetham
