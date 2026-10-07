<?php
// ====================================================================
// SecureJobLab: Centralized AJAX API Engine (5 AppSec Labs)
// Course: 20CYS403 Web Application Security
// Character Encoding: Strict UTF-8 / UTF8MB4
// Modules: 1. SQLi, 2. XSS, 3. Command Injection, 4. Directory Traversal, 5. Clickjacking
// ====================================================================

header('Content-Type: application/json; charset=utf-8');
session_start();

$db_host = "localhost";
$db_user = "root";
$db_pass = "";
$db_name = "securejoblab";

$conn = @mysqli_connect($db_host, $db_user, $db_pass, $db_name);
if ($conn) {
    @mysqli_set_charset($conn, "utf8mb4");
    @mysqli_report(MYSQLI_REPORT_OFF);
} else {
    echo json_encode(['success' => false, 'error' => 'Database connection failed: ' . mysqli_connect_error()]);
    exit;
}

// Ensure resume directory exists
$upload_dir = __DIR__ . '/uploads/resumes';
if (!is_dir($upload_dir)) {
    @mkdir($upload_dir, 0777, true);
}

$action = $_GET['action'] ?? $_POST['action'] ?? '';

// --------------------------------------------------------------------
// 1. INSTANT JOB SEARCH & FILTER (AJAX) — Mode-aware: SQLi in Vulnerable, Parameterized in Secure
// --------------------------------------------------------------------
if ($action === 'search_jobs') {
    $keyword  = trim($_GET['keyword']  ?? $_POST['keyword']  ?? '');
    $location = trim($_GET['location'] ?? $_POST['location'] ?? '');
    $job_type = trim($_GET['job_type'] ?? $_POST['job_type'] ?? '');
    // Read security mode from session (set by index.php switcher)
    $search_mode = $_SESSION['appsec_mode'] ?? 'vulnerable';
    $search_vuln = ($search_mode !== 'secure');

    $jobs        = [];
    $exec_query  = '';
    $sqli_hit    = false;

    if ($search_vuln) {
        // ============================================================
        // INTENTIONALLY VULNERABLE TRAINING CODE — SQLi demonstration
        // Raw string interpolation — keyword directly embedded in SQL
        // ============================================================
        $kw_raw = $keyword;
        $loc_raw = $location;
        $jt_raw  = $job_type;
        $where   = ["1=1"];
        if ($kw_raw !== '')  $where[] = "(title LIKE '%$kw_raw%' OR company LIKE '%$kw_raw%' OR description LIKE '%$kw_raw%')";
        if ($loc_raw !== '') $where[] = "location LIKE '%$loc_raw%'";
        if ($jt_raw  !== '') $where[] = "job_type = '$jt_raw'";
        $exec_query = "SELECT id, title, company, location, salary, job_type, department, description, secret_notes FROM jobs WHERE " . implode(' AND ', $where) . " ORDER BY id DESC";
        $res = @mysqli_query($conn, $exec_query);
        if ($res && !is_bool($res)) {
            while ($row = mysqli_fetch_assoc($res)) { $jobs[] = $row; }
        }
        // Detect if injection altered result (more rows than a normal search would return)
        if (!empty($keyword) && count($jobs) > 3) $sqli_hit = true;
    } else {
        // ============================================================
        // SECURE IMPLEMENTATION — Parameterized prepared statement
        // ============================================================
        $parts  = [];
        $types  = '';
        $params = [];
        $base   = "SELECT id, title, company, location, salary, job_type, department, description FROM jobs WHERE 1=1";
        if ($keyword !== '')  { $base .= " AND (title LIKE ? OR company LIKE ? OR description LIKE ?)"; $kw = "%$keyword%"; $types .= 'sss'; $params[] = &$kw; $params[] = &$kw; $params[] = &$kw; }
        if ($location !== '') { $base .= " AND location LIKE ?"; $loc = "%$location%"; $types .= 's'; $params[] = &$loc; }
        if ($job_type !== '') { $base .= " AND job_type = ?"; $types .= 's'; $params[] = &$job_type; }
        $base .= " ORDER BY id DESC";
        $exec_query = "SELECT id, title, company, location, salary, job_type, department, description FROM jobs WHERE ... [PARAMETERIZED]";
        $stmt = mysqli_prepare($conn, $base);
        if ($stmt && $types !== '') {
            $bind_args = array_merge([$stmt, $types], $params);
            call_user_func_array('mysqli_stmt_bind_param', $bind_args);
            mysqli_stmt_execute($stmt);
            $res = mysqli_stmt_get_result($stmt);
            while ($row = mysqli_fetch_assoc($res)) { $jobs[] = $row; }
        } elseif ($stmt) {
            mysqli_stmt_execute($stmt);
            $res = mysqli_stmt_get_result($stmt);
            while ($row = mysqli_fetch_assoc($res)) { $jobs[] = $row; }
        }
    }

    echo json_encode([
        'success'     => true,
        'count'       => count($jobs),
        'jobs'        => $jobs,
        'mode'        => $search_vuln ? 'vulnerable' : 'secure',
        'exec_query'  => $exec_query,
        'sqli_hit'    => $sqli_hit,
        'keyword'     => $keyword,
    ]);
    exit;
}

// --------------------------------------------------------------------
// 1b. PING GATEWAY — OS Command Injection demonstration endpoint
// --------------------------------------------------------------------
if ($action === 'ping_gateway') {
    $host = trim($_POST['host'] ?? '127.0.0.1');
    $mode = $_POST['mode'] ?? $_SESSION['appsec_mode'] ?? 'vulnerable';
    $is_vuln = ($mode !== 'secure');

    if ($is_vuln) {
        // INTENTIONALLY VULNERABLE TRAINING CODE — direct shell concatenation
        $cmd    = "ping -n 1 " . $host;
        $output = @shell_exec($cmd . " 2>&1");
        echo json_encode([
            'success'  => true,
            'mode'     => 'vulnerable',
            'cmd'      => $cmd,
            'output'   => $output ?: '(no output)',
            'injected' => (strpos($host, '&') !== false || strpos($host, '|') !== false || strpos($host, ';') !== false),
        ]);
    } else {
        // SECURE IMPLEMENTATION — strict whitelist + escapeshellarg
        if (preg_match('/^[a-zA-Z0-9.\-]+$/', $host)) {
            $safe = escapeshellarg($host);
            $cmd  = "ping -n 1 " . $safe;
            $out  = @shell_exec($cmd . " 2>&1");
            echo json_encode(['success' => true, 'mode' => 'secure', 'cmd' => $cmd, 'output' => $out ?: '(no output)', 'injected' => false]);
        } else {
            echo json_encode(['success' => true, 'mode' => 'secure', 'cmd' => 'REJECTED', 'output' => 'SECURITY BLOCK: Input contains forbidden characters (&, |, ;, `, space). Only alphanumeric, dots, hyphens allowed.', 'injected' => false]);
        }
    }
    exit;
}

// --------------------------------------------------------------------
// 1c. VIEW DOCUMENT — Directory Traversal demonstration endpoint
// --------------------------------------------------------------------
if ($action === 'view_document') {
    $file = trim($_POST['file'] ?? $_GET['file'] ?? 'resume.txt');
    $mode = $_POST['mode'] ?? $_SESSION['appsec_mode'] ?? 'vulnerable';
    $is_vuln = ($mode !== 'secure');

    if ($is_vuln) {
        // INTENTIONALLY VULNERABLE TRAINING CODE — direct path concatenation
        $path = __DIR__ . '/lab_files/' . $file;
        if (file_exists($path)) {
            $content = @file_get_contents($path);
            echo json_encode([
                'success'       => true,
                'mode'          => 'vulnerable',
                'requested'     => $file,
                'resolved_path' => realpath($path) ?: $path,
                'content'       => substr($content, 0, 2000),
                'traversal_hit' => (strpos($file, '..') !== false),
            ]);
        } else {
            echo json_encode(['success' => true, 'mode' => 'vulnerable', 'requested' => $file, 'resolved_path' => $path, 'content' => '(File not found at resolved path)', 'traversal_hit' => false]);
        }
    } else {
        // SECURE IMPLEMENTATION — basename() + whitelist + realpath boundary check
        $safe_file = basename($file);
        $whitelist  = ['resume.txt', 'coverletter.txt', 'certificate.txt', 'skills.txt', 'assignment.txt'];
        $base_dir   = realpath(__DIR__ . '/lab_files');
        if (!in_array($safe_file, $whitelist, true)) {
            echo json_encode(['success' => true, 'mode' => 'secure', 'requested' => $file, 'sanitized' => $safe_file, 'content' => 'ACCESS DENIED: "' . htmlspecialchars($safe_file) . '" is not in the authorized document whitelist.', 'traversal_hit' => false]);
        } else {
            $path    = $base_dir . DIRECTORY_SEPARATOR . $safe_file;
            $content = @file_get_contents($path);
            echo json_encode(['success' => true, 'mode' => 'secure', 'requested' => $file, 'sanitized' => $safe_file, 'resolved_path' => $path, 'content' => substr($content, 0, 2000), 'traversal_hit' => false]);
        }
    }
    exit;
}

// --------------------------------------------------------------------
// 2. SUBMIT APPLICATION (AJAX with Local Resume Upload)
// --------------------------------------------------------------------
if ($action === 'apply_job') {
    $job_title = trim($_POST['job_title'] ?? '');
    $company = trim($_POST['company'] ?? '');
    $applicant_name = trim($_POST['applicant_name'] ?? 'Ram Karthik');
    $email = trim($_POST['email'] ?? 'ram.karthik@securejob.io');
    $phone = trim($_POST['phone'] ?? '+91 98765 43210');
    $experience = trim($_POST['experience'] ?? '3+ Years in AppSec');
    $cover_note = trim($_POST['cover_note'] ?? '');

    if (empty($job_title) || empty($applicant_name) || empty($email)) {
        echo json_encode(['success' => false, 'error' => 'Job title, applicant name, and email are required.']);
        exit;
    }

    $resume_path = 'lab_files/resume.txt';
    if (isset($_FILES['resume_file']) && $_FILES['resume_file']['error'] === UPLOAD_ERR_OK) {
        $orig_name = basename($_FILES['resume_file']['name']);
        $clean_name = time() . '_' . preg_replace('/[^a-zA-Z0-9._-]/', '', $orig_name);
        $dest = $upload_dir . '/' . $clean_name;
        if (move_uploaded_file($_FILES['resume_file']['tmp_name'], $dest)) {
            $resume_path = 'uploads/resumes/' . $clean_name;
        }
    }

    $stmt = mysqli_prepare($conn, "INSERT INTO applications (job_title, company, applicant_name, email, phone, experience, cover_note, resume_file, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Under Review')");
    mysqli_stmt_bind_param($stmt, "ssssssss", $job_title, $company, $applicant_name, $email, $phone, $experience, $cover_note, $resume_path);
    
    if (mysqli_stmt_execute($stmt)) {
        $new_id = mysqli_insert_id($conn);
        echo json_encode([
            'success' => true,
            'message' => 'Application submitted successfully for ' . $job_title . '!',
            'app_id' => $new_id,
            'resume_file' => $resume_path
        ]);
    } else {
        echo json_encode(['success' => false, 'error' => 'Failed to save application: ' . mysqli_error($conn)]);
    }
    exit;
}

// --------------------------------------------------------------------
// 3. JOB POST CRUD (AJAX)
// --------------------------------------------------------------------
if ($action === 'add_job') {
    $title = trim($_POST['title'] ?? '');
    $company = trim($_POST['company'] ?? '');
    $location = trim($_POST['location'] ?? 'Bangalore / Hybrid');
    $salary = trim($_POST['salary'] ?? '₹24,00,000 / yr');
    $job_type = trim($_POST['job_type'] ?? 'Full-time');
    $department = trim($_POST['department'] ?? 'Engineering');
    $description = trim($_POST['description'] ?? '');
    $secret_notes = trim($_POST['secret_notes'] ?? 'CONFIDENTIAL: Standard compensation band.');

    if (empty($title) || empty($company)) {
        echo json_encode(['success' => false, 'error' => 'Job title and company name are required.']);
        exit;
    }

    $stmt = mysqli_prepare($conn, "INSERT INTO jobs (title, company, location, salary, job_type, department, description, secret_notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
    mysqli_stmt_bind_param($stmt, "ssssssss", $title, $company, $location, $salary, $job_type, $department, $description, $secret_notes);

    if (mysqli_stmt_execute($stmt)) {
        echo json_encode(['success' => true, 'message' => 'Job posted successfully!', 'job_id' => mysqli_insert_id($conn)]);
    } else {
        echo json_encode(['success' => false, 'error' => mysqli_error($conn)]);
    }
    exit;
}

if ($action === 'edit_job') {
    $id = intval($_POST['id'] ?? 0);
    $title = trim($_POST['title'] ?? '');
    $company = trim($_POST['company'] ?? '');
    $location = trim($_POST['location'] ?? '');
    $salary = trim($_POST['salary'] ?? '');
    $job_type = trim($_POST['job_type'] ?? 'Full-time');
    $department = trim($_POST['department'] ?? 'Engineering');
    $description = trim($_POST['description'] ?? '');
    $secret_notes = trim($_POST['secret_notes'] ?? '');

    if ($id <= 0 || empty($title) || empty($company)) {
        echo json_encode(['success' => false, 'error' => 'Invalid job data.']);
        exit;
    }

    $stmt = mysqli_prepare($conn, "UPDATE jobs SET title = ?, company = ?, location = ?, salary = ?, job_type = ?, department = ?, description = ?, secret_notes = ? WHERE id = ?");
    mysqli_stmt_bind_param($stmt, "ssssssssi", $title, $company, $location, $salary, $job_type, $department, $description, $secret_notes, $id);

    if (mysqli_stmt_execute($stmt)) {
        echo json_encode(['success' => true, 'message' => 'Job updated successfully!']);
    } else {
        echo json_encode(['success' => false, 'error' => mysqli_error($conn)]);
    }
    exit;
}

if ($action === 'delete_job') {
    $id = intval($_POST['id'] ?? 0);
    if ($id <= 0) {
        echo json_encode(['success' => false, 'error' => 'Invalid job ID.']);
        exit;
    }

    $stmt = mysqli_prepare($conn, "DELETE FROM jobs WHERE id = ?");
    mysqli_stmt_bind_param($stmt, "i", $id);
    if (mysqli_stmt_execute($stmt)) {
        echo json_encode(['success' => true, 'message' => 'Job listing deleted successfully!']);
    } else {
        echo json_encode(['success' => false, 'error' => mysqli_error($conn)]);
    }
    exit;
}

if ($action === 'withdraw_app') {
    $id = intval($_POST['id'] ?? 0);
    if ($id <= 0) {
        echo json_encode(['success' => false, 'error' => 'Invalid application ID.']);
        exit;
    }

    $stmt = mysqli_prepare($conn, "DELETE FROM applications WHERE id = ?");
    mysqli_stmt_bind_param($stmt, "i", $id);
    if (mysqli_stmt_execute($stmt)) {
        echo json_encode(['success' => true, 'message' => 'Application withdrawn successfully!']);
    } else {
        echo json_encode(['success' => false, 'error' => mysqli_error($conn)]);
    }
    exit;
}

// --------------------------------------------------------------------
// 4. THE 5 CORE APPSEC TESTING LABS (AJAX)
// --------------------------------------------------------------------
if ($action === 'test_lab') {
    $vuln_id = intval($_POST['vuln_id'] ?? 1);
    $mode = $_POST['mode'] ?? 'vulnerable';
    $is_vuln = ($mode === 'vulnerable');
    $payload = $_POST['payload'] ?? '';

    // ================================================================
    // MODULE 1: SQL INJECTION (CWE-89)
    // ================================================================
    if ($vuln_id === 1) {
        if ($is_vuln) {
            $query = "SELECT id, title, company, salary, secret_notes FROM jobs WHERE title = '$payload'";
            try {
                $res = @mysqli_query($conn, $query);
                $rows = [];
                if ($res && !is_bool($res)) {
                    while ($r = mysqli_fetch_assoc($res)) {
                        $rows[] = $r;
                    }
                    echo json_encode([
                        'success' => true,
                        'vuln_id' => 1,
                        'vuln_name' => 'SQL Injection (SQLi)',
                        'cwe' => 'CWE-89',
                        'mode' => 'vulnerable',
                        'executed_query' => $query,
                        'rows_returned' => count($rows),
                        'results' => $rows,
                        'status_type' => count($rows) > 1 ? 'danger' : 'warning',
                        'exploit_status' => count($rows) > 1 ? 'EXPLOIT SUCCESSFUL: Authentication/query bypassed. Confidential internal notes and salary bands extracted.' : 'Single query executed.',
                        'defense_info' => 'Vulnerable string concatenation detected: Direct variable interpolation allows breaking query structure.'
                    ]);
                } else {
                    echo json_encode([
                        'success' => true,
                        'vuln_id' => 1,
                        'vuln_name' => 'SQL Injection (SQLi)',
                        'cwe' => 'CWE-89',
                        'mode' => 'vulnerable',
                        'executed_query' => $query,
                        'error_message' => mysqli_error($conn) ?: 'Syntax error or zero rows returned.',
                        'status_type' => 'danger',
                        'exploit_status' => 'SQL SYNTAX TRIGGERED: Malformed injection broke SQL grammar (Error-based SQLi indicator).',
                        'defense_info' => 'Unsanitized input broke the database parser directly.'
                    ]);
                }
            } catch (Exception $e) {
                echo json_encode([
                    'success' => true,
                    'vuln_id' => 1,
                    'vuln_name' => 'SQL Injection (SQLi)',
                    'cwe' => 'CWE-89',
                    'mode' => 'vulnerable',
                    'executed_query' => $query,
                    'error_message' => $e->getMessage(),
                    'status_type' => 'danger',
                    'exploit_status' => 'SQL EXCEPTION: Dynamic query failed safely in exception handler.',
                    'defense_info' => 'Unparameterized query execution threw an unhandled database exception.'
                ]);
            }
        } else {
            // SECURE MITIGATION: Prepared Statements with Parameter Binding
            $stmt = mysqli_prepare($conn, "SELECT id, title, company, salary, secret_notes FROM jobs WHERE title = ?");
            if ($stmt) {
                mysqli_stmt_bind_param($stmt, "s", $payload);
                mysqli_stmt_execute($stmt);
                $res = mysqli_stmt_get_result($stmt);
                $rows = [];
                while ($r = mysqli_fetch_assoc($res)) {
                    $rows[] = $r;
                }
                echo json_encode([
                    'success' => true,
                    'vuln_id' => 1,
                    'vuln_name' => 'SQL Injection (SQLi)',
                    'cwe' => 'CWE-89',
                    'mode' => 'secure',
                    'executed_query' => 'SELECT id, title, company, salary, secret_notes FROM jobs WHERE title = ?',
                    'bound_parameter' => $payload,
                    'rows_returned' => count($rows),
                    'results' => $rows,
                    'status_type' => 'success',
                    'exploit_status' => 'DEFENSE VERIFIED: Prepared statement compiled query structure separately. Payload treated strictly as literal string.',
                    'defense_info' => 'Parameterized prepared statements (mysqli_prepare + mysqli_stmt_bind_param) completely neutralize injection.'
                ]);
            }
        }
        exit;
    }

    // ================================================================
    // MODULE 2: CROSS-SITE SCRIPTING (XSS) (CWE-79)
    // ================================================================
    if ($vuln_id === 2) {
        $input = empty($payload) ? "<script>alert('XSS: ' + document.domain)</script>" : $payload;
        if ($is_vuln) {
            // VULNERABLE: Direct raw reflection without encoding
            echo json_encode([
                'success' => true,
                'vuln_id' => 2,
                'vuln_name' => 'Cross-Site Scripting (XSS)',
                'cwe' => 'CWE-79',
                'mode' => 'vulnerable',
                'raw_payload' => $input,
                'rendered_html' => $input,
                'status_type' => 'danger',
                'exploit_status' => 'EXPLOIT SUCCESSFUL: Unsanitized script tags rendered directly into browser DOM. Arbitrary JavaScript executes.',
                'defense_info' => 'Vulnerable: Output reflected directly into DOM without HTML entity encoding, allowing cookie theft and DOM hijacking.'
            ]);
        } else {
            // SECURE MITIGATION: HTML contextual entity encoding
            $safe = htmlspecialchars($input, ENT_QUOTES, 'UTF-8');
            echo json_encode([
                'success' => true,
                'vuln_id' => 2,
                'vuln_name' => 'Cross-Site Scripting (XSS)',
                'cwe' => 'CWE-79',
                'mode' => 'secure',
                'raw_payload' => $input,
                'rendered_html' => $safe,
                'status_type' => 'success',
                'exploit_status' => 'DEFENSE VERIFIED: Input encoded with htmlspecialchars(). Browser renders HTML tags safely as plain text.',
                'defense_info' => 'htmlspecialchars($input, ENT_QUOTES, "UTF-8") converts special characters (&, <, >, ", \') into harmless HTML entities.'
            ]);
        }
        exit;
    }

    // ================================================================
    // MODULE 3: OS COMMAND INJECTION (CWE-78)
    // ================================================================
    if ($vuln_id === 3) {
        $host = empty($payload) ? '127.0.0.1 & whoami' : $payload;
        if ($is_vuln) {
            // VULNERABLE: Direct concatenation into shell_exec
            $cmd = "ping -n 1 " . $host;
            $output = @shell_exec($cmd . " 2>&1");
            echo json_encode([
                'success' => true,
                'vuln_id' => 3,
                'vuln_name' => 'OS Command Injection',
                'cwe' => 'CWE-78',
                'mode' => 'vulnerable',
                'command_executed' => $cmd,
                'output' => $output ?: '(No output returned or command blocked by system policy)',
                'status_type' => 'danger',
                'exploit_status' => 'EXPLOIT SUCCESSFUL: Arbitrary OS command executed on server host via shell command delimiter (&, |, ;).',
                'defense_info' => 'Direct concatenation into shell_exec() permits command chaining and full host takeover.'
            ]);
        } else {
            // SECURE MITIGATION: Strict regex whitelist & escapeshellarg
            if (preg_match('/^[a-zA-Z0-9.-]+$/', $host)) {
                $clean_host = escapeshellarg($host);
                $cmd = "ping -n 1 " . $clean_host;
                $output = @shell_exec($cmd . " 2>&1");
                echo json_encode([
                    'success' => true,
                    'vuln_id' => 3,
                    'vuln_name' => 'OS Command Injection',
                    'cwe' => 'CWE-78',
                    'mode' => 'secure',
                    'command_executed' => $cmd,
                    'output' => $output,
                    'status_type' => 'success',
                    'exploit_status' => 'DEFENSE VERIFIED: Input validated against strict hostname/IP whitelist and escaped safely.',
                    'defense_info' => 'Input whitelist validation + escapeshellarg() prevents command separator injection.'
                ]);
            } else {
                echo json_encode([
                    'success' => true,
                    'vuln_id' => 3,
                    'vuln_name' => 'OS Command Injection',
                    'cwe' => 'CWE-78',
                    'mode' => 'secure',
                    'command_executed' => 'REJECTED: Contains forbidden characters (&, |, ;, `)',
                    'output' => 'SECURITY INTERCEPTION: Injected command delimiters detected and rejected before reaching OS shell.',
                    'status_type' => 'success',
                    'exploit_status' => 'DEFENSE BLOCKED: Injected command delimiters (&, |, ;, `) rejected by strict regex whitelist.',
                    'defense_info' => 'Whitelist validation rejected input before system call was initiated.'
                ]);
            }
        }
        exit;
    }

    // ================================================================
    // MODULE 4: DIRECTORY / PATH TRAVERSAL (CWE-22)
    // ================================================================
    if ($vuln_id === 4) {
        $file = empty($payload) ? '../credentials.txt' : $payload;
        if ($is_vuln) {
            // VULNERABLE: Direct relative path concatenation
            $path = __DIR__ . '/lab_files/' . $file;
            if (file_exists($path)) {
                $content = @file_get_contents($path);
                echo json_encode([
                    'success' => true,
                    'vuln_id' => 4,
                    'vuln_name' => 'Directory / Path Traversal',
                    'cwe' => 'CWE-22',
                    'mode' => 'vulnerable',
                    'requested_file' => $file,
                    'resolved_path' => realpath($path) ?: $path,
                    'content' => substr($content, 0, 1500),
                    'status_type' => 'danger',
                    'exploit_status' => (strpos($file, '..') !== false) ? 'EXPLOIT SUCCESSFUL: Directory escaping (../) bypassed folder isolation to read sensitive server credentials.' : 'Document loaded successfully.',
                    'defense_info' => 'Relative path traversal permitted without path resolution bounds.'
                ]);
            } else {
                echo json_encode([
                    'success' => true,
                    'vuln_id' => 4,
                    'vuln_name' => 'Directory / Path Traversal',
                    'cwe' => 'CWE-22',
                    'mode' => 'vulnerable',
                    'requested_file' => $file,
                    'resolved_path' => $path,
                    'content' => 'Target file not found at path: ' . $path,
                    'status_type' => 'warning',
                    'exploit_status' => 'TRAVERSAL ATTEMPTED: Target resolved to ' . $path,
                    'defense_info' => 'Relative path traversal permitted without path resolution bounds.'
                ]);
            }
        } else {
            // SECURE MITIGATION: basename() + strict whitelist
            $safe_file = basename($file);
            $whitelist = ['resume.txt', 'secret_flag.txt', 'assignment.txt', 'coverletter.txt', 'certificate.txt', 'skills.txt'];
            if (in_array($safe_file, $whitelist, true)) {
                $path = __DIR__ . '/lab_files/' . $safe_file;
                $content = @file_get_contents($path);
                echo json_encode([
                    'success' => true,
                    'vuln_id' => 4,
                    'vuln_name' => 'Directory / Path Traversal',
                    'cwe' => 'CWE-22',
                    'mode' => 'secure',
                    'requested_file' => $file,
                    'sanitized_file' => $safe_file,
                    'resolved_path' => realpath($path),
                    'content' => substr($content, 0, 1500),
                    'status_type' => 'success',
                    'exploit_status' => 'DEFENSE VERIFIED: Traversal tokens (../) stripped by basename(). Only authorized files read.',
                    'defense_info' => 'basename() filename extraction + strict whitelist array guarantees sandbox confinement.'
                ]);
            } else {
                echo json_encode([
                    'success' => true,
                    'vuln_id' => 4,
                    'vuln_name' => 'Directory / Path Traversal',
                    'cwe' => 'CWE-22',
                    'mode' => 'secure',
                    'requested_file' => $file,
                    'sanitized_file' => $safe_file,
                    'content' => 'ACCESS DENIED: The requested file is not in the authorized document whitelist.',
                    'status_type' => 'success',
                    'exploit_status' => 'DEFENSE BLOCKED: Traversal tokens (../) stripped by basename() and unauthorized file rejected by whitelist.',
                    'defense_info' => 'basename() + strict whitelist ensures path never escapes designated storage directory.'
                ]);
            }
        }
        exit;
    }

    // ================================================================
    // MODULE 5: CLICKJACKING (UI REDRESSING) (CWE-1021)
    // ================================================================
    if ($vuln_id === 5) {
        $frame_url = "clickjack_target.php?mode=" . ($is_vuln ? 'vulnerable' : 'secure');
        echo json_encode([
            'success' => true,
            'vuln_id' => 5,
            'vuln_name' => 'Clickjacking (UI Redressing)',
            'cwe' => 'CWE-1021',
            'mode' => $is_vuln ? 'vulnerable' : 'secure',
            'frame_url' => $frame_url,
            'headers_applied' => $is_vuln ? 'None (Framing Allowed)' : 'X-Frame-Options: DENY, Content-Security-Policy: frame-ancestors none',
            'status_type' => $is_vuln ? 'danger' : 'success',
            'exploit_status' => $is_vuln ? 'EXPLOIT SUCCESSFUL: Target page framed without restrictions. Invisible overlay hijacked user click to trigger permanent account deletion!' : 'DEFENSE VERIFIED: Browser refuses to render framed document due to X-Frame-Options: DENY.',
            'defense_info' => $is_vuln ? 'Missing X-Frame-Options and CSP headers permits third-party framing, enabling attackers to trick victims into triggering destructive actions.' : 'X-Frame-Options: DENY and CSP frame-ancestors "none" instructs modern browsers to reject all iframe embedding.'
        ]);
        exit;
    }
}

// --------------------------------------------------------------------
// 5. DATABASE RE-SEED (AJAX)
// --------------------------------------------------------------------
if ($action === 'reseed_db') {
    mysqli_query($conn, "SET FOREIGN_KEY_CHECKS = 0");
    mysqli_query($conn, "TRUNCATE TABLE applications");
    mysqli_query($conn, "TRUNCATE TABLE jobs");
    mysqli_query($conn, "TRUNCATE TABLE feedback");
    mysqli_query($conn, "SET FOREIGN_KEY_CHECKS = 1");

    mysqli_query($conn, "INSERT INTO jobs (title, company, location, salary, job_type, department, description, secret_notes) VALUES 
        ('Senior Cybersecurity Engineer', 'Amazon Web Services (AWS)', 'Bangalore / Hybrid', '₹28,00,000 / yr', 'Full-time', 'Information Security', 'Architect automated application security scanning, threat modeling, and defensive frameworks for cloud native services.', 'CONFIDENTIAL: Salary band max ₹32 LPA. Clearance Level 3.'),
        ('Application Security Specialist', 'Stripe Payments', 'Bangalore / Remote', '₹24,00,000 / yr', 'Full-time', 'Product Security', 'Identify vulnerabilities across high-throughput financial APIs, perform manual code review, and build defensive tooling.', 'CONFIDENTIAL: Sign-on equity grant 1,200 RSUs approved.'),
        ('Cloud Security Operations Analyst', 'Microsoft India', 'Hyderabad', '₹20,00,000 / yr', 'Full-time', 'Cloud Operations', 'Monitor cloud security telemetry, investigate SIEM alerts, and execute incident response runbooks.', 'CONFIDENTIAL: Shift rotation bonus ₹30,000/month.'),
        ('Full Stack Security Engineer', 'Razorpay', 'Bangalore / Onsite', '₹22,00,000 / yr', 'Full-time', 'FinTech Security', 'Develop resilient web services, integrate SAST/DAST pipelines, and audit authentication and payment gateway workflows.', 'CONFIDENTIAL: Candidate shortlisted for final interview round.'),
        ('DevSecOps Automation Engineer', 'CRED Tech', 'Bangalore / Remote', '₹26,00,000 / yr', 'Full-time', 'Infrastructure', 'Build zero-trust CI/CD deployment gates, secure Kubernetes container runtime, and automate vulnerability remediation.', 'CONFIDENTIAL: Budget flexibility up to ₹29 LPA.')");

    mysqli_query($conn, "INSERT INTO applications (job_title, company, applicant_name, email, phone, experience, cover_note, resume_file, status) VALUES 
        ('Senior Cybersecurity Engineer', 'Amazon Web Services (AWS)', 'Ram Karthik', 'ram.karthik@securejob.io', '+91 98765 43210', '3+ Years in AppSec', 'Passionate about defensive web architectures and cloud security.', 'lab_files/resume.txt', 'Interview Scheduled'),
        ('Application Security Specialist', 'Stripe Payments', 'Ram Karthik', 'ram.karthik@securejob.io', '+91 98765 43210', '3+ Years in AppSec', 'Extensive experience auditing web APIs and implementing OWASP defenses.', 'lab_files/resume.txt', 'Under Review')");

    mysqli_query($conn, "INSERT INTO feedback (author, comment) VALUES 
        ('Tech Recruiter (AWS)', 'Ram Karthik demonstrated outstanding technical depth in secure code review and cloud architecture defense.'),
        ('Lead Security Architect (Stripe)', 'Solid understanding of OWASP Top 10 vulnerabilities, parameterization, and cryptographic session protection.')");

    echo json_encode([
        'success' => true,
        'message' => 'Database successfully re-seeded with pristine demonstration records for Ram Karthik!'
    ]);
    exit;
}

echo json_encode(['success' => false, 'error' => 'Invalid action parameter.']);
exit;
