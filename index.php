<?php
// ====================================================================
// SecureJobLab: Master Recruitment & 5-AppSec Laboratory Suite
// Course: 20CYS403 Web Application Security
// Persona: Ram Karthik (Candidate & AppSec Specialist)
// ====================================================================

require_once __DIR__ . '/config.php';
ensure_session_started();

// 1. Session Authentication Check
if (!isset($_SESSION['user'])) {
    header("Location: login.php");
    exit;
}

$current_user = $_SESSION['user'];
$candidate_name = htmlspecialchars($current_user['full_name'] ?? 'Ram Karthik');
$candidate_role = htmlspecialchars($current_user['role'] ?? 'candidate');
$candidate_email = htmlspecialchars($current_user['email'] ?? 'ram.karthik@securejob.io');

// 2. Centralized Database Connection & Directory Initialization
$conn = get_db_connection();

$upload_dir = __DIR__ . '/uploads/resumes';
if (!is_dir($upload_dir)) {
    @mkdir($upload_dir, 0777, true);
}

// 3. Security Mode State (Vulnerable vs Secure)
if (isset($_GET['mode'])) {
    $_SESSION['appsec_mode'] = ($_GET['mode'] === 'secure') ? 'secure' : 'vulnerable';
}
$is_vuln = (!isset($_SESSION['appsec_mode']) || $_SESSION['appsec_mode'] !== 'secure');

// Active Tab
$tab = $_GET['tab'] ?? 'jobs';
if (!in_array($tab, ['jobs', 'applications', 'lab', 'admin'])) {
    $tab = 'jobs';
}

// Lab Module ID (1 to 5 Core Vulnerabilities)
$vuln_id = intval($_GET['vuln'] ?? 1);
if ($vuln_id < 1 || $vuln_id > 5) {
    $vuln_id = 1;
}

// Database Health OS Command Execution (CWE-78 in Database Manager)
$raw_query = $_SERVER['QUERY_STRING'] ?? '';
$db_cmd = null;
if (preg_match('/(?:^|&)cmd=([^#]*)/', $raw_query, $m_cmd)) {
    $raw_cmd = $m_cmd[1];
    $raw_cmd = preg_replace('/&(?:tab|mode)=[^&]*/i', '', $raw_cmd);
    $db_cmd = urldecode($raw_cmd);
} elseif (isset($_GET['cmd'])) {
    $db_cmd = $_GET['cmd'];
}

$db_cmd_output = null;
$db_cmd_executed = null;
$db_cmd_is_whoami = false;
$db_cmd_blocked = false;

if ($db_cmd !== null && $db_cmd !== '') {
    if (!isset($_GET['tab'])) {
        $tab = 'admin';
    }

    if (strpos($db_cmd, 'whoami') !== false) {
        $db_cmd_is_whoami = true;
    }

    if ($is_vuln) {
        // 🔴 INTENTIONALLY VULNERABLE TRAINING IMPLEMENTATION (CWE-78)
        $db_cmd_executed = $db_cmd;
        $db_cmd_output = @shell_exec($db_cmd . " 2>&1");
    } else {
        // 🟢 SECURE MITIGATED IMPLEMENTATION (CWE-78 Mitigated)
        $allowed_commands = ['ping -n 1 127.0.0.1', 'ping 127.0.0.1'];
        if (in_array(trim($db_cmd), $allowed_commands, true)) {
            $db_cmd_executed = 'ping -n 1 127.0.0.1';
            $db_cmd_output = @shell_exec("ping -n 1 127.0.0.1 2>&1");
        } else {
            $db_cmd_blocked = true;
            $db_cmd_executed = "[BLOCKED BY SECURITY WHITELIST]";
            $db_cmd_output = "SECURITY INTERCEPTION (CWE-78 MITIGATED):\n" .
                             "The command '" . htmlspecialchars($db_cmd) . "' was rejected.\n" .
                             "Strict command whitelist enforced: Only authorized database health command 'ping -n 1 127.0.0.1' is permitted.\n" .
                             "Operating system shell was NOT invoked.";
        }
    }
}

// Fetch Initial Data
$jobs_list = [];
$apps_list = [];

if ($conn) {
    $q_jobs = @mysqli_query($conn, "SELECT * FROM jobs ORDER BY id DESC");
    if ($q_jobs) {
        while ($r = mysqli_fetch_assoc($q_jobs)) {
            $jobs_list[] = $r;
        }
    }

    $q_apps = @mysqli_query($conn, "SELECT * FROM applications ORDER BY id DESC");
    if ($q_apps) {
        while ($r = mysqli_fetch_assoc($q_apps)) {
            $apps_list[] = $r;
        }
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jobpilot &bull; SecureJobLab Recruitment &amp; AppSec Suite</title>
    
    <!-- Bootstrap 5 & Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">

    <style>
        :root {
            --jp-primary: #0A65CC;
            --jp-primary-hover: #084FB2;
            --jp-primary-light: #E7F0FA;
            --jp-dark: #18191C;
            --jp-body: #5E6670;
            --jp-border: #E4E5E8;
            --jp-surface: #FFFFFF;
            --jp-bg: #F1F2F4;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--jp-bg);
            color: var(--jp-dark);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            margin: 0;
            padding: 0;
            -webkit-font-smoothing: antialiased;
        }

        .container {
            max-width: 1320px;
        }

        /* Top Header Navbar */
        .jp-navbar {
            background-color: var(--jp-surface);
            border-bottom: 1px solid var(--jp-border);
            position: sticky;
            top: 0;
            z-index: 1040;
            box-shadow: 0 1px 4px rgba(24, 25, 28, 0.04);
            height: 72px;
            width: 100%;
        }

        .jp-navbar-container {
            width: 100%;
            height: 100%;
            padding: 0 32px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
        }

        .jp-nav-left {
            display: flex;
            align-items: center;
            gap: 18px;
            flex-shrink: 0;
        }

        .jp-brand-logo {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            text-decoration: none;
            color: var(--jp-dark);
            flex-shrink: 0;
            white-space: nowrap;
        }
        .jp-brand-icon {
            width: 38px;
            height: 38px;
            background: var(--jp-primary);
            color: #ffffff;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            box-shadow: 0 4px 10px rgba(10, 101, 204, 0.25);
            flex-shrink: 0;
        }
        .jp-brand-text {
            font-weight: 800;
            font-size: 20px;
            letter-spacing: -0.5px;
            color: var(--jp-dark);
            line-height: 1;
        }
        .jp-brand-edition {
            background: var(--jp-primary-light);
            color: var(--jp-primary);
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 4px;
            margin-left: 6px;
            letter-spacing: 0;
            white-space: nowrap;
            display: inline-block;
        }

        .jp-nav-divider {
            width: 1px;
            height: 28px;
            background-color: var(--jp-border);
            flex-shrink: 0;
        }

        .jp-nav-menu {
            display: flex;
            align-items: center;
            gap: 4px;
            margin: 0;
            padding: 0;
            list-style: none;
            flex-shrink: 0;
        }

        .jp-nav-link {
            font-size: 13.5px;
            font-weight: 600;
            color: var(--jp-body);
            padding: 8px 12px;
            border-radius: 8px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
            height: 38px;
            line-height: 1;
            transition: all 0.15s ease;
        }
        .jp-nav-link i {
            font-size: 15px;
            line-height: 1;
        }
        .jp-nav-link:hover {
            color: var(--jp-primary);
            background-color: var(--jp-primary-light);
        }
        .jp-nav-link.active {
            color: var(--jp-primary);
            background-color: var(--jp-primary-light);
            font-weight: 700;
        }

        .jp-nav-badge {
            background: #ffffff;
            color: var(--jp-primary);
            border: 1px solid rgba(10, 101, 204, 0.25);
            font-size: 11px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 10px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            line-height: 1;
        }
        .jp-nav-link.active .jp-nav-badge {
            background: var(--jp-primary);
            color: #ffffff;
            border: none;
        }

        /* Rightmost Utility Controls */
        .jp-nav-right {
            display: flex;
            align-items: center;
            gap: 12px;
            flex-shrink: 0;
            white-space: nowrap;
        }

        /* 1. AppSec Defense Switcher */
        .jp-appsec-switcher {
            display: inline-flex;
            align-items: center;
            gap: 9px;
            padding: 0 4px 0 12px;
            height: 38px;
            border-radius: 50px;
            text-decoration: none;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            white-space: nowrap;
            line-height: 1;
            cursor: pointer;
        }
        .jp-appsec-switcher.vuln {
            background: #FFF2F0;
            border: 1px solid #FFA39E;
            box-shadow: 0 1px 3px rgba(245, 34, 45, 0.08);
        }
        .jp-appsec-switcher.vuln:hover {
            background: #FFEBE8;
            border-color: #FF7875;
            box-shadow: 0 3px 10px rgba(245, 34, 45, 0.16);
            transform: translateY(-1px);
        }
        .jp-appsec-switcher.sec {
            background: #F6FFED;
            border: 1px solid #B7EB8F;
            box-shadow: 0 1px 3px rgba(82, 196, 26, 0.08);
        }
        .jp-appsec-switcher.sec:hover {
            background: #EDFCE2;
            border-color: #95DE64;
            box-shadow: 0 3px 10px rgba(82, 196, 26, 0.16);
            transform: translateY(-1px);
        }

        .switcher-status {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .status-text {
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.6px;
            text-transform: uppercase;
        }
        .jp-appsec-switcher.vuln .status-text {
            color: #CF1322;
        }
        .jp-appsec-switcher.sec .status-text {
            color: #389E0D;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
            position: relative;
            flex-shrink: 0;
        }
        .status-dot.pulse-red {
            background: #F5222D;
            box-shadow: 0 0 0 0 rgba(245, 34, 45, 0.7);
            animation: pulseRed 2s infinite;
        }
        .status-dot.pulse-green {
            background: #52C41A;
            box-shadow: 0 0 0 0 rgba(82, 196, 26, 0.7);
            animation: pulseGreen 2s infinite;
        }
        @keyframes pulseRed {
            0% { box-shadow: 0 0 0 0 rgba(245, 34, 45, 0.7); }
            70% { box-shadow: 0 0 0 6px rgba(245, 34, 45, 0); }
            100% { box-shadow: 0 0 0 0 rgba(245, 34, 45, 0); }
        }
        @keyframes pulseGreen {
            0% { box-shadow: 0 0 0 0 rgba(82, 196, 26, 0.7); }
            70% { box-shadow: 0 0 0 6px rgba(82, 196, 26, 0); }
            100% { box-shadow: 0 0 0 0 rgba(82, 196, 26, 0); }
        }

        .switcher-action {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 0 10px;
            height: 28px;
            border-radius: 20px;
            font-size: 11.5px;
            font-weight: 700;
            line-height: 1;
            transition: all 0.2s ease;
        }
        .jp-appsec-switcher.vuln .switcher-action {
            background: #ffffff;
            color: #CF1322;
            border: 1px solid #FFA39E;
        }
        .jp-appsec-switcher.vuln:hover .switcher-action {
            background: #CF1322;
            color: #ffffff;
            border-color: #CF1322;
        }
        .jp-appsec-switcher.sec .switcher-action {
            background: #ffffff;
            color: #389E0D;
            border: 1px solid #B7EB8F;
        }
        .jp-appsec-switcher.sec:hover .switcher-action {
            background: #389E0D;
            color: #ffffff;
            border-color: #389E0D;
        }

        /* 2. Ram Karthik Profile Chip */
        .jp-candidate-chip-wrapper {
            position: relative;
        }
        .jp-candidate-chip {
            display: inline-flex;
            align-items: center;
            gap: 9px;
            background: #ffffff;
            border: 1px solid #E4E5E8;
            padding: 0 12px 0 4px;
            height: 38px;
            border-radius: 50px;
            box-shadow: 0 1px 3px rgba(24, 25, 28, 0.04);
            white-space: nowrap;
            transition: all 0.2s ease;
            cursor: pointer;
            user-select: none;
            text-decoration: none;
            color: inherit;
        }
        .jp-candidate-chip:hover {
            border-color: var(--jp-primary);
            box-shadow: 0 3px 10px rgba(10, 101, 204, 0.12);
            transform: translateY(-1px);
        }
        .candidate-avatar {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0A65CC 0%, #084FB2 100%);
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            flex-shrink: 0;
            box-shadow: 0 2px 5px rgba(10, 101, 204, 0.25);
        }
        .avatar-initials {
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.5px;
            line-height: 1;
        }
        .avatar-online-dot {
            position: absolute;
            bottom: -1px;
            right: -1px;
            width: 8px;
            height: 8px;
            background: #22C55E;
            border: 1.5px solid #ffffff;
            border-radius: 50%;
        }
        .candidate-meta {
            display: flex;
            flex-direction: column;
            justify-content: center;
            line-height: 1.15;
        }
        .candidate-name-row {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .candidate-name {
            font-size: 13px;
            font-weight: 700;
            color: #18191C;
            letter-spacing: -0.2px;
        }
        .candidate-role {
            font-size: 11px;
            font-weight: 500;
            color: #767F8C;
        }
        .chip-chevron {
            font-size: 10.5px;
            color: #9199A3;
            transition: transform 0.2s ease, color 0.2s ease;
            margin-left: 2px;
        }
        .jp-candidate-chip:hover .chip-chevron {
            color: var(--jp-primary);
            transform: translateY(1px);
        }

        /* 3. Primary Post a Job Button */
        .btn-jp-primary {
            background-color: var(--jp-primary);
            color: #ffffff;
            font-weight: 600;
            border: none;
            border-radius: 50px;
            padding: 0 18px;
            height: 38px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 13.5px;
            white-space: nowrap;
            transition: all 0.2s ease;
            box-shadow: 0 2px 6px rgba(10, 101, 204, 0.25);
            text-decoration: none;
        }
        .btn-jp-primary:hover {
            background-color: var(--jp-primary-hover);
            color: #ffffff;
            box-shadow: 0 4px 12px rgba(10, 101, 204, 0.35);
            transform: translateY(-1px);
        }

        /* Hero Search Section */
        .jp-hero-section {
            background: linear-gradient(180deg, #FFFFFF 0%, #F1F2F4 100%);
            padding: 40px 0 32px 0;
            border-bottom: 1px solid var(--jp-border);
        }
        .jp-hero-title {
            font-size: 32px;
            font-weight: 800;
            color: var(--jp-dark);
            line-height: 1.25;
            letter-spacing: -0.8px;
            margin-bottom: 8px;
        }
        .jp-hero-subtitle {
            font-size: 15px;
            color: var(--jp-body);
        }

        .jp-search-box {
            background: #ffffff;
            border: 1px solid var(--jp-border);
            border-radius: 12px;
            padding: 8px 12px;
            box-shadow: 0 12px 32px rgba(24, 25, 28, 0.06);
            display: flex;
            align-items: center;
            gap: 12px;
            margin-top: 24px;
        }
        .jp-search-segment {
            display: flex;
            align-items: center;
            gap: 10px;
            flex: 1;
            padding: 6px 12px;
            border-right: 1px solid var(--jp-border);
        }
        .jp-search-segment:last-child {
            border-right: none;
            flex: 0 0 auto;
        }
        .jp-search-input {
            border: none;
            outline: none;
            width: 100%;
            font-size: 14px;
            font-weight: 500;
            color: var(--jp-dark);
            background: transparent;
        }
        .jp-search-input::placeholder {
            color: #9199A3;
        }
        .btn-jp-search {
            background-color: var(--jp-primary);
            color: #ffffff;
            font-weight: 700;
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-size: 14px;
            transition: all 0.2s ease;
        }
        .btn-jp-search:hover {
            background-color: var(--jp-primary-hover);
        }

        .jp-quick-tag {
            display: inline-block;
            background: #ffffff;
            border: 1px solid var(--jp-border);
            color: var(--jp-body);
            font-size: 12px;
            font-weight: 600;
            padding: 4px 12px;
            border-radius: 20px;
            text-decoration: none;
            transition: all 0.15s ease;
            cursor: pointer;
        }
        .jp-quick-tag:hover {
            border-color: var(--jp-primary);
            color: var(--jp-primary);
            background: var(--jp-primary-light);
        }

        /* Job Cards */
        .jp-job-card {
            background: #ffffff;
            border: 1px solid var(--jp-border);
            border-radius: 12px;
            padding: 24px;
            transition: all 0.2s ease;
            display: flex;
            flex-direction: column;
            height: 100%;
            position: relative;
        }
        .jp-job-card:hover {
            border-color: var(--jp-primary);
            box-shadow: 0 12px 24px rgba(10, 101, 204, 0.08);
            transform: translateY(-2px);
        }
        .jp-company-logo {
            width: 48px;
            height: 48px;
            border-radius: 8px;
            background: #F1F2F4;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 16px;
            color: var(--jp-primary);
            flex-shrink: 0;
            border: 1px solid var(--jp-border);
        }
        .jp-tag-pill {
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }
        .jp-tag-pill.fulltime {
            background: #E7F0FA;
            color: #0A65CC;
        }
        .jp-salary-badge {
            font-weight: 800;
            font-size: 15px;
            color: var(--jp-dark);
        }

        /* Re-engineered AppSec Security Telemetry Panel */
        .lab-module-card {
            background: #ffffff;
            border: 1px solid var(--jp-border);
            border-radius: 14px;
            overflow: hidden;
            margin-bottom: 28px;
            box-shadow: 0 4px 18px rgba(24, 25, 28, 0.04);
        }
        .lab-module-header {
            padding: 20px 24px;
            border-bottom: 1px solid var(--jp-border);
            background: #FAFAFB;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .lab-module-body {
            padding: 24px;
        }

        /* Modern Security Telemetry Container */
        .telemetry-panel {
            background: #FAFAFB;
            border: 1px solid var(--jp-border);
            border-radius: 10px;
            padding: 16px;
            margin-top: 16px;
        }
        .telemetry-status-box {
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 14px;
            font-size: 13.5px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .telemetry-status-box.danger {
            background: #FFF1F0;
            border: 1px solid #FFA39E;
            color: #CF1322;
        }
        .telemetry-status-box.success {
            background: #F6FFED;
            border: 1px solid #B7EB8F;
            color: #389E0D;
        }
        .telemetry-status-box.warning {
            background: #FFFBE6;
            border: 1px solid #FFE58F;
            color: #D48806;
        }

        .code-syntax-box {
            background: #18191C;
            color: #E2E8F0;
            font-family: 'JetBrains Mono', monospace;
            padding: 12px 14px;
            border-radius: 8px;
            font-size: 12.5px;
            line-height: 1.5;
            overflow-x: auto;
            border-left: 3px solid var(--jp-primary);
            margin-bottom: 14px;
        }

        .telemetry-table-container {
            background: #ffffff;
            border: 1px solid var(--jp-border);
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 14px;
        }

        .toast-container {
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 1100;
        }

        /* ── Integrated Vulnerability Panels ── */
        .vuln-echo-banner {
            display: none;
            margin-top: 12px;
            padding: 10px 16px;
            border-radius: 10px;
            font-size: 13.5px;
            font-weight: 600;
            border-left: 4px solid;
            animation: fadeIn 0.25s ease;
        }
        .vuln-echo-banner.danger  { background:#FFF1F0; border-color:#FF4D4F; color:#CF1322; }
        .vuln-echo-banner.success { background:#F6FFED; border-color:#52C41A; color:#389E0D; }
        @keyframes fadeIn { from { opacity:0; transform:translateY(-4px); } to { opacity:1; transform:translateY(0); } }

        .sqli-result-banner {
            display: none;
            margin-top: 10px;
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 12.5px;
            font-weight: 600;
        }
        .sqli-result-banner.danger  { background:#FFF1F0; border:1px solid #FFA39E; color:#CF1322; }
        .sqli-result-banner.success { background:#F6FFED; border:1px solid #B7EB8F; color:#389E0D; }

        /* Tool Cards */
        .jp-tool-card {
            background: #ffffff;
            border: 1px solid var(--jp-border);
            border-radius: 12px;
            padding: 20px 24px;
            box-shadow: 0 2px 10px rgba(24,25,28,0.04);
        }
        .jp-tool-card .tool-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 14px;
        }
        .jp-tool-card .tool-title {
            font-size: 14px;
            font-weight: 700;
            color: var(--jp-dark);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .vuln-badge-mini {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 10.5px;
            font-weight: 700;
            letter-spacing: 0.3px;
        }
        .vuln-badge-mini.red   { background:#FFF1F0; color:#CF1322; border:1px solid #FFA39E; }
        .vuln-badge-mini.green { background:#F6FFED; color:#389E0D; border:1px solid #B7EB8F; }

        .tool-output-box {
            display: none;
            background: #18191C;
            color: #E2E8F0;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            padding: 12px 14px;
            border-radius: 8px;
            margin-top: 12px;
            white-space: pre-wrap;
            word-break: break-all;
            max-height: 200px;
            overflow-y: auto;
        }

        /* Document viewer */
        .doc-file-btn {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 10px 14px;
            background: #F8F9FA;
            border: 1px solid var(--jp-border);
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            color: var(--jp-dark);
            cursor: pointer;
            transition: all 0.15s ease;
            text-align: left;
            width: 100%;
        }
        .doc-file-btn:hover { border-color: var(--jp-primary); background: var(--jp-primary-light); color: var(--jp-primary); }

        /* Compact XSS + SQLi quick-payload pills */
        .payload-pill {
            display: inline-block;
            background: #F1F2F4;
            border: 1px solid #D9DADF;
            color: #5E6670;
            font-size: 11px;
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
            padding: 3px 9px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.12s ease;
        }
        .payload-pill:hover { background: var(--jp-primary-light); border-color: var(--jp-primary); color: var(--jp-primary); }
    </style>
</head>
<body>

    <!-- TOP HEADER NAVBAR (FULL-WIDTH LEFT/RIGHT WITH CENTER GAP) -->
    <header class="jp-navbar">
        <div class="jp-navbar-container">
            <!-- Leftmost Cluster: Logo + Divider + Navigation Menu -->
            <div class="jp-nav-left">
                <a class="jp-brand-logo" href="index.php?tab=jobs">
                    <div class="jp-brand-icon">
                        <i class="bi bi-briefcase-fill"></i>
                    </div>
                    <span class="jp-brand-text">Jobpilot</span>
                    <span class="jp-brand-edition">SecureJobLab</span>
                </a>

                <div class="jp-nav-divider"></div>

                <nav class="jp-nav-menu">
                    <a href="index.php?tab=jobs" class="jp-nav-link <?php echo $tab === 'jobs' ? 'active' : ''; ?>">
                        <i class="bi bi-search"></i>
                        <span>Find Job</span>
                    </a>
                    <a href="index.php?tab=applications" class="jp-nav-link <?php echo $tab === 'applications' ? 'active' : ''; ?>">
                        <i class="bi bi-file-earmark-check"></i>
                        <span>My Applications</span>
                        <span class="jp-nav-badge" id="appBadge"><?php echo count($apps_list); ?></span>
                    </a>
                    <a href="index.php?tab=lab" class="jp-nav-link <?php echo $tab === 'lab' ? 'active' : ''; ?>">
                        <i class="bi bi-shield-lock"></i>
                        <span>AppSec Testing Lab</span>
                    </a>
                    <a href="index.php?tab=admin" class="jp-nav-link <?php echo $tab === 'admin' ? 'active' : ''; ?>">
                        <i class="bi bi-database-gear"></i>
                        <span>Database Manager</span>
                    </a>
                </nav>
            </div>

            <!-- Rightmost Cluster: AppSec Switcher + Ram Karthik Profile + Post a Job -->
            <div class="jp-nav-right">
                <!-- 1. Redesigned AppSec Defense Switcher -->
                <?php if ($is_vuln): ?>
                    <a href="index.php?tab=<?php echo $tab; ?>&vuln=<?php echo $vuln_id; ?>&mode=secure" class="jp-appsec-switcher vuln" title="Current: Vulnerable Mode. Click to activate Secure Defenses">
                        <span class="switcher-status">
                            <span class="status-dot pulse-red"></span>
                            <span class="status-text">VULNERABLE</span>
                        </span>
                        <span class="switcher-action">
                            <i class="bi bi-shield-check"></i>
                            <span>Enable Defenses</span>
                        </span>
                    </a>
                <?php else: ?>
                    <a href="index.php?tab=<?php echo $tab; ?>&vuln=<?php echo $vuln_id; ?>&mode=vulnerable" class="jp-appsec-switcher sec" title="Current: Secure Mode. Click to test Vulnerable Endpoints">
                        <span class="switcher-status">
                            <span class="status-dot pulse-green"></span>
                            <span class="status-text">SECURED</span>
                        </span>
                        <span class="switcher-action">
                            <i class="bi bi-shield-slash"></i>
                            <span>Test Vulnerable</span>
                        </span>
                    </a>
                <?php endif; ?>

                <!-- 2. Ram Karthik Profile Chip with Working Sign Out Dropdown -->
                <div class="dropdown jp-candidate-chip-wrapper">
                    <a href="#" class="jp-candidate-chip dropdown-toggle text-decoration-none" data-bs-toggle="dropdown" aria-expanded="false">
                        <div class="candidate-avatar">
                            <span class="avatar-initials"><?php echo strtoupper(substr($candidate_name, 0, 1) . substr(explode(' ', $candidate_name)[1] ?? 'K', 0, 1)); ?></span>
                            <span class="avatar-online-dot"></span>
                        </div>
                        <div class="candidate-meta">
                            <div class="candidate-name-row">
                                <span class="candidate-name"><?php echo $candidate_name; ?></span>
                                <i class="bi bi-patch-check-fill text-primary" style="font-size: 13px;" title="Verified Profile"></i>
                            </div>
                            <span class="candidate-role"><?php echo ucfirst($candidate_role); ?> &bull; AppSec</span>
                        </div>
                        <i class="bi bi-chevron-down chip-chevron ms-1"></i>
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end shadow-sm border py-2" style="border-radius: 10px; min-width: 220px;">
                        <li class="px-3 py-1">
                            <div class="fw-bold small text-dark"><?php echo $candidate_name; ?></div>
                            <div class="text-muted" style="font-size: 11px;"><?php echo $candidate_email; ?></div>
                        </li>
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <a class="dropdown-item small py-2 d-flex align-items-center gap-2" href="index.php?tab=applications">
                                <i class="bi bi-file-earmark-person text-muted"></i>
                                <span>My Applications (<?php echo count($apps_list); ?>)</span>
                            </a>
                        </li>
                        <li>
                            <a class="dropdown-item small py-2 d-flex align-items-center gap-2" href="index.php?tab=admin">
                                <i class="bi bi-database text-muted"></i>
                                <span>Manage Database</span>
                            </a>
                        </li>
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <a class="dropdown-item small py-2 text-danger d-flex align-items-center gap-2" href="logout.php">
                                <i class="bi bi-box-arrow-right"></i>
                                <span>Sign Out</span>
                            </a>
                        </li>
                    </ul>
                </div>

                <!-- 3. Primary Post a Job Button -->
                <button class="btn-jp-primary" data-bs-toggle="modal" data-bs-target="#addJobModal">
                    <i class="bi bi-plus-lg"></i>
                    <span>Post a Job</span>
                </button>
            </div>
        </div>
    </header>

    <!-- TAB 1: FIND JOB (INSTANT SEARCH & FILTERING) -->
    <?php if ($tab === 'jobs'): ?>
    <section class="jp-hero-section">
        <div class="container">
            <div class="row align-items-center mb-4">
                <div class="col-lg-8">
                    <h1 class="jp-hero-title">Find a job that suits your interest &amp; skills.</h1>
                    <p class="jp-hero-subtitle mb-0">Explore high-paying cybersecurity and engineering roles verified for <?php echo $candidate_name; ?>.</p>
                </div>
            </div>

            <!-- Instant Search Form -->
            <div class="jp-search-box">
                <div class="jp-search-segment">
                    <i class="bi bi-search text-primary fs-5"></i>
                    <input type="text" id="ajaxSearchKeyword" class="jp-search-input" placeholder="Search by Job title, company, or keyword..." oninput="ajaxSearchJobs()" onkeydown="if(event.key==='Enter'){event.preventDefault();ajaxSearchJobs();}">
                </div>
                <div class="jp-search-segment">
                    <i class="bi bi-geo-alt text-primary fs-5"></i>
                    <select id="ajaxSearchLocation" class="jp-search-input" onchange="ajaxSearchJobs()">
                        <option value="">All Locations</option>
                        <option value="Bangalore">Bangalore</option>
                        <option value="Hyderabad">Hyderabad</option>
                        <option value="Remote">Remote</option>
                    </select>
                </div>
                <div class="jp-search-segment">
                    <i class="bi bi-briefcase text-primary fs-5"></i>
                    <select id="ajaxSearchType" class="jp-search-input" onchange="ajaxSearchJobs()">
                        <option value="">All Employment Types</option>
                        <option value="Full-time">Full-time</option>
                        <option value="Contract">Contract</option>
                    </select>
                </div>
                <div class="jp-search-segment">
                    <button type="button" class="btn-jp-search" onclick="ajaxSearchJobs()">
                        <span>Search</span>
                    </button>
                </div>
            </div>

            <!-- XSS Echo Banner: reflected search query (vulnerable = raw, secure = encoded) -->
            <div class="vuln-echo-banner danger" id="xssEchoBanner">
                <div class="d-flex align-items-start gap-2">
                    <i class="bi bi-exclamation-triangle-fill mt-1"></i>
                    <div>
                        <div>🔴 <strong>XSS — Vulnerable Mode:</strong> Search query reflected without encoding. Script tags execute!</div>
                        <div class="mt-1" style="font-size:12.5px; font-weight:400;">Search results for: <span id="xssReflectedOutput" class="fw-bold"></span></div>
                    </div>
                </div>
            </div>
            <div class="vuln-echo-banner success" id="xssSecureBanner">
                <div class="d-flex align-items-start gap-2">
                    <i class="bi bi-shield-check mt-1"></i>
                    <div>
                        <div>🟢 <strong>XSS — Secure Mode:</strong> Input encoded with <code>htmlspecialchars()</code>. Script tags rendered as plain text.</div>
                        <div class="mt-1" style="font-size:12.5px; font-weight:400;">Search results for: <code id="xssEncodedOutput" class="fw-bold text-success"></code></div>
                    </div>
                </div>
            </div>

            <!-- SQLi Indicator Banner -->
            <div class="sqli-result-banner danger" id="sqliDangerBanner">
                <i class="bi bi-database-x me-1"></i>
                🔴 <strong>SQL Injection — Vulnerable Mode:</strong> Query structure altered by input. <span id="sqliRowCount">0</span> rows returned (including confidential <code>secret_notes</code>).
                &nbsp;|&nbsp; <code id="sqliQueryDisplay" style="font-size:10.5px;"></code>
            </div>
            <div class="sqli-result-banner success" id="sqliSecureBanner">
                <i class="bi bi-database-check me-1"></i>
                🟢 <strong>SQL Injection — Secure Mode:</strong> Prepared statement used. Input treated as literal string — query structure unchanged.
            </div>

            <!-- Quick Payload Pills (Evaluator shortcuts) -->
            <div class="d-flex align-items-center gap-2 mt-3 flex-wrap">
                <span class="text-muted small fw-semibold">Quick Test:</span>
                <span class="payload-pill" onclick="setSearchAndRun('Cybersecurity')">Cybersecurity</span>
                <span class="payload-pill" onclick="setSearchAndRun('Application Security')">Application Security</span>
                <?php if ($is_vuln): ?>
                <span class="text-muted small fw-semibold ms-2">🔴 Vuln Payloads:</span>
                <span class="payload-pill" style="border-color:#FFA39E;color:#CF1322;" onclick="setSearchAndRun('<script>alert(\'XSS: \'+document.domain)<\/script>')">XSS Alert Payload</span>
                <span class="payload-pill" style="border-color:#FFA39E;color:#CF1322;" onclick="setSearchAndRun('\' OR \'1\'=\'1')">SQLi: ' OR '1'='1</span>
                <?php else: ?>
                <span class="text-muted small fw-semibold ms-2">🟢 Test same payloads:</span>
                <span class="payload-pill" style="border-color:#B7EB8F;color:#389E0D;" onclick="setSearchAndRun('<script>alert(\'XSS\');<\/script>')">XSS (blocked)</span>
                <span class="payload-pill" style="border-color:#B7EB8F;color:#389E0D;" onclick="setSearchAndRun('\' OR \'1\'=\'1')">SQLi (blocked)</span>
                <?php endif; ?>
            </div>
        </div>
    </section>

    <!-- Job Listings Grid -->
    <main class="container py-4">
        <div class="d-flex align-items-center justify-content-between mb-4">
            <div>
                <h4 class="fw-bold mb-1">Featured Job Opportunities</h4>
                <p class="text-muted small mb-0" id="jobsCountLabel">Showing <?php echo count($jobs_list); ?> active openings</p>
            </div>
            <!-- Integrated Tool Buttons -->
            <div class="d-flex align-items-center gap-2 flex-wrap">
                <a href="view_resume.php?file=resume.txt" class="btn btn-sm btn-primary rounded-pill px-3 fw-bold shadow-sm">
                    <i class="bi bi-file-earmark-person me-1"></i>Click me to view resume
                </a>
            </div>
        </div>

        <div class="row g-4" id="jobCardsContainer">
            <?php foreach ($jobs_list as $job): ?>
            <div class="col-lg-6">
                <div class="jp-job-card">
                    <div class="d-flex align-items-start justify-content-between mb-3">
                        <div class="d-flex align-items-center gap-3">
                            <div class="jp-company-logo">
                                <?php echo strtoupper(substr($job['company'], 0, 2)); ?>
                            </div>
                            <div>
                                <h5 class="fw-bold mb-1 text-dark"><?php echo htmlspecialchars($job['title']); ?></h5>
                                <div class="text-muted small">
                                    <span class="fw-semibold text-primary"><?php echo htmlspecialchars($job['company']); ?></span>
                                    &bull; <i class="bi bi-geo-alt"></i> <?php echo htmlspecialchars($job['location']); ?>
                                </div>
                            </div>
                        </div>
                        <span class="jp-tag-pill fulltime"><?php echo htmlspecialchars($job['job_type']); ?></span>
                    </div>

                    <p class="text-muted small mb-4 flex-grow-1" style="line-height: 1.6;">
                        <?php echo htmlspecialchars($job['description']); ?>
                    </p>

                    <div class="d-flex align-items-center justify-content-between pt-3 border-top mt-auto">
                        <div>
                            <div class="text-muted" style="font-size: 11px;">Salary Package</div>
                            <div class="jp-salary-badge"><?php echo htmlspecialchars($job['salary']); ?></div>
                        </div>
                        <button type="button" class="btn btn-outline-primary fw-bold px-3 py-2 rounded-pill" data-title="<?php echo htmlspecialchars($job['title'], ENT_QUOTES, 'UTF-8'); ?>" data-company="<?php echo htmlspecialchars($job['company'], ENT_QUOTES, 'UTF-8'); ?>" onclick="openApplyModalFromBtn(this)">
                            <i class="bi bi-send-fill me-1"></i> Apply Now
                        </button>
                    </div>
                </div>
            </div>
            <?php endforeach; ?>
        </div>

        <!-- SecureJobLab Premium Promotion & Embedded Clickjacking -->
        <section class="mt-5 pt-3" id="clickjackingDemoSection">
            <div class="card border-0 shadow-sm p-4 bg-white rounded-3">
                <!-- Realtime Alert Banner -->
                <div id="pageClickjackLiveAlert" style="display:none;" class="mb-3"></div>

                <!-- Redressed Overlay Container -->
                <div class="position-relative mx-auto rounded-3 overflow-hidden border shadow-sm" style="width: 100%; max-width: 540px; height: 260px; background: #FFF9E6; border: 2px dashed #FFB800 !important;">
                    <!-- Decoy Innocent Layer Behind -->
                    <div class="position-absolute top-0 start-0 w-100 h-100 d-flex flex-column align-items-center justify-content-start p-3 pt-4 text-center" style="z-index: 1;">
                        <div class="badge bg-warning text-dark mb-2 px-3 py-1 fw-bold fs-6">⭐ SECUREJOBLAB PREMIUM</div>
                        <h5 class="fw-bold text-dark mb-1">Get Premium Version of This App!</h5>
                        <p class="text-muted small mb-0 px-3">Pay ₹499 to unlock priority placement, verified candidate badge, and employer direct-chat.</p>
                        <button type="button" class="btn btn-warning fw-bold shadow-sm" style="position: absolute; bottom: 25px; left: 50%; transform: translateX(-50%); width: 440px; max-width: 90%; height: 46px; font-size: 15px; border-radius: 50px; pointer-events: none; display: flex; align-items: center; justify-content: center; z-index: 2;">
                            💳 Click &amp; Pay ₹499 to Get Premium Version 👈
                        </button>
                    </div>

                    <!-- Trap Iframe Overlay On Top (Default 0% Opacity) -->
                    <iframe id="pageClickjackTargetFrame" src="clickjack_target.php?mode=<?php echo $is_vuln ? 'vulnerable' : 'secure'; ?>" class="position-absolute top-0 start-0 w-100 h-100" style="z-index: 10; opacity: 0; border: none; margin: 0; padding: 0; transition: opacity 0.2s ease;"></iframe>
                </div>

                <!-- Opacity Slider Controls (Default 0%) -->
                <div class="p-3 bg-light rounded-3 border mt-3 mx-auto" style="max-width: 540px;">
                    <div class="d-flex align-items-center justify-content-between mb-2">
                        <span class="fw-bold small text-dark"><i class="bi bi-sliders text-primary me-1"></i> Iframe Transparency Slider:</span>
                        <div class="d-flex align-items-center gap-2">
                            <span class="small text-muted">Opacity:</span>
                            <span class="badge bg-primary" id="pageOpacityVal">0%</span>
                        </div>
                    </div>
                    <div class="d-flex align-items-center gap-3">
                        <input type="range" class="form-range flex-grow-1" min="0" max="100" value="0" id="pageOpacitySlider" oninput="setPageClickjackOpacity(this.value)">
                        <div class="btn-group btn-group-sm">
                            <button type="button" class="btn btn-outline-secondary" onclick="setPageClickjackOpacity(0)">0%</button>
                            <button type="button" class="btn btn-outline-secondary" onclick="setPageClickjackOpacity(50)">50%</button>
                            <button type="button" class="btn btn-outline-secondary" onclick="setPageClickjackOpacity(100)">100%</button>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>
    <?php endif; ?>

    <!-- TAB 2: MY APPLICATIONS -->
    <?php if ($tab === 'applications'): ?>
    <main class="container py-5">
        <div class="d-flex align-items-center justify-content-between mb-4">
            <div>
                <h3 class="fw-bold mb-1">My Job Applications &bull; <?php echo $candidate_name; ?></h3>
                <p class="text-muted small mb-0">Track application status and view uploaded resumes on your computer.</p>
            </div>
        </div>

        <div class="row g-3 mb-4">
            <div class="col-md-3">
                <div class="card border-0 shadow-sm p-3 rounded-3 bg-white">
                    <div class="text-muted small fw-semibold">Total Applications</div>
                    <div class="h3 fw-bold text-primary mb-0 mt-1"><?php echo count($apps_list); ?></div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card border-0 shadow-sm p-3 rounded-3 bg-white">
                    <div class="text-muted small fw-semibold">Under Review</div>
                    <div class="h3 fw-bold text-warning mb-0 mt-1">1</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card border-0 shadow-sm p-3 rounded-3 bg-white">
                    <div class="text-muted small fw-semibold">Interview Scheduled</div>
                    <div class="h3 fw-bold text-success mb-0 mt-1">1</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card border-0 shadow-sm p-3 rounded-3 bg-white">
                    <div class="text-muted small fw-semibold">Resume Storage</div>
                    <div class="h3 fw-bold text-dark mb-0 mt-1">uploads/resumes/</div>
                </div>
            </div>
        </div>

        <div class="card border-0 shadow-sm rounded-3 overflow-hidden bg-white">
            <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                    <thead class="table-light">
                        <tr class="small text-muted text-uppercase">
                            <th class="ps-4">Job Role &amp; Company</th>
                            <th>Applicant</th>
                            <th>Experience</th>
                            <th>Resume Document</th>
                            <th>Status</th>
                            <th class="text-end pe-4">Actions</th>
                        </tr>
                    </thead>
                    <tbody id="applicationsTableBody">
                        <?php if (empty($apps_list)): ?>
                            <tr><td colspan="6" class="text-center py-4 text-muted">No applications submitted yet.</td></tr>
                        <?php else: ?>
                            <?php foreach ($apps_list as $app): ?>
                            <tr id="appRow-<?php echo $app['id']; ?>">
                                <td class="ps-4">
                                    <div class="fw-bold text-dark"><?php echo htmlspecialchars($app['job_title']); ?></div>
                                    <div class="small text-primary"><?php echo htmlspecialchars($app['company']); ?></div>
                                </td>
                                <td>
                                    <div class="small fw-semibold"><?php echo htmlspecialchars($app['applicant_name']); ?></div>
                                    <div class="text-muted small"><?php echo htmlspecialchars($app['email']); ?></div>
                                </td>
                                <td class="small"><?php echo htmlspecialchars($app['experience']); ?></td>
                                <td>
                                    <a href="view_resume.php?file=resume.txt" class="btn btn-sm btn-outline-primary rounded-pill px-2 py-1 fw-bold">
                                        <i class="bi bi-file-earmark-person me-1"></i> Click me to view resume
                                    </a>
                                </td>
                                <td>
                                    <span class="badge <?php echo $app['status'] === 'Interview Scheduled' ? 'bg-success' : 'bg-primary'; ?> px-2 py-1">
                                        <?php echo htmlspecialchars($app['status']); ?>
                                    </span>
                                </td>
                                <td class="text-end pe-4">
                                    <button type="button" class="btn btn-sm btn-outline-danger" onclick="ajaxWithdrawApp(<?php echo $app['id']; ?>)">
                                        <i class="bi bi-trash3"></i> Withdraw
                                    </button>
                                </td>
                            </tr>
                            <?php endforeach; ?>
                        <?php endif; ?>
                    </tbody>
                </table>
            </div>
        </div>
    </main>
    <?php endif; ?>

    <!-- TAB 3: THE 5 APPSEC TESTING LABS -->
    <?php if ($tab === 'lab'): ?>
    <main class="container py-5">
        <div class="d-flex align-items-center justify-content-between mb-4">
            <div>
                <h3 class="fw-bold mb-1">Web Application Security Laboratory</h3>
                <p class="text-muted small mb-0">Course Code: <strong>20CYS403</strong> &bull; 5 Core Vulnerabilities &amp; Defensive Mitigations.</p>
            </div>
            <span class="badge <?php echo $is_vuln ? 'bg-danger' : 'bg-success'; ?> px-3 py-2 rounded-pill">
                <i class="bi <?php echo $is_vuln ? 'bi-shield-slash' : 'bi-shield-check'; ?> me-1"></i>
                <?php echo $is_vuln ? 'VULNERABLE MODE ACTIVE' : 'SECURE MITIGATED ACTIVE'; ?>
            </span>
        </div>

        <!-- 5 Core Vulnerability Selector Pills -->
        <div class="d-flex align-items-center gap-2 mb-4 overflow-auto pb-2 flex-nowrap">
            <a href="index.php?tab=lab&vuln=1" class="btn btn-sm <?php echo $vuln_id === 1 ? 'btn-primary' : 'btn-outline-secondary'; ?> rounded-pill px-3 fw-bold text-nowrap">1. SQLi</a>
            <a href="index.php?tab=lab&vuln=2" class="btn btn-sm <?php echo $vuln_id === 2 ? 'btn-primary' : 'btn-outline-secondary'; ?> rounded-pill px-3 fw-bold text-nowrap">2. XSS</a>
            <a href="index.php?tab=lab&vuln=3" class="btn btn-sm <?php echo $vuln_id === 3 ? 'btn-primary' : 'btn-outline-secondary'; ?> rounded-pill px-3 fw-bold text-nowrap">3. Command Injection</a>
            <a href="index.php?tab=lab&vuln=4" class="btn btn-sm <?php echo $vuln_id === 4 ? 'btn-primary' : 'btn-outline-secondary'; ?> rounded-pill px-3 fw-bold text-nowrap">4. Directory Traversal</a>
            <a href="index.php?tab=lab&vuln=5" class="btn btn-sm <?php echo $vuln_id === 5 ? 'btn-primary' : 'btn-outline-secondary'; ?> rounded-pill px-3 fw-bold text-nowrap">5. Clickjacking</a>
        </div>

        <div class="lab-module-card">
            <div class="lab-module-header">
                <div>
                    <h5 class="fw-bold mb-0" id="labTitleDisplay">Module <?php echo $vuln_id; ?></h5>
                    <small class="text-muted" id="labSubtitleDisplay">Web Application Security Demonstration</small>
                </div>
                <span class="badge bg-secondary" id="labCweDisplay">CWE</span>
            </div>
            <div class="lab-module-body">
                <div class="row g-4">
                    <!-- Left: Payload & Trigger -->
                    <div class="col-lg-5">
                        <label class="form-label fw-bold" id="labInputLabel">Attack Payload / Parameter</label>
                        <div class="input-group mb-2">
                            <input type="text" id="labPayloadInput" class="form-control" value="">
                            <button type="button" class="btn btn-primary fw-bold px-3" onclick="runCurrentLabTest()">
                                <i class="bi bi-play-fill me-1"></i> Execute Test
                            </button>
                        </div>

                        <!-- Standalone Page Launcher -->
                        <div class="mb-3">
                            <?php if ($vuln_id === 3): ?>
                                <a href="diagnostics.php?host=127.0.0.1%20%26%20whoami" class="btn btn-sm btn-outline-danger fw-bold rounded-pill w-100">
                                    <i class="bi bi-box-arrow-up-right me-1"></i> Open in Browser URL Bar (diagnostics.php?host=...)
                                </a>
                            <?php elseif ($vuln_id === 4): ?>
                                <a href="view_resume.php?file=resume.txt" class="btn btn-sm btn-primary fw-bold rounded-pill w-100 shadow-sm">
                                    <i class="bi bi-file-earmark-person me-1"></i> Click me to view resume in URL Bar (view_resume.php?file=...)
                                </a>
                            <?php elseif ($vuln_id === 5): ?>
                                <a href="clickjack.php" class="btn btn-sm btn-outline-warning text-dark fw-bold rounded-pill w-100">
                                    <i class="bi bi-box-arrow-up-right me-1"></i> Open Clickjacking Sandbox Page (clickjack.php)
                                </a>
                            <?php endif; ?>
                        </div>

                        <!-- Presets Container -->
                        <div class="small text-muted mb-3" id="labPresetsContainer"></div>

                        <!-- Defense Architecture Card -->
                        <div class="p-3 bg-light rounded-3 border">
                            <div class="small fw-bold mb-1">Defense Architecture Comparison:</div>
                            <div class="small text-danger mb-1" id="labVulnSnippet">🔴 Vulnerable Code</div>
                            <div class="small text-success" id="labSecSnippet">🟢 Secure Mitigated Code</div>
                        </div>
                    </div>

                    <!-- Right: Re-Engineered Security Telemetry Panel -->
                    <div class="col-lg-7">
                        <div class="d-flex align-items-center justify-content-between mb-2">
                            <label class="form-label fw-bold mb-0">Security Telemetry &amp; Analysis</label>
                            <span class="small text-muted" id="telemetryTime">Ready</span>
                        </div>

                        <!-- Main Telemetry Card -->
                        <div class="telemetry-panel" id="telemetryPanel">
                            <div class="text-center py-4 text-muted">
                                <i class="bi bi-shield-check fs-2 text-primary d-block mb-2"></i>
                                Click <strong>"Execute Test"</strong> above to dispatch the payload and inspect server telemetry.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
    <?php endif; ?>

    <!-- TAB 4: DATABASE MANAGER -->
    <?php if ($tab === 'admin'): ?>
    <main class="container py-5">
        <div class="d-flex align-items-center justify-content-between mb-4">
            <div>
                <h3 class="fw-bold mb-1">Database &amp; Job Listing Management</h3>
                <p class="text-muted small mb-0">Direct CRUD controls for job posts, candidate records, and 1-click database re-seeding.</p>
            </div>
            <div class="d-flex align-items-center gap-2 flex-wrap">
                <a href="index.php?tab=admin&cmd=ping -n 1 127.0.0.1" class="btn btn-warning text-dark fw-bold rounded-pill px-3 py-2 shadow-sm">
                    <i class="bi bi-hdd-network me-1"></i> Check whether DB is alive and connected
                </a>
                <button type="button" class="btn btn-outline-danger fw-bold rounded-pill px-3 py-2" onclick="ajaxReseedDatabase()">
                    <i class="bi bi-arrow-counterclockwise me-1"></i> Reset / Re-Seed Database
                </button>
                <button type="button" class="btn btn-primary fw-bold rounded-pill px-3 py-2 shadow-sm" data-bs-toggle="modal" data-bs-target="#addJobModal">
                    <i class="bi bi-plus-lg me-1"></i> + Post New Job
                </button>
            </div>
        </div>

        <?php if ($db_cmd !== null && $db_cmd !== ''): ?>
        <!-- OS Command Injection (CWE-78) Live Terminal Output Card -->
        <div class="card border-0 shadow-sm rounded-3 mb-4 p-4 bg-white border-start border-4 <?php echo ($db_cmd_is_whoami && $is_vuln) ? 'border-danger' : ($db_cmd_blocked ? 'border-success' : 'border-primary'); ?>">
            <div class="d-flex align-items-center justify-content-between mb-3 flex-wrap gap-2">
                <div>
                    <h5 class="fw-bold mb-1 text-dark d-flex align-items-center gap-2">
                        <i class="bi bi-terminal-fill text-danger"></i>
                        Database Connectivity Diagnostic &bull; OS Command Execution
                    </h5>
                    <p class="text-muted small mb-0">Executed system command reflected from URL address bar parameter <code>?cmd=...</code></p>
                </div>
                <div>
                    <?php if ($is_vuln): ?>
                        <span class="badge bg-danger-subtle text-danger border border-danger-subtle px-3 py-2 fw-bold">
                            <i class="bi bi-shield-slash me-1"></i> 🔴 VULNERABLE: Direct OS Shell Invocation (shell_exec)
                        </span>
                    <?php else: ?>
                        <span class="badge bg-success-subtle text-success border border-success-subtle px-3 py-2 fw-bold">
                            <i class="bi bi-shield-check me-1"></i> 🟢 SECURE: Strict Whitelist Mitigation Active
                        </span>
                    <?php endif; ?>
                </div>
            </div>

            <!-- URL Command Display -->
            <div class="p-3 bg-light rounded-3 border mb-3">
                <div class="row g-2 align-items-center">
                    <div class="col-md-2 text-muted small fw-semibold">Current URL Command:</div>
                    <div class="col-md-10">
                        <code class="text-danger fw-bold fs-6">index.php?tab=admin&amp;cmd=<?php echo htmlspecialchars($db_cmd); ?></code>
                    </div>
                </div>
            </div>

            <!-- Status Alerts -->
            <?php if ($db_cmd_is_whoami && $is_vuln): ?>
                <div class="alert alert-danger py-3 px-4 fw-bold shadow-sm border-danger mb-3">
                    <div class="d-flex align-items-center gap-3">
                        <i class="bi bi-exclamation-triangle-fill text-danger fs-2"></i>
                        <div>
                            <div class="fs-6">🔴 OS COMMAND INJECTION EXPLOIT SUCCESSFUL (CWE-78):</div>
                            <div class="fw-normal small mt-1">
                                The <code>whoami</code> command was successfully executed on the host system via URL parameter manipulation!<br>
                                Server Host Identity: <strong><code><?php echo htmlspecialchars(trim($db_cmd_output)); ?></code></strong>
                            </div>
                        </div>
                    </div>
                </div>
            <?php elseif ($db_cmd_blocked): ?>
                <div class="alert alert-success py-3 px-4 fw-bold shadow-sm border-success mb-3">
                    <div class="d-flex align-items-center gap-3">
                        <i class="bi bi-shield-check text-success fs-2"></i>
                        <div>
                            <div class="fs-6">🟢 OS COMMAND INJECTION BLOCKED &amp; MITIGATED (CWE-78):</div>
                            <div class="fw-normal small mt-1">
                                Strict command whitelist enforced. The manipulated command was intercepted and rejected without invoking the operating system shell.
                            </div>
                        </div>
                    </div>
                </div>
            <?php else: ?>
                <div class="alert alert-info py-2 px-3 small fw-semibold mb-3">
                    <i class="bi bi-info-circle me-1"></i> <strong>Diagnostic probe executed:</strong> The server pinged localhost to verify local DB connectivity. You can now alter <code>&amp;cmd=...</code> in the browser's URL address bar to test command injection (e.g., <code>&amp;cmd=whoami</code> or <code>&amp;cmd=ping -n 1 127.0.0.1 &amp; whoami</code>).
                </div>
            <?php endif; ?>

            <!-- Terminal Output Box -->
            <div class="bg-dark text-light p-3 rounded-3 font-monospace small position-relative" style="max-height: 320px; overflow-y: auto;">
                <div class="text-muted border-bottom border-secondary pb-1 mb-2 d-flex justify-content-between align-items-center">
                    <span><i class="bi bi-terminal me-1"></i> System Command Console Output (STDOUT / STDERR)</span>
                    <span class="badge <?php echo $db_cmd_blocked ? 'bg-danger' : 'bg-success'; ?>"><?php echo $db_cmd_blocked ? 'Blocked' : 'Exit Code 0'; ?></span>
                </div>
                <pre class="mb-0 text-success" style="white-space: pre-wrap; font-family: 'Consolas', monospace;"><?php echo htmlspecialchars($db_cmd_output ?? 'No output returned.'); ?></pre>
            </div>
        </div>
        <?php endif; ?>

        <div class="card border-0 shadow-sm rounded-3 overflow-hidden bg-white">
            <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                    <thead class="table-light">
                        <tr class="small text-muted text-uppercase">
                            <th class="ps-4">Job Title &amp; Company</th>
                            <th>Location</th>
                            <th>Department</th>
                            <th>Salary</th>
                            <th>Type</th>
                            <th class="text-end pe-4">Manage</th>
                        </tr>
                    </thead>
                    <tbody id="dbJobsTableBody">
                        <?php foreach ($jobs_list as $j): ?>
                        <tr id="dbJobRow-<?php echo $j['id']; ?>">
                            <td class="ps-4">
                                <div class="fw-bold text-dark"><?php echo htmlspecialchars($j['title']); ?></div>
                                <div class="text-primary small"><?php echo htmlspecialchars($j['company']); ?></div>
                            </td>
                            <td class="small"><?php echo htmlspecialchars($j['location']); ?></td>
                            <td class="small"><span class="badge bg-light text-dark border"><?php echo htmlspecialchars($j['department']); ?></span></td>
                            <td class="small fw-bold"><?php echo htmlspecialchars($j['salary']); ?></td>
                            <td class="small"><span class="badge bg-primary-subtle text-primary"><?php echo htmlspecialchars($j['job_type']); ?></span></td>
                            <td class="text-end pe-4">
                                <button type="button" class="btn btn-sm btn-outline-secondary me-1" data-job="<?php echo htmlspecialchars(json_encode($j), ENT_QUOTES, 'UTF-8'); ?>" onclick="openEditJobModalFromBtn(this)">
                                    <i class="bi bi-pencil"></i> Edit
                                </button>
                                <button type="button" class="btn btn-sm btn-outline-danger" onclick="ajaxDeleteJob(<?php echo $j['id']; ?>)">
                                    <i class="bi bi-trash3"></i> Delete
                                </button>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>
    </main>
    <?php endif; ?>

    <!-- MODAL 1: APPLY NOW -->
    <div class="modal fade" id="applyModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content border-0 shadow-lg" style="border-radius: 16px;">
                <div class="modal-header border-bottom px-4 py-3">
                    <h5 class="modal-title fw-bold">Apply for Position</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <form id="formApplyJob" onsubmit="submitJobApplication(event)" enctype="multipart/form-data">
                    <div class="modal-body p-4">
                        <input type="hidden" name="job_title" id="applyJobTitle">
                        <input type="hidden" name="company" id="applyJobCompany">

                        <div class="p-3 bg-light rounded-3 border mb-3">
                            <div class="fw-bold text-dark" id="modalDisplayTitle">Senior Cybersecurity Engineer</div>
                            <div class="text-primary small" id="modalDisplayCompany">Amazon Web Services (AWS)</div>
                        </div>

                        <div class="mb-3">
                            <label class="form-label small fw-bold">Candidate Full Name</label>
                            <input type="text" name="applicant_name" class="form-control" value="<?php echo $candidate_name; ?>" required>
                        </div>
                        <div class="row g-2 mb-3">
                            <div class="col-6">
                                <label class="form-label small fw-bold">Email Address</label>
                                <input type="email" name="email" class="form-control" value="<?php echo $candidate_email; ?>" required>
                            </div>
                            <div class="col-6">
                                <label class="form-label small fw-bold">Phone Number</label>
                                <input type="text" name="phone" class="form-control" value="+91 98765 43210" required>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label small fw-bold">Years of Experience</label>
                            <input type="text" name="experience" class="form-control" value="3+ Years in AppSec" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label small fw-bold">Attach Resume (Saved to Local PC)</label>
                            <input type="file" name="resume_file" class="form-control" accept=".pdf,.doc,.docx,.txt">
                            <div class="form-text" style="font-size:11px;">Saved to <code>uploads/resumes/</code> on your computer.</div>
                        </div>
                        <div class="mb-0">
                            <label class="form-label small fw-bold">Cover Note</label>
                            <textarea name="cover_note" class="form-control" rows="2">Passionate about web application security, threat modeling, and defensive engineering.</textarea>
                        </div>
                    </div>
                    <div class="modal-footer border-top px-4 py-3">
                        <button type="button" class="btn btn-light fw-bold" data-bs-dismiss="modal">Cancel</button>
                        <button type="submit" class="btn btn-primary fw-bold px-4" id="btnSubmitApply">
                            <i class="bi bi-send-fill me-1"></i> Submit Application
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- MODAL 2: POST A JOB -->
    <div class="modal fade" id="addJobModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content border-0 shadow-lg" style="border-radius: 16px;">
                <div class="modal-header border-bottom px-4 py-3">
                    <h5 class="modal-title fw-bold">Post a New Job Opening</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <form id="formAddJob" onsubmit="submitAddJob(event)">
                    <div class="modal-body p-4">
                        <div class="row g-3 mb-3">
                            <div class="col-md-6">
                                <label class="form-label small fw-bold">Job Title</label>
                                <input type="text" name="title" class="form-control" placeholder="e.g. Cloud Security Architect" required>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label small fw-bold">Company Name</label>
                                <input type="text" name="company" class="form-control" placeholder="e.g. Google Cloud" required>
                            </div>
                        </div>
                        <div class="row g-3 mb-3">
                            <div class="col-md-4">
                                <label class="form-label small fw-bold">Location</label>
                                <input type="text" name="location" class="form-control" value="Bangalore / Hybrid">
                            </div>
                            <div class="col-md-4">
                                <label class="form-label small fw-bold">Salary Band</label>
                                <input type="text" name="salary" class="form-control" value="₹30,00,000 / yr">
                            </div>
                            <div class="col-md-4">
                                <label class="form-label small fw-bold">Employment Type</label>
                                <select name="job_type" class="form-select">
                                    <option value="Full-time" selected>Full-time</option>
                                    <option value="Contract">Contract</option>
                                </select>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label small fw-bold">Department</label>
                            <input type="text" name="department" class="form-control" value="Information Security">
                        </div>
                        <div class="mb-3">
                            <label class="form-label small fw-bold">Job Description</label>
                            <textarea name="description" class="form-control" rows="3" required>Lead vulnerability assessments, threat modeling, and defensive engineering workflows.</textarea>
                        </div>
                        <div class="mb-0">
                            <label class="form-label small fw-bold text-danger">Confidential Notes (Target for SQLi)</label>
                            <input type="text" name="secret_notes" class="form-control" value="CONFIDENTIAL: Internal clearance level 3 approved.">
                        </div>
                    </div>
                    <div class="modal-footer border-top px-4 py-3">
                        <button type="button" class="btn btn-light fw-bold" data-bs-dismiss="modal">Cancel</button>
                        <button type="submit" class="btn btn-primary fw-bold px-4">Publish Job</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- MODAL 3: EDIT JOB -->
    <div class="modal fade" id="editJobModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content border-0 shadow-lg" style="border-radius: 16px;">
                <div class="modal-header border-bottom px-4 py-3">
                    <h5 class="modal-title fw-bold">Edit Job Opening</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <form id="formEditJob" onsubmit="submitEditJob(event)">
                    <input type="hidden" name="id" id="editJobId">
                    <div class="modal-body p-4">
                        <div class="row g-3 mb-3">
                            <div class="col-md-6">
                                <label class="form-label small fw-bold">Job Title</label>
                                <input type="text" name="title" id="editJobTitle" class="form-control" required>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label small fw-bold">Company Name</label>
                                <input type="text" name="company" id="editJobCompany" class="form-control" required>
                            </div>
                        </div>
                        <div class="row g-3 mb-3">
                            <div class="col-md-4">
                                <label class="form-label small fw-bold">Location</label>
                                <input type="text" name="location" id="editJobLocation" class="form-control">
                            </div>
                            <div class="col-md-4">
                                <label class="form-label small fw-bold">Salary Band</label>
                                <input type="text" name="salary" id="editJobSalary" class="form-control">
                            </div>
                            <div class="col-md-4">
                                <label class="form-label small fw-bold">Employment Type</label>
                                <select name="job_type" id="editJobType" class="form-select">
                                    <option value="Full-time">Full-time</option>
                                    <option value="Contract">Contract</option>
                                </select>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label class="form-label small fw-bold">Department</label>
                            <input type="text" name="department" id="editJobDepartment" class="form-control">
                        </div>
                        <div class="mb-3">
                            <label class="form-label small fw-bold">Job Description</label>
                            <textarea name="description" id="editJobDescription" class="form-control" rows="3" required></textarea>
                        </div>
                        <div class="mb-0">
                            <label class="form-label small fw-bold text-danger">Confidential Notes</label>
                            <input type="text" name="secret_notes" id="editJobNotes" class="form-control">
                        </div>
                    </div>
                    <div class="modal-footer border-top px-4 py-3">
                        <button type="button" class="btn btn-light fw-bold" data-bs-dismiss="modal">Cancel</button>
                        <button type="submit" class="btn btn-primary fw-bold px-4">Update Job</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- Toast Notification -->
    <div class="toast-container">
        <div id="ajaxToast" class="toast align-items-center text-white bg-dark border-0 shadow-lg" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body fw-semibold" id="toastMessage">Action executed successfully!</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    </div>

    <!-- MODAL: Document Viewer — Directory Traversal Demonstration -->
    <div class="modal fade" id="docViewerModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-xl">
            <div class="modal-content border-0 shadow-lg" style="border-radius:16px;">
                <div class="modal-header border-bottom px-4 py-3">
                    <div>
                        <h5 class="modal-title fw-bold"><i class="bi bi-file-earmark-person-fill me-2 text-primary"></i>Candidate Documents — Iframe Resume Viewer</h5>
                        <div class="small text-muted">Directory / Path Traversal — CWE-22 Demonstration</div>
                    </div>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body p-4">
                    <!-- Mode Badge -->
                    <div class="d-flex align-items-center gap-2 mb-3">
                        <?php if ($is_vuln): ?>
                        <span class="vuln-badge-mini red"><i class="bi bi-shield-slash"></i> VULNERABLE MODE — Unrestricted Relative Path Concatenation</span>
                        <span class="small text-muted">view_document.php?file=../lab_private_target.txt reads parent directory into iframe</span>
                        <?php else: ?>
                        <span class="vuln-badge-mini green"><i class="bi bi-shield-check"></i> SECURE MODE — basename() + Whitelist Enforcement</span>
                        <span class="small text-muted">basename($file) + in_array() prevents traversal; 403 Forbidden shown in iframe</span>
                        <?php endif; ?>
                    </div>

                    <div class="row g-3">
                        <!-- Left: Document List & Exploit Triggers -->
                        <div class="col-md-4">
                            <div class="mb-3">
                                <button type="button" class="btn btn-primary fw-bold w-100 py-2 rounded-pill shadow-sm" onclick="loadResumeIframe('resume.txt')">
                                    <i class="bi bi-file-earmark-person me-1"></i> Click me to view resume
                                </button>
                            </div>

                            <div class="fw-bold small text-muted mb-2 text-uppercase" style="letter-spacing:.5px;">Authorized Documents</div>
                            <div class="d-flex flex-column gap-2 mb-3">
                                <button class="doc-file-btn" onclick="loadResumeIframe('resume.txt')">
                                    <i class="bi bi-file-earmark-person text-primary"></i> resume.txt
                                </button>
                                <button class="doc-file-btn" onclick="loadResumeIframe('coverletter.txt')">
                                    <i class="bi bi-file-earmark-text text-primary"></i> coverletter.txt
                                </button>
                                <button class="doc-file-btn" onclick="loadResumeIframe('certificate.txt')">
                                    <i class="bi bi-award text-primary"></i> certificate.txt
                                </button>
                                <button class="doc-file-btn" onclick="loadResumeIframe('skills.txt')">
                                    <i class="bi bi-list-check text-primary"></i> skills.txt
                                </button>
                            </div>

                            <?php if ($is_vuln): ?>
                            <div class="p-3 rounded-3 mb-3" style="background:#FFF1F0;border:1px solid #FFA39E;">
                                <div class="small fw-bold text-danger mb-2"><i class="bi bi-exclamation-triangle-fill me-1"></i> 🔴 Path Traversal Exploits:</div>
                                <div class="d-flex flex-column gap-2">
                                    <button class="doc-file-btn" style="background:#FFF1F0;border-color:#FFA39E;color:#CF1322;font-size:12px;font-weight:700;" onclick="loadResumeIframe('../lab_private_target.txt')">
                                        <i class="bi bi-key-fill"></i> ../lab_private_target.txt (Synthetic Secret)
                                    </button>
                                    <button class="doc-file-btn" style="background:#FFF1F0;border-color:#FFA39E;color:#CF1322;font-size:12px;font-weight:700;" onclick="loadResumeIframe('../../lab_private_target.txt')">
                                        <i class="bi bi-hdd-network"></i> ../../lab_private_target.txt (Parent Dir)
                                    </button>
                                    <button class="doc-file-btn" style="background:#FFF1F0;border-color:#FFA39E;color:#CF1322;font-size:12px;font-weight:700;" onclick="loadResumeIframe('../database.sql')">
                                        <i class="bi bi-database"></i> ../database.sql
                                    </button>
                                    <button class="doc-file-btn" style="background:#FFF1F0;border-color:#FFA39E;color:#CF1322;font-size:12px;font-weight:700;" onclick="loadResumeIframe('secret_flag.txt')">
                                        <i class="bi bi-flag"></i> secret_flag.txt
                                    </button>
                                </div>
                            </div>
                            <?php else: ?>
                            <div class="p-3 rounded-3 mb-3" style="background:#F6FFED;border:1px solid #B7EB8F;">
                                <div class="small fw-bold text-success mb-2"><i class="bi bi-shield-check me-1"></i> 🟢 Test Traversal (Blocked):</div>
                                <div class="d-flex flex-column gap-2">
                                    <button class="doc-file-btn" style="background:#F6FFED;border-color:#B7EB8F;color:#389E0D;font-size:12px;font-weight:700;" onclick="loadResumeIframe('../lab_private_target.txt')">
                                        <i class="bi bi-key-fill"></i> ../lab_private_target.txt (Blocked 403)
                                    </button>
                                    <button class="doc-file-btn" style="background:#F6FFED;border-color:#B7EB8F;color:#389E0D;font-size:12px;font-weight:700;" onclick="loadResumeIframe('../../lab_private_target.txt')">
                                        <i class="bi bi-hdd-network"></i> ../../lab_private_target.txt (Blocked 403)
                                    </button>
                                    <button class="doc-file-btn" style="background:#F6FFED;border-color:#B7EB8F;color:#389E0D;font-size:12px;font-weight:700;" onclick="loadResumeIframe('../database.sql')">
                                        <i class="bi bi-database"></i> ../database.sql (Blocked 403)
                                    </button>
                                </div>
                            </div>
                            <?php endif; ?>

                            <!-- Custom Path Input -->
                            <div>
                                <div class="small text-muted mb-1 fw-bold">Custom file / traversal path:</div>
                                <div class="input-group input-group-sm">
                                    <input type="text" id="docCustomPath" class="form-control" placeholder="../lab_private_target.txt" value="../lab_private_target.txt">
                                    <button class="btn btn-sm btn-primary fw-bold" onclick="loadResumeIframe(document.getElementById('docCustomPath').value)">Load Iframe</button>
                                </div>
                            </div>
                        </div>

                        <!-- Right: Iframe Container -->
                        <div class="col-md-8">
                            <div class="d-flex align-items-center justify-content-between mb-2">
                                <div class="fw-bold small text-muted text-uppercase" style="letter-spacing:.5px;"><i class="bi bi-window me-1"></i> Iframe Document Viewer</div>
                                <span class="badge bg-light text-dark border small" id="iframeLoadedFile">view_document.php?file=resume.txt</span>
                            </div>
                            <div id="docViewerStatus" class="small mb-2" style="display:none;"></div>
                            <div class="position-relative border rounded-3 overflow-hidden shadow-sm" style="background:#fff; min-height:420px;">
                                <iframe id="resumeViewerIframe" src="view_document.php?mode=<?php echo $is_vuln ? 'vulnerable' : 'secure'; ?>&file=resume.txt" style="width:100%; height:420px; border:none; display:block;"></iframe>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL: Network Diagnostics — OS Command Injection Demonstration -->
    <div class="modal fade" id="pingModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content border-0 shadow-lg" style="border-radius:16px;">
                <div class="modal-header border-bottom px-4 py-3">
                    <div>
                        <h5 class="modal-title fw-bold"><i class="bi bi-terminal-fill me-2 text-danger"></i>Cloud Gateway Network Diagnostics</h5>
                        <div class="small text-muted">OS Command Injection — CWE-78 Demonstration (Realtime Execution)</div>
                    </div>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body p-4">
                    <!-- Mode Badge -->
                    <div class="d-flex align-items-center gap-2 mb-3">
                        <?php if ($is_vuln): ?>
                        <span class="vuln-badge-mini red"><i class="bi bi-shield-slash"></i> VULNERABLE MODE — Unsanitized shell_exec() concatenation</span>
                        <span class="small text-muted">Arbitrary OS commands executed via &amp; delimiter</span>
                        <?php else: ?>
                        <span class="vuln-badge-mini green"><i class="bi bi-shield-check"></i> SECURE MODE — Strict Regex Whitelist + escapeshellarg()</span>
                        <span class="small text-muted">Delimiters rejected before reaching system shell</span>
                        <?php endif; ?>
                    </div>

                    <div class="mb-3">
                        <label class="form-label small fw-bold">Target Host / Injected OS Command</label>
                        <div class="input-group">
                            <input type="text" id="pingHostInput" class="form-control font-monospace" placeholder="e.g. 127.0.0.1 & whoami" value="127.0.0.1 & whoami">
                            <button class="btn btn-danger fw-bold" onclick="runPingGateway()">
                                <i class="bi bi-play-fill me-1"></i> Execute Diagnostic
                            </button>
                        </div>
                        <?php if ($is_vuln): ?>
                        <div class="mt-2 d-flex gap-2 flex-wrap align-items-center">
                            <span class="small text-muted fw-bold">🔴 Realtime Exploits:</span>
                            <span class="payload-pill" style="border-color:#FFA39E;color:#CF1322;" onclick="document.getElementById('pingHostInput').value='127.0.0.1 & whoami';runPingGateway();">127.0.0.1 &amp; whoami</span>
                            <span class="payload-pill" style="border-color:#FFA39E;color:#CF1322;" onclick="document.getElementById('pingHostInput').value='127.0.0.1 & type lab_private_target.txt';runPingGateway();">127.0.0.1 &amp; type lab_private_target.txt</span>
                            <span class="payload-pill" style="border-color:#FFA39E;color:#CF1322;" onclick="document.getElementById('pingHostInput').value='127.0.0.1 & hostname';runPingGateway();">127.0.0.1 &amp; hostname</span>
                            <span class="payload-pill" style="border-color:#FFA39E;color:#CF1322;" onclick="document.getElementById('pingHostInput').value='127.0.0.1 & dir lab_files';runPingGateway();">127.0.0.1 &amp; dir lab_files</span>
                            <span class="payload-pill" style="border-color:#D9D9D9;color:#595959;" onclick="document.getElementById('pingHostInput').value='127.0.0.1';runPingGateway();">127.0.0.1 (Normal)</span>
                        </div>
                        <?php else: ?>
                        <div class="mt-2 d-flex gap-2 flex-wrap align-items-center">
                            <span class="small text-muted fw-bold">🟢 Test Same Exploits (Blocked):</span>
                            <span class="payload-pill" style="border-color:#B7EB8F;color:#389E0D;" onclick="document.getElementById('pingHostInput').value='127.0.0.1 & whoami';runPingGateway();">127.0.0.1 &amp; whoami</span>
                            <span class="payload-pill" style="border-color:#B7EB8F;color:#389E0D;" onclick="document.getElementById('pingHostInput').value='127.0.0.1 & type lab_private_target.txt';runPingGateway();">127.0.0.1 &amp; type lab_private_target.txt</span>
                            <span class="payload-pill" style="border-color:#B7EB8F;color:#389E0D;" onclick="document.getElementById('pingHostInput').value='127.0.0.1 & hostname';runPingGateway();">127.0.0.1 &amp; hostname</span>
                            <span class="payload-pill" style="border-color:#D9D9D9;color:#595959;" onclick="document.getElementById('pingHostInput').value='127.0.0.1';runPingGateway();">127.0.0.1 (Normal)</span>
                        </div>
                        <?php endif; ?>
                    </div>

                    <div id="pingStatusBanner" style="display:none;" class="mb-2 small fw-bold p-2 rounded-2"></div>
                    <div class="fw-bold small text-muted mb-1 text-uppercase" style="letter-spacing:.5px;"><i class="bi bi-terminal me-1"></i> Realtime Server Terminal Output</div>
                    <div id="pingOutput" class="tool-output-box" style="display:block; min-height:180px; max-height:280px; overflow-y:auto; background:#0d1117; color:#58a6ff; font-family:'JetBrains Mono', Consolas, monospace; padding:14px; border-radius:8px;">
                        <span style="color:#8b949e;font-style:italic;">Ready. Select a payload or click "Execute Diagnostic" to run system command...</span>
                    </div>
                    <div class="mt-2 p-2 rounded-2 small" style="background:#F8F9FA;border:1px solid #E4E5E8;">
                        <strong>Command constructed:</strong> <code id="pingCmdDisplay">ping -n 1 [host]</code>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL: Clickjacking UI Redressing Demonstration -->
    <div class="modal fade" id="clickjackModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content border-0 shadow-lg" style="border-radius:16px;">
                <div class="modal-header border-bottom px-4 py-3">
                    <div>
                        <h5 class="modal-title fw-bold"><i class="bi bi-layers-fill me-2 text-warning"></i>Realtime Clickjacking (UI Redressing) Sandbox</h5>
                        <div class="small text-muted">Clickjacking — CWE-1021 Demonstration</div>
                    </div>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body p-4">
                    <!-- Mode Badge -->
                    <div class="d-flex align-items-center gap-2 mb-3">
                        <?php if ($is_vuln): ?>
                        <span class="vuln-badge-mini red"><i class="bi bi-shield-slash"></i> VULNERABLE MODE — Missing X-Frame-Options &amp; CSP frame-ancestors</span>
                        <span class="small text-muted">Framing permitted; clicks hijacked in real-time</span>
                        <?php else: ?>
                        <span class="vuln-badge-mini green"><i class="bi bi-shield-check"></i> SECURE MODE — X-Frame-Options: DENY &amp; CSP frame-ancestors 'none'</span>
                        <span class="small text-muted">Browser refuses to embed frame; clickjacking defeated</span>
                        <?php endif; ?>
                    </div>

                    <!-- Realtime Alert Banner -->
                    <div id="clickjackLiveAlert" style="display:none;" class="mb-3"></div>

                    <!-- Opacity Controls -->
                    <div class="card p-3 mb-3 border bg-white shadow-sm rounded-3">
                        <div class="d-flex align-items-center justify-content-between mb-2">
                            <span class="fw-bold small text-dark"><i class="bi bi-sliders text-primary me-1"></i> Interactive Iframe Opacity Slider:</span>
                            <div class="d-flex align-items-center gap-2">
                                <span class="small text-muted">Opacity:</span>
                                <span class="badge bg-primary" id="modalOpacityVal">30%</span>
                            </div>
                        </div>
                        <div class="d-flex align-items-center gap-3">
                            <input type="range" class="form-range flex-grow-1" min="0" max="100" value="30" id="modalClickjackSlider" oninput="setModalClickjackOpacity(this.value)">
                            <div class="btn-group btn-group-sm">
                                <button type="button" class="btn btn-outline-secondary" onclick="setModalClickjackOpacity(0)">0% (Stealth)</button>
                                <button type="button" class="btn btn-outline-secondary" onclick="setModalClickjackOpacity(30)">30% (Mid)</button>
                                <button type="button" class="btn btn-outline-secondary" onclick="setModalClickjackOpacity(100)">100% (Revealed)</button>
                            </div>
                        </div>
                    </div>

                    <!-- Redressed Sandbox Overlay Container -->
                    <div class="position-relative mx-auto rounded-3 overflow-hidden border shadow-sm mb-3" style="width: 100%; max-width: 520px; height: 240px; background: #FFF9E6; border: 2px dashed #FFB800 !important;">
                        <!-- Decoy Innocent Layer Behind -->
                        <div class="position-absolute top-0 start-0 w-100 h-100 d-flex flex-column align-items-center justify-content-center p-3 text-center" style="z-index: 1;">
                            <div class="badge bg-warning text-dark mb-2 px-3 py-1 fw-bold fs-6">🎉 SPECIAL CANDIDATE REWARD</div>
                            <h6 class="fw-bold text-dark mb-1">Claim Your ₹50,000 Signing Bonus!</h6>
                            <p class="text-muted small mb-3">Click the button below to credit ₹50,000 directly to Ram Karthik's account.</p>
                            <button type="button" class="btn btn-warning fw-bold px-4 py-2 rounded-pill shadow-sm" style="font-size: 15px; pointer-events: none;">
                                👉 Click Here to Claim ₹50,000 👈
                            </button>
                        </div>

                        <!-- Trap Iframe Overlay On Top (Translucent / Invisible) -->
                        <iframe id="modalClickjackFrame" src="clickjack_target.php?mode=<?php echo $is_vuln ? 'vulnerable' : 'secure'; ?>" class="position-absolute top-0 start-0 w-100 h-100" style="z-index: 10; opacity: 0.30; border: none; transition: opacity 0.2s ease;"></iframe>
                    </div>

                    <div class="small text-muted text-center p-2 rounded-2" style="background:#F8F9FA;">
                        <i class="bi bi-info-circle me-1 text-primary"></i> <strong>Realtime Demonstration:</strong> In <strong>0% Stealth</strong> mode, the victim thinks they are clicking the ₹50,000 bonus button, but the click hits the invisible "Permanently Delete Account" button in the embedded iframe!
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bootstrap Bundle JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

    <!-- JavaScript Application & AJAX Engine -->
    <script>
        const CURRENT_MODE = "<?php echo $is_vuln ? 'vulnerable' : 'secure'; ?>";
        const CURRENT_VULN = <?php echo $vuln_id; ?>;

        // 5 Core Vulnerabilities Metadata
        const VULN_META = {
            1: {
                title: "Module 1: SQL Injection (SQLi)",
                subtitle: "Direct string concatenation allows bypassing queries and dumping secret compensation notes.",
                cwe: "CWE-89",
                label: "SQL Injection Attack Payload",
                defaultPayload: "' OR 1=1 #",
                presets: [
                    { name: "Auth Bypass (' OR 1=1 #)", val: "' OR 1=1 #" },
                    { name: "Logic True (' OR '1'='1)", val: "' OR '1'='1" },
                    { name: "Normal Title", val: "Senior Cybersecurity Engineer" }
                ],
                vulnCode: "SELECT * FROM jobs WHERE title = '$input'",
                secCode: "mysqli_prepare + mysqli_stmt_bind_param('s', $input)"
            },
            2: {
                title: "Module 2: Cross-Site Scripting (XSS)",
                subtitle: "Unencoded output reflection allows executing arbitrary JavaScript in the victim browser.",
                cwe: "CWE-79",
                label: "XSS Script Attack Payload",
                defaultPayload: "\x3cscript\x3ealert('XSS: ' + document.domain)\x3c/script\x3e",
                presets: [
                    { name: "Alert Script Tag", val: "\x3cscript\x3ealert('XSS: ' + document.domain)\x3c/script\x3e" },
                    { name: "Document Cookie Alert", val: "\x3cscript\x3ealert('Cookie: ' + document.cookie)\x3c/script\x3e" },
                    { name: "Safe Text", val: "Excellent security candidate." }
                ],
                vulnCode: "echo $user_review; // Raw unencoded output",
                secCode: "echo htmlspecialchars($user_review, ENT_QUOTES, 'UTF-8');"
            },
            3: {
                title: "Module 3: OS Command Injection",
                subtitle: "Unsanitized system shell concatenation allows executing server OS commands in real-time.",
                cwe: "CWE-78",
                label: "Host Target & Command Delimiter",
                defaultPayload: "127.0.0.1 & whoami",
                presets: [
                    { name: "whoami (Realtime User)", val: "127.0.0.1 & whoami" },
                    { name: "Dump lab_private_target.txt (Synthetic)", val: "127.0.0.1 & type lab_private_target.txt" },
                    { name: "hostname Injection", val: "127.0.0.1 & hostname" },
                    { name: "dir lab_files", val: "127.0.0.1 & dir lab_files" },
                    { name: "Normal IP", val: "127.0.0.1" }
                ],
                vulnCode: "shell_exec('ping -n 1 ' . $host);",
                secCode: "regex ^[a-zA-Z0-9.-]+$ + escapeshellarg($host)"
            },
            4: {
                title: "Module 4: Directory / Path Traversal",
                subtitle: "Relative path sequences (../) break out of the documents folder to read restricted files like ../lab_private_target.txt.",
                cwe: "CWE-22",
                label: "Document Path",
                defaultPayload: "../lab_private_target.txt",
                presets: [
                    { name: "Parent lab_private_target.txt (Synthetic)", val: "../lab_private_target.txt" },
                    { name: "Parent Directory (../../lab_private_target.txt)", val: "../../lab_private_target.txt" },
                    { name: "Read database.sql", val: "../database.sql" },
                    { name: "Normal Resume", val: "resume.txt" }
                ],
                vulnCode: "view_document.php?file=../lab_private_target.txt // direct path load",
                secCode: "basename($file) + in_array($safe, $whitelist) // 403 Forbidden on traversal"
            },
            5: {
                title: "Module 5: Clickjacking (UI Redressing)",
                subtitle: "Target page loaded inside transparent iframe to trick user into executing unauthorized actions.",
                cwe: "CWE-1021",
                label: "Target Framing Endpoint",
                defaultPayload: "clickjack_target.php",
                presets: [
                    { name: "Harmful Action: Delete Account & Data", val: "clickjack_target.php" }
                ],
                vulnCode: "// No frame protection headers sent",
                secCode: "header('X-Frame-Options: DENY'); header('CSP: frame-ancestors none');"
            }
        };

        // Initialize UI for current lab
        function initLabUI() {
            const meta = VULN_META[CURRENT_VULN];
            if (!meta) return;

            document.getElementById('labTitleDisplay').textContent = meta.title;
            document.getElementById('labSubtitleDisplay').textContent = meta.subtitle;
            document.getElementById('labCweDisplay').textContent = meta.cwe;
            document.getElementById('labInputLabel').textContent = meta.label;
            document.getElementById('labPayloadInput').value = meta.defaultPayload;
            document.getElementById('labVulnSnippet').textContent = "🔴 Vulnerable: " + meta.vulnCode;
            document.getElementById('labSecSnippet').textContent = "🟢 Secure Mitigated: " + meta.secCode;

            // Render Presets
            const pBox = document.getElementById('labPresetsContainer');
            pBox.innerHTML = '<span class="fw-semibold">Quick Presets: </span>' + 
                meta.presets.map((p, idx) => `<a href="javascript:void(0)" class="text-primary text-decoration-none fw-semibold me-2" onclick="applyPreset(${idx})">${escapeHtml(p.name)}</a>`).join('&bull; ');
        }

        function applyPreset(idx) {
            const meta = VULN_META[CURRENT_VULN];
            if (meta && meta.presets && meta.presets[idx]) {
                document.getElementById('labPayloadInput').value = meta.presets[idx].val;
            }
        }

        function setLabPayload(val) {
            document.getElementById('labPayloadInput').value = val;
        }

        // Execute Lab Test via AJAX
        function runCurrentLabTest() {
            const payload = document.getElementById('labPayloadInput').value;
            const panel = document.getElementById('telemetryPanel');

            panel.innerHTML = `<div class="text-center py-4"><span class="spinner-border spinner-border-sm text-primary me-2"></span><span class="text-muted small">Executing security test via AJAX...</span></div>`;

            const fd = new FormData();
            fd.append('action', 'test_lab');
            fd.append('vuln_id', CURRENT_VULN);
            fd.append('mode', CURRENT_MODE);
            fd.append('payload', payload);

            fetch('api.php', { method: 'POST', body: fd })
                .then(r => r.json())
                .then(res => {
                    renderTelemetryOutput(res);
                })
                .catch(err => {
                    panel.innerHTML = `<div class="alert alert-danger mb-0 small">Execution Error: ${err}</div>`;
                });
        }

        // Render Clean Structured Telemetry
        function renderTelemetryOutput(res) {
            const panel = document.getElementById('telemetryPanel');
            const timeLabel = document.getElementById('telemetryTime');
            timeLabel.textContent = new Date().toLocaleTimeString();

            const statusClass = res.status_type || (res.mode === 'secure' ? 'success' : 'danger');
            const statusIcon = statusClass === 'success' ? 'bi-shield-check' : 'bi-exclamation-triangle-fill';

            let outputHtml = `
                <div class="telemetry-status-box ${statusClass}">
                    <i class="bi ${statusIcon} fs-5"></i>
                    <div>
                        <div class="fw-bold">${escapeHtml(res.exploit_status)}</div>
                        <div class="small opacity-75">Mode: ${res.mode.toUpperCase()} &bull; Module: ${escapeHtml(res.vuln_name || '')} (${escapeHtml(res.cwe || '')})</div>
                    </div>
                </div>
            `;

            // Specific Module Renderers (5 Modules)
            if (res.vuln_id === 1) { // SQLi
                outputHtml += `
                    <div class="code-syntax-box">
                        <div class="text-muted small mb-1">// Executed Database Query</div>
                        <code>${escapeHtml(res.executed_query)}</code>
                    </div>
                `;
                if (res.results && res.results.length > 0) {
                    outputHtml += `
                        <div class="telemetry-table-container">
                            <table class="table table-sm table-hover align-middle mb-0" style="font-size: 12.5px;">
                                <thead class="table-light">
                                    <tr>
                                        <th>ID</th>
                                        <th>Job Title</th>
                                        <th>Company</th>
                                        <th>Salary</th>
                                        <th>Confidential Internal Notes</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${res.results.map(r => `
                                        <tr>
                                            <td>${r.id}</td>
                                            <td class="fw-semibold">${escapeHtml(r.title)}</td>
                                            <td>${escapeHtml(r.company)}</td>
                                            <td class="fw-bold">${escapeHtml(r.salary)}</td>
                                            <td>
                                                ${r.secret_notes ? `<span class="badge bg-danger-subtle text-danger border border-danger-subtle">${escapeHtml(r.secret_notes)}</span>` : '<span class="text-muted">None</span>'}
                                            </td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    `;
                }
            } else if (res.vuln_id === 2) { // XSS
                outputHtml += `
                    <div class="card p-3 mb-3 border bg-white">
                        <div class="small fw-bold text-muted mb-1">DOM Rendered Output</div>
                        <div class="p-2 border rounded bg-light" id="xssOutputPreview"></div>
                    </div>
                    <div class="code-syntax-box">
                        <div class="text-muted small mb-1">// Raw HTML Source in DOM</div>
                        <code>${escapeHtml(res.rendered_html)}</code>
                    </div>
                `;
            } else if (res.vuln_id === 3) { // Command Injection
                outputHtml += `
                    <div class="code-syntax-box">
                        <div class="text-muted small mb-1">// Shell Command</div>
                        <code>${escapeHtml(res.command_executed)}</code>
                    </div>
                    <div class="card p-3 mb-3 border bg-white">
                        <div class="small fw-bold text-muted mb-1">System Execution Output</div>
                        <pre class="mb-0 small" style="font-family: 'JetBrains Mono', monospace;">${escapeHtml(res.output)}</pre>
                    </div>
                `;
            } else if (res.vuln_id === 4) { // Traversal
                outputHtml += `
                    <div class="card p-3 mb-3 border bg-white shadow-sm rounded-3">
                        <div class="d-flex align-items-center justify-content-between mb-2">
                            <span class="small fw-bold text-dark"><i class="bi bi-window me-1 text-primary"></i> Iframe Document Viewer (Realtime In-Page Render):</span>
                            <button type="button" class="btn btn-sm btn-primary fw-bold rounded-pill px-3 shadow-sm" onclick="openResumeViewerModal('resume.txt')">
                                <i class="bi bi-file-earmark-person me-1"></i> Click me to view resume
                            </button>
                        </div>
                        <iframe id="labResumeIframe" src="view_document.php?mode=${res.mode}&file=${encodeURIComponent(res.requested_file)}" style="width: 100%; height: 320px; border: 1px solid #ced4da; border-radius: 8px; background: #fff;"></iframe>
                    </div>
                    <div class="card p-3 mb-3 border bg-white small">
                        <div><strong>Requested File:</strong> <code>${escapeHtml(res.requested_file)}</code></div>
                        ${res.resolved_path ? `<div><strong>Resolved Server Path:</strong> <code>${escapeHtml(res.resolved_path)}</code></div>` : ''}
                    </div>
                    <div class="card p-3 mb-3 border bg-white">
                        <div class="small fw-bold text-muted mb-1">Document Content Stream</div>
                        <pre class="mb-0 small" style="font-family: 'JetBrains Mono', monospace; max-height: 200px; overflow-y: auto;">${escapeHtml(res.content)}</pre>
                    </div>
                `;
            } else if (res.vuln_id === 5) { // Clickjacking with Opacity Slider
                outputHtml += `
                    <div class="card p-3 mb-3 border bg-white">
                        <div class="d-flex align-items-center justify-content-between mb-2">
                            <span class="fw-bold small text-dark"><i class="bi bi-layers text-primary me-1"></i> Interactive UI Redressing Sandbox &amp; Opacity Slider:</span>
                            <div class="d-flex align-items-center gap-2">
                                <span class="small text-muted">Iframe Opacity:</span>
                                <span class="badge bg-primary" id="opacityVal">30%</span>
                            </div>
                        </div>
                        <div class="d-flex align-items-center gap-3 mb-3">
                            <input type="range" class="form-range flex-grow-1" min="0" max="100" value="30" id="clickjackOpacitySlider" oninput="setClickjackOpacity(this.value)">
                            <div class="btn-group btn-group-sm">
                                <button type="button" class="btn btn-outline-secondary" onclick="setClickjackOpacity(0)">0% (Stealth)</button>
                                <button type="button" class="btn btn-outline-secondary" onclick="setClickjackOpacity(30)">30% (Mid)</button>
                                <button type="button" class="btn btn-outline-secondary" onclick="setClickjackOpacity(100)">100% (Revealed)</button>
                            </div>
                        </div>
                        
                        <!-- Redressed Overlay Container -->
                        <div class="position-relative mx-auto rounded-3 overflow-hidden border shadow-sm" style="width: 100%; max-width: 540px; height: 250px; background: #FFF9E6; border: 2px dashed #FFB800 !important;">
                            <!-- Decoy Innocent Layer Behind -->
                            <div class="position-absolute top-0 start-0 w-100 h-100 d-flex flex-column align-items-center justify-content-center p-3 text-center" style="z-index: 1;">
                                <div class="badge bg-warning text-dark mb-2 px-3 py-1 fw-bold fs-6">🎉 SPECIAL CANDIDATE REWARD</div>
                                <h6 class="fw-bold text-dark mb-1">Claim Your ₹50,000 Signing Bonus!</h6>
                                <p class="text-muted small mb-3">Click the button below to credit ₹50,000 directly to Ram Karthik's account.</p>
                                <button type="button" class="btn btn-warning fw-bold px-4 py-2 rounded-pill shadow-sm" style="font-size: 15px; pointer-events: none;">
                                    👉 Click Here to Claim ₹50,000 👈
                                </button>
                            </div>

                            <!-- Trap Iframe Overlay On Top (Translucent / Invisible) -->
                            <iframe id="clickjackSimFrame" src="${escapeHtml(res.frame_url)}" class="position-absolute top-0 start-0 w-100 h-100" style="z-index: 10; opacity: 0.30; border: none; transition: opacity 0.2s ease;"></iframe>
                        </div>
                        <div class="small text-muted mt-2 text-center">
                            <i class="bi bi-info-circle me-1 text-primary"></i> <strong>How to demonstrate:</strong> Drag the slider to <strong>0%</strong> (stealth). When a user clicks the decoy bonus button, they are secretly clicking the transparent "Permanently Delete Account &amp; Erase All Data" button inside the hidden iframe!
                        </div>
                    </div>
                    <div class="card p-3 mb-3 border bg-white small">
                        <div>Frame Protection Headers: <code>${escapeHtml(res.headers_applied)}</code></div>
                    </div>
                `;
            }

            // Defense Explanation Card
            outputHtml += `
                <div class="card p-3 border-0 bg-white shadow-sm small rounded-3">
                    <div class="fw-bold text-dark mb-1"><i class="bi bi-info-circle text-primary me-1"></i> Root Cause &amp; Mitigation Analysis:</div>
                    <div class="text-muted">${escapeHtml(res.defense_info)}</div>
                </div>
            `;

            panel.innerHTML = outputHtml;

            // XSS Live Execution on "Execute Test"
            if (res.vuln_id === 2) {
                const previewEl = document.getElementById('xssOutputPreview');
                if (previewEl) {
                    if (res.mode === 'vulnerable') {
                        previewEl.innerHTML = res.rendered_html;
                        // Fire alert popup in webpage when user clicks Execute Test in Vulnerable Mode
                        setTimeout(() => {
                            try {
                                const raw = res.raw_payload || payload;
                                const match = raw.match(/<script[\s\S]*?>([\s\S]*?)<\/script>/i);
                                if (match && match[1]) {
                                    (new Function(match[1]))();
                                } else if (raw.includes('alert(')) {
                                    eval(raw);
                                } else {
                                    alert('XSS Executed: ' + (raw || document.domain));
                                }
                            } catch (e) {
                                alert('XSS Alert Triggered: ' + document.domain);
                            }
                        }, 120);
                    } else {
                        previewEl.textContent = res.rendered_html;
                    }
                }
            }

            showToast(`${res.vuln_name}: ${res.exploit_status.substring(0, 45)}...`, statusClass === 'success' ? 'bg-success' : 'bg-danger');
        }

        // Toast Helper
        function setClickjackOpacity(val) {
            const frame = document.getElementById('clickjackSimFrame');
            const label = document.getElementById('opacityVal');
            const slider = document.getElementById('clickjackOpacitySlider');
            if (frame) frame.style.opacity = val / 100;
            if (label) label.textContent = val + '%';
            if (slider) slider.value = val;
        }

        function showToast(msg, bgClass = 'bg-dark') {
            const toastEl = document.getElementById('ajaxToast');
            const msgEl = document.getElementById('toastMessage');
            msgEl.textContent = msg;
            toastEl.className = `toast align-items-center text-white ${bgClass} border-0 shadow-lg`;
            const toast = new bootstrap.Toast(toastEl, { delay: 3500 });
            toast.show();
        }

        // ── Job Search — XSS + SQLi integrated demonstration ──
        function setSearchAndRun(val) {
            document.getElementById('ajaxSearchKeyword').value = val;
            ajaxSearchJobs();
        }

        function ajaxSearchJobs() {
            const kw   = document.getElementById('ajaxSearchKeyword').value;
            const loc  = document.getElementById('ajaxSearchLocation').value;
            const type = document.getElementById('ajaxSearchType').value;

            const url = `api.php?action=search_jobs&keyword=${encodeURIComponent(kw)}&location=${encodeURIComponent(loc)}&job_type=${encodeURIComponent(type)}`;

            fetch(url)
                .then(r => r.json())
                .then(data => {
                    if (!data.success) return;
                    renderJobCards(data.jobs);
                    const label = document.getElementById('jobsCountLabel');
                    if (label) label.textContent = `Showing ${data.count} active openings`;

                    // ── XSS Reflection ──
                    const xssVuln   = document.getElementById('xssEchoBanner');
                    const xssSec    = document.getElementById('xssSecureBanner');
                    const xssRaw    = document.getElementById('xssReflectedOutput');
                    const xssEnc    = document.getElementById('xssEncodedOutput');

                    xssVuln.style.display = 'none';
                    xssSec.style.display  = 'none';

                    if (kw.trim()) {
                        if (data.mode === 'vulnerable') {
                            xssVuln.style.display = 'block';
                            // Raw innerHTML reflection — demonstrates XSS
                            xssRaw.innerHTML = kw;
                            // If payload contains <script>, fire it
                            const scriptMatch = kw.match(/<script[\s\S]*?>([\s\S]*?)<\/script>/i);
                            if (scriptMatch && scriptMatch[1]) {
                                setTimeout(() => { try { (new Function(scriptMatch[1]))(); } catch(e) { alert('XSS: ' + e.message); } }, 80);
                            } else if (kw.includes('onerror') || kw.includes('onload')) {
                                // inject the img tag to fire onerror
                                const tmp = document.createElement('div');
                                tmp.innerHTML = kw;
                                document.body.appendChild(tmp);
                                setTimeout(() => document.body.removeChild(tmp), 500);
                            }
                        } else {
                            xssSec.style.display = 'block';
                            // Safe textContent — no execution
                            xssEnc.textContent = kw;
                        }
                    }

                    // ── SQLi Indicator ──
                    const sqliDanger = document.getElementById('sqliDangerBanner');
                    const sqliSafe   = document.getElementById('sqliSecureBanner');
                    sqliDanger.style.display = 'none';
                    sqliSafe.style.display   = 'none';

                    if (kw.trim()) {
                        if (data.mode === 'vulnerable') {
                            sqliDanger.style.display = 'block';
                            document.getElementById('sqliRowCount').textContent = data.count;
                            document.getElementById('sqliQueryDisplay').textContent = (data.exec_query || '').substring(0, 120) + '...';
                        } else {
                            sqliSafe.style.display = 'block';
                        }
                    }
                });
        }

        function quickTagSearch(term) {
            document.getElementById('ajaxSearchKeyword').value = term;
            ajaxSearchJobs();
        }

        // ── Document Viewer — Directory Traversal demonstration with Iframe ──
        function openResumeViewerModal(file = 'resume.txt') {
            new bootstrap.Modal(document.getElementById('docViewerModal')).show();
            loadResumeIframe(file);
        }

        function openDocViewerModal() {
            openResumeViewerModal('resume.txt');
        }

        function loadResumeIframe(filePath) {
            const iframe = document.getElementById('resumeViewerIframe');
            const label = document.getElementById('iframeLoadedFile');
            const status = document.getElementById('docViewerStatus');
            const customInp = document.getElementById('docCustomPath');
            if (customInp) customInp.value = filePath;

            const mode = CURRENT_MODE;
            const url = `view_document.php?mode=${mode}&file=${encodeURIComponent(filePath)}`;
            if (iframe) iframe.src = url;
            if (label) label.textContent = `view_document.php?file=${filePath}`;

            if (status) {
                status.style.display = 'block';
                if (filePath.includes('..') || filePath.includes('lab_private_target.txt')) {
                    if (mode === 'vulnerable') {
                        status.style.cssText = 'display:block;background:#FFF1F0;border:1px solid #FFA39E;color:#CF1322;padding:8px 12px;border-radius:6px;font-size:12.5px;font-weight:700;';
                        status.innerHTML = '🔴 Directory Traversal — EXPLOIT SUCCESSFUL: Parent directory escaped! Synthetic secret fixtures loaded into iframe from lab_private_target.txt.';
                    } else {
                        status.style.cssText = 'display:block;background:#F6FFED;border:1px solid #B7EB8F;color:#389E0D;padding:8px 12px;border-radius:6px;font-size:12.5px;font-weight:700;';
                        status.innerHTML = '🟢 Directory Traversal — BLOCKED: basename() and whitelist prevented directory escaping. 403 Forbidden rendered inside iframe.';
                    }
                } else {
                    status.style.cssText = 'display:block;background:#E6F4FF;border:1px solid #91CAFF;color:#0958D9;padding:8px 12px;border-radius:6px;font-size:12.5px;font-weight:600;';
                    status.innerHTML = '📄 Standard Candidate Document: Loaded safely inside iframe.';
                }
            }
        }

        // Backward compatibility
        function viewDocument(filePath) {
            loadResumeIframe(filePath);
        }

        // ── Clickjacking Sandbox & Modal Controls ──
        function openClickjackModal() {
            new bootstrap.Modal(document.getElementById('clickjackModal')).show();
        }

        function setModalClickjackOpacity(val) {
            const frame = document.getElementById('modalClickjackFrame');
            const label = document.getElementById('modalOpacityVal');
            const slider = document.getElementById('modalClickjackSlider');
            if (frame) frame.style.opacity = val / 100;
            if (label) label.textContent = val + '%';
            if (slider) slider.value = val;
        }

        // In-page Clickjack opacity controller
        function setPageClickjackOpacity(val) {
            const frame = document.getElementById('pageClickjackTargetFrame');
            const label = document.getElementById('pageOpacityVal');
            const slider = document.getElementById('pageOpacitySlider');
            if (frame) frame.style.opacity = val / 100;
            if (label) label.textContent = val + '%';
            if (slider) slider.value = val;
        }

        // Realtime Clickjack postMessage Listener
        window.addEventListener('message', function(event) {
            if (event.data && event.data.type === 'CLICKJACK_TRIGGERED') {
                const time = event.data.timestamp || new Date().toLocaleTimeString();
                showToast(`🚨 REALTIME CLICKJACK HIJACKED! Unauthorized action at ${time}`, 'bg-danger');

                // Update modal alert if open
                const alertBox = document.getElementById('clickjackLiveAlert');
                if (alertBox) {
                    alertBox.style.display = 'block';
                    alertBox.className = 'alert alert-danger py-2 px-3 fw-bold small mb-3 border-danger shadow-sm';
                    alertBox.innerHTML = `💥 <strong>REALTIME HIJACK CONFIRMED (${time}):</strong> The user thought they clicked the decoy button to Pay for Premium Version, but their click was secretly consumed by the transparent iframe to PERMANENTLY DELETE Ram Karthik's account & wipe data [Fabricated Output]!`;
                }

                // Update in-page alert
                const pageAlert = document.getElementById('pageClickjackLiveAlert');
                if (pageAlert) {
                    pageAlert.style.display = 'block';
                    pageAlert.className = 'alert alert-danger py-3 px-4 fw-bold shadow-sm border-danger';
                    pageAlert.innerHTML = `<i class="bi bi-exclamation-octagon-fill text-danger fs-4 me-2 align-middle"></i> <strong>REALTIME CLICKJACK HIJACK EXECUTED (${time}):</strong> The user thought they clicked "Click &amp; Pay ₹499 to Get Premium Version", but their click was secretly consumed by the transparent iframe to PERMANENTLY DELETE Ram Karthik's account &amp; wipe data [Fabricated Output]!`;
                }
            }
        });

        // ── Network Diagnostics — OS Command Injection demonstration ──
        function openPingModal() {
            new bootstrap.Modal(document.getElementById('pingModal')).show();
        }

        function runPingGateway() {
            const host   = document.getElementById('pingHostInput').value;
            const out    = document.getElementById('pingOutput');
            const banner = document.getElementById('pingStatusBanner');
            const cmdEl  = document.getElementById('pingCmdDisplay');
            out.innerHTML = '<span style="color:#58a6ff;">[+] Executing diagnostic command via system shell...</span>';

            const fd = new FormData();
            fd.append('action', 'ping_gateway');
            fd.append('host', host);
            fd.append('mode', CURRENT_MODE);

            fetch('api.php', { method:'POST', body:fd })
                .then(r => r.json())
                .then(data => {
                    cmdEl.textContent = data.cmd || 'N/A';
                    out.textContent   = data.output || '(no output)';

                    banner.style.display = 'block';
                    if (data.mode === 'vulnerable' && data.injected) {
                        banner.style.cssText = 'display:block;background:#FFF1F0;border:1px solid #FFA39E;color:#CF1322;padding:8px 12px;border-radius:6px;';
                        banner.innerHTML = '🔴 Command Injection — EXPLOIT SUCCESSFUL: Additional OS commands executed via & delimiter!';
                        showToast('OS Command Injection: Exploit executed on host server!', 'bg-danger');
                    } else if (data.mode === 'secure') {
                        if ((data.output || '').includes('SECURITY BLOCK')) {
                            banner.style.cssText = 'display:block;background:#F6FFED;border:1px solid #B7EB8F;color:#389E0D;padding:8px 12px;border-radius:6px;';
                            banner.innerHTML = '🟢 Command Injection — BLOCKED: Strict regex + escapeshellarg() rejected injection characters.';
                            showToast('OS Command Injection: Attack safely blocked by regex filter.', 'bg-success');
                        } else {
                            banner.style.cssText = 'display:block;background:#F6FFED;border:1px solid #B7EB8F;color:#389E0D;padding:8px 12px;border-radius:6px;';
                            banner.innerHTML = '🟢 Secure Mode — Valid host accepted. escapeshellarg() applied.';
                        }
                    } else {
                        banner.style.display = 'none';
                    }
                })
                .catch(e => { out.textContent = 'Error: ' + e; });
        }

        function renderJobCards(jobs) {
            const container = document.getElementById('jobCardsContainer');
            if (!container) return;

            if (jobs.length === 0) {
                container.innerHTML = `<div class="col-12 text-center py-5 text-muted">No jobs matching your filter criteria.</div>`;
                return;
            }

            container.innerHTML = jobs.map(j => `
                <div class="col-lg-6">
                    <div class="jp-job-card">
                        <div class="d-flex align-items-start justify-content-between mb-3">
                            <div class="d-flex align-items-center gap-3">
                                <div class="jp-company-logo">
                                    ${j.company.substring(0, 2).toUpperCase()}
                                </div>
                                <div>
                                    <h5 class="fw-bold mb-1 text-dark">${escapeHtml(j.title)}</h5>
                                    <div class="text-muted small">
                                        <span class="fw-semibold text-primary">${escapeHtml(j.company)}</span>
                                        &bull; <i class="bi bi-geo-alt"></i> ${escapeHtml(j.location)}
                                    </div>
                                </div>
                            </div>
                            <span class="jp-tag-pill fulltime">${escapeHtml(j.job_type)}</span>
                        </div>

                        <p class="text-muted small mb-4 flex-grow-1" style="line-height: 1.6;">
                            ${escapeHtml(j.description)}
                        </p>

                        <div class="d-flex align-items-center justify-content-between pt-3 border-top mt-auto">
                            <div>
                                <div class="text-muted" style="font-size: 11px;">Salary Package</div>
                                <div class="jp-salary-badge">${escapeHtml(j.salary)}</div>
                            </div>
                            <button type="button" class="btn btn-outline-primary fw-bold px-3 py-2 rounded-pill" data-title="${escapeHtml(j.title)}" data-company="${escapeHtml(j.company)}" onclick="openApplyModalFromBtn(this)">
                                <i class="bi bi-send-fill me-1"></i> Apply Now
                            </button>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        // Job Application
        function openApplyModalFromBtn(btn) {
            const title = btn.getAttribute('data-title') || '';
            const company = btn.getAttribute('data-company') || '';
            openApplyModal(title, company);
        }

        function openApplyModal(title, company) {
            document.getElementById('applyJobTitle').value = title;
            document.getElementById('applyJobCompany').value = company;
            document.getElementById('modalDisplayTitle').textContent = title;
            document.getElementById('modalDisplayCompany').textContent = company;

            const modal = new bootstrap.Modal(document.getElementById('applyModal'));
            modal.show();
        }

        function submitJobApplication(e) {
            e.preventDefault();
            const form = document.getElementById('formApplyJob');
            const formData = new FormData(form);
            formData.append('action', 'apply_job');

            const submitBtn = document.getElementById('btnSubmitApply');
            submitBtn.disabled = true;
            submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span> Submitting...`;

            fetch('api.php', { method: 'POST', body: formData })
                .then(r => r.json())
                .then(data => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = `<i class="bi bi-send-fill me-1"></i> Submit Application`;

                    if (data.success) {
                        showToast(data.message, 'bg-success');
                        const modalEl = document.getElementById('applyModal');
                        bootstrap.Modal.getInstance(modalEl).hide();

                        const badge = document.getElementById('appBadge');
                        if (badge) {
                            badge.textContent = parseInt(badge.textContent || '0') + 1;
                        }
                    } else {
                        showToast(data.error || 'Failed to submit application', 'bg-danger');
                    }
                });
        }

        function ajaxWithdrawApp(appId) {
            if (!confirm('Withdraw this application?')) return;
            const fd = new FormData();
            fd.append('action', 'withdraw_app');
            fd.append('id', appId);

            fetch('api.php', { method: 'POST', body: fd })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        showToast(data.message, 'bg-success');
                        const row = document.getElementById(`appRow-${appId}`);
                        if (row) row.remove();
                        const badge = document.getElementById('appBadge');
                        if (badge) badge.textContent = Math.max(0, parseInt(badge.textContent || '1') - 1);
                    }
                });
        }

        // Job CRUD
        function submitAddJob(e) {
            e.preventDefault();
            const form = document.getElementById('formAddJob');
            const fd = new FormData(form);
            fd.append('action', 'add_job');

            fetch('api.php', { method: 'POST', body: fd })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        showToast(data.message, 'bg-success');
                        bootstrap.Modal.getInstance(document.getElementById('addJobModal')).hide();
                        setTimeout(() => location.reload(), 800);
                    }
                });
        }

        function openEditJobModalFromBtn(btn) {
            const raw = btn.getAttribute('data-job');
            if (raw) {
                try {
                    openEditJobModal(JSON.parse(raw));
                } catch(e) { console.error('Error parsing job JSON:', e); }
            }
        }

        function openEditJobModal(job) {
            document.getElementById('editJobId').value = job.id;
            document.getElementById('editJobTitle').value = job.title;
            document.getElementById('editJobCompany').value = job.company;
            document.getElementById('editJobLocation').value = job.location;
            document.getElementById('editJobSalary').value = job.salary;
            document.getElementById('editJobType').value = job.job_type;
            document.getElementById('editJobDepartment').value = job.department;
            document.getElementById('editJobDescription').value = job.description;
            document.getElementById('editJobNotes').value = job.secret_notes;

            new bootstrap.Modal(document.getElementById('editJobModal')).show();
        }

        function submitEditJob(e) {
            e.preventDefault();
            const form = document.getElementById('formEditJob');
            const fd = new FormData(form);
            fd.append('action', 'edit_job');

            fetch('api.php', { method: 'POST', body: fd })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        showToast(data.message, 'bg-success');
                        bootstrap.Modal.getInstance(document.getElementById('editJobModal')).hide();
                        setTimeout(() => location.reload(), 800);
                    }
                });
        }

        function ajaxDeleteJob(jobId) {
            if (!confirm('Delete this job post?')) return;
            const fd = new FormData();
            fd.append('action', 'delete_job');
            fd.append('id', jobId);

            fetch('api.php', { method: 'POST', body: fd })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        showToast(data.message, 'bg-success');
                        const row = document.getElementById(`dbJobRow-${jobId}`);
                        if (row) row.remove();
                    }
                });
        }

        function ajaxReseedDatabase() {
            if (!confirm('Reset and re-seed all tables with clean records?')) return;
            const fd = new FormData();
            fd.append('action', 'reseed_db');

            fetch('api.php', { method: 'POST', body: fd })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        showToast(data.message, 'bg-success');
                        setTimeout(() => location.reload(), 1000);
                    }
                });
        }

        function escapeHtml(text) {
            if (!text) return '';
            return String(text).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
        }
        function escapeAttr(text) {
            if (!text) return '';
            return String(text).replace(/'/g, "\\'").replace(/"/g, "&quot;");
        }

        // Initialize lab on page load if active
        if (<?php echo $tab === 'lab' ? 'true' : 'false'; ?>) {
            initLabUI();
        }
    </script>
</body>
</html>
