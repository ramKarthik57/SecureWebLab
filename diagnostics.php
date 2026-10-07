<?php
// ====================================================================
// SecureJobLab: Network Gateway Diagnostics (CWE-78)
// OS Command Injection URL Demonstration Page
// Course: 20CYS403 Web Application Security
// Persona: Ram Karthik (Candidate & AppSec Specialist)
// ====================================================================

session_start();

$raw_query = $_SERVER['QUERY_STRING'] ?? '';

// Mode Switcher (via query parameter or session)
if (preg_match('/(?:^|&)mode=([^&]+)/i', $raw_query, $m_mode)) {
    $_SESSION['appsec_mode'] = (urldecode($m_mode[1]) === 'secure') ? 'secure' : 'vulnerable';
}
$mode = $_SESSION['appsec_mode'] ?? 'vulnerable';
$is_vuln = ($mode !== 'secure');

// Extract host from raw query string so unencoded '&', ';', '|' in browser URL bar work seamlessly
$host = '';
if (preg_match('/(?:^|&)host=([^#]*)/', $raw_query, $m_host)) {
    $raw_host = $m_host[1];
    // Strip trailing &mode=... if present
    $raw_host = preg_replace('/&mode=[^&]*/i', '', $raw_host);
    $host = urldecode($raw_host);
} else {
    $host = $_GET['host'] ?? '127.0.0.1';
}
if (empty($host)) {
    $host = '127.0.0.1';
}

$output = '';
$executed_cmd = '';
$injected = false;
$blocked = false;
$block_reason = '';

// Detect if command chaining character is present
if (strpos($host, '&') !== false || strpos($host, '|') !== false || strpos($host, ';') !== false || strpos($host, '`') !== false) {
    $injected = true;
}

if ($is_vuln) {
    // ----------------------------------------------------------------
    // 🔴 INTENTIONALLY VULNERABLE TRAINING IMPLEMENTATION (CWE-78)
    // Direct concatenation of user-supplied $_GET['host'] into system shell.
    // An evaluator can append "& whoami" or "& type ..\credentials.txt"
    // to execute arbitrary server commands directly from the URL bar!
    // ----------------------------------------------------------------
    $executed_cmd = "ping -n 1 " . $host;
    $output = @shell_exec($executed_cmd . " 2>&1");
    if (!$output) {
        $output = "(No output or command blocked by host policy)";
    }
} else {
    // ----------------------------------------------------------------
    // 🟢 SECURE MITIGATED IMPLEMENTATION (CWE-78 Mitigated)
    // 1. Strict regex whitelist allowing only clean hostnames and IP addresses
    // 2. escapeshellarg() wraps argument in protective quotes
    // ----------------------------------------------------------------
    if (preg_match('/^[a-zA-Z0-9.\-]+$/', $host)) {
        $safe_host = escapeshellarg($host);
        $executed_cmd = "ping -n 1 " . $safe_host;
        $output = @shell_exec($executed_cmd . " 2>&1");
    } else {
        $blocked = true;
        $executed_cmd = "[BLOCKED BY REGEX WHITELIST]";
        $block_reason = "SECURITY INTERCEPTION: Injected command delimiters (&, |, ;, `, space) detected. Only alphanumeric, dots, and hyphens permitted.";
        $output = "================================================================================\n" .
                  "SECURITY BLOCK — COMMAND INJECTION NEUTRALIZED (CWE-78 MITIGATED)\n" .
                  "================================================================================\n\n" .
                  "Input parameter : " . htmlspecialchars($host) . "\n" .
                  "Filter rule     : Regex Whitelist /^[a-zA-Z0-9.\-]+$/\n" .
                  "Escaping        : escapeshellarg() enforced\n" .
                  "Result          : Command rejected before reaching operating system shell.";
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Network Diagnostics &bull; SecureJobLab (CWE-78 Demo)</title>
    
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
            --jp-dark: #18191C;
            --jp-body: #5E6670;
            --jp-border: #E4E5E8;
        }
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #F8F9FA;
            color: var(--jp-dark);
            margin: 0;
            padding: 0;
        }
        .navbar-custom {
            background: #ffffff;
            border-bottom: 1px solid var(--jp-border);
            padding: 12px 24px;
        }
        .url-callout-box {
            background: #FFFBE6;
            border: 2px dashed #FFE58F;
            border-radius: 12px;
            padding: 18px 24px;
            margin-bottom: 24px;
        }
        .code-url-badge {
            background: #ffffff;
            border: 1px solid #D9D9D9;
            padding: 4px 10px;
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13.5px;
            color: #D4380D;
            font-weight: 600;
        }
        .terminal-viewer {
            background: #0D1117;
            color: #58A6FF;
            border-radius: 12px;
            padding: 20px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 13.5px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
            border: 1px solid #30363D;
            min-height: 380px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        }
        .payload-btn {
            font-size: 12px;
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 50px;
            text-decoration: none;
            transition: all 0.2s;
            display: inline-block;
        }
    </style>
</head>
<body>

    <!-- Header Navigation -->
    <header class="navbar-custom d-flex align-items-center justify-content-between">
        <div class="d-flex align-items-center gap-3">
            <a href="index.php" class="text-decoration-none d-flex align-items-center gap-2">
                <i class="bi bi-briefcase-fill fs-4 text-primary"></i>
                <span class="fs-5 fw-bold text-dark">Jobpilot</span>
                <span class="badge bg-light text-primary border">SecureJobLab</span>
            </a>
            <span class="text-muted small">|</span>
            <span class="fw-semibold small text-muted"><i class="bi bi-terminal-fill text-danger me-1"></i>Cloud Gateway Network Diagnostics</span>
        </div>

        <div class="d-flex align-items-center gap-2">
            <!-- Mode Switcher -->
            <?php if ($is_vuln): ?>
                <a href="diagnostics.php?host=<?php echo urlencode($host); ?>&mode=secure" class="btn btn-sm btn-outline-danger fw-bold rounded-pill px-3">
                    <i class="bi bi-shield-slash me-1"></i> VULNERABLE MODE (Click for Secure)
                </a>
            <?php else: ?>
                <a href="diagnostics.php?host=<?php echo urlencode($host); ?>&mode=vulnerable" class="btn btn-sm btn-success fw-bold rounded-pill px-3">
                    <i class="bi bi-shield-check me-1"></i> SECURE MODE (Click for Vulnerable)
                </a>
            <?php endif; ?>

            <a href="index.php?tab=jobs" class="btn btn-sm btn-outline-secondary rounded-pill px-3">
                <i class="bi bi-arrow-left me-1"></i> Back to Jobs Portal
            </a>
        </div>
    </header>

    <main class="container py-4">
        <!-- Interactive URL Modification Guide Box -->
        <div class="url-callout-box">
            <div class="d-flex align-items-start justify-content-between mb-2">
                <div class="d-flex align-items-center gap-2">
                    <i class="bi bi-terminal fs-4 text-danger"></i>
                    <h5 class="fw-bold mb-0 text-dark">OS Command Injection (CWE-78) — URL Parameter Demonstration</h5>
                </div>
                <span class="badge bg-dark">Course: 20CYS403</span>
            </div>
            <p class="text-muted small mb-3" style="line-height: 1.6;">
                The diagnostic target is read directly from the <strong><code>?host=</code></strong> parameter in your browser's address bar.
                You can <strong>physically edit the browser URL</strong> by appending command delimiters (<code>&amp;</code>, <code>|</code>, <code>;</code>) to chain arbitrary OS commands on the server host!
            </p>

            <!-- URL Input Form (Submits via GET so URL bar is automatically updated) -->
            <form method="GET" action="diagnostics.php" class="row g-2 align-items-center mb-3">
                <div class="col-auto">
                    <label class="col-form-label small fw-bold">Address Bar Parameter:</label>
                </div>
                <div class="col-md-6">
                    <div class="input-group">
                        <span class="input-group-text font-monospace bg-light">?host=</span>
                        <input type="text" name="host" class="form-control font-monospace" value="<?php echo htmlspecialchars($host); ?>" placeholder="127.0.0.1 & whoami">
                        <button type="submit" class="btn btn-primary fw-bold">
                            <i class="bi bi-play-fill me-1"></i> Run Diagnostic
                        </button>
                    </div>
                </div>
                <div class="col-auto">
                    <span class="small text-muted">(Or type directly into browser address bar and press Enter)</span>
                </div>
            </form>

            <!-- Quick 1-Click URL Mutators -->
            <div class="d-flex align-items-center gap-2 flex-wrap">
                <span class="small text-muted fw-bold">Test URLs:</span>
                <a href="diagnostics.php?host=127.0.0.1" class="payload-btn btn btn-sm btn-outline-primary">
                    ?host=127.0.0.1 (Normal)
                </a>
                <a href="diagnostics.php?host=127.0.0.1%20%26%20whoami" class="payload-btn btn btn-sm <?php echo $is_vuln ? 'btn-danger text-white' : 'btn-outline-danger'; ?>">
                    <i class="bi bi-person-fill"></i> ?host=127.0.0.1 &amp; whoami
                </a>
                <a href="diagnostics.php?host=127.0.0.1%20%26%20type%20credentials.txt" class="payload-btn btn btn-sm <?php echo $is_vuln ? 'btn-danger text-white' : 'btn-outline-danger'; ?>">
                    <i class="bi bi-key-fill"></i> ?host=127.0.0.1 &amp; type credentials.txt
                </a>
                <a href="diagnostics.php?host=127.0.0.1%20%26%20hostname" class="payload-btn btn btn-sm btn-outline-secondary">
                    <i class="bi bi-hdd"></i> ?host=127.0.0.1 &amp; hostname
                </a>
                <a href="diagnostics.php?host=127.0.0.1%20%26%20dir%20lab_files" class="payload-btn btn btn-sm btn-outline-secondary">
                    <i class="bi bi-folder"></i> ?host=127.0.0.1 &amp; dir lab_files
                </a>
            </div>
        </div>

        <!-- Exploit / Defense Status Banner -->
        <?php if ($is_vuln && $injected): ?>
            <div class="alert alert-danger shadow-sm border-danger d-flex align-items-center gap-3 mb-4 rounded-3 p-3">
                <i class="bi bi-exclamation-triangle-fill fs-3 text-danger"></i>
                <div>
                    <h6 class="fw-bold mb-1 text-danger">🔴 OS COMMAND INJECTION EXPLOIT SUCCESSFUL (CWE-78)</h6>
                    <div class="small">The server executed arbitrary host commands via the <strong><code>&amp;</code></strong> delimiter concatenated directly into <code>shell_exec()</code>!</div>
                </div>
            </div>
        <?php elseif (!$is_vuln && $blocked): ?>
            <div class="alert alert-success shadow-sm border-success d-flex align-items-center gap-3 mb-4 rounded-3 p-3">
                <i class="bi bi-shield-check fs-3 text-success"></i>
                <div>
                    <h6 class="fw-bold mb-1 text-success">🟢 OS COMMAND INJECTION BLOCKED &amp; MITIGATED (CWE-78)</h6>
                    <div class="small">Defense Active: Input validation regex <code>/^[a-zA-Z0-9.\-]+$/</code> and <code>escapeshellarg()</code> intercepted forbidden characters before shell execution!</div>
                </div>
            </div>
        <?php elseif ($is_vuln): ?>
            <div class="alert alert-warning shadow-sm border-warning d-flex align-items-center gap-3 mb-4 rounded-3 p-3">
                <i class="bi bi-info-circle-fill fs-3 text-warning"></i>
                <div>
                    <h6 class="fw-bold mb-1 text-dark">🔴 VULNERABLE MODE ACTIVE — Ready for Command Injection Demonstration</h6>
                    <div class="small">Currently pinging clean host. Append <code>&amp; whoami</code> to the <code>?host=</code> parameter in the URL bar to demonstrate exploit.</div>
                </div>
            </div>
        <?php else: ?>
            <div class="alert alert-success shadow-sm border-success d-flex align-items-center gap-3 mb-4 rounded-3 p-3">
                <i class="bi bi-shield-check fs-3 text-success"></i>
                <div>
                    <h6 class="fw-bold mb-1 text-success">🟢 SECURE MODE ACTIVE — Whitelist &amp; escapeshellarg() Enforced</h6>
                    <div class="small">Strict regex filter prevents command chaining characters (&amp;, |, ;, `, space).</div>
                </div>
            </div>
        <?php endif; ?>

        <!-- Server Metadata Bar -->
        <div class="card border-0 shadow-sm p-3 mb-3 bg-white rounded-3">
            <div class="row g-2 small">
                <div class="col-md-4">
                    <span class="text-muted fw-semibold">URL Parameter Input:</span>
                    <div class="fw-bold text-dark font-monospace"><?php echo htmlspecialchars($host); ?></div>
                </div>
                <div class="col-md-5">
                    <span class="text-muted fw-semibold">Constructed Shell Command:</span>
                    <div class="text-muted font-monospace"><?php echo htmlspecialchars($executed_cmd); ?></div>
                </div>
                <div class="col-md-3 text-md-end">
                    <span class="text-muted fw-semibold">Security Enforcement:</span>
                    <div>
                        <?php if ($is_vuln): ?>
                            <span class="badge bg-danger-subtle text-danger border border-danger-subtle fw-bold">Unsanitized shell_exec</span>
                        <?php else: ?>
                            <span class="badge bg-success-subtle text-success border border-success-subtle fw-bold">Regex Whitelist + escapeshellarg</span>
                        <?php endif; ?>
                    </div>
                </div>
            </div>
        </div>

        <!-- Terminal Output Display -->
        <div class="terminal-viewer">
<span style="color:#8b949e;">$ <?php echo htmlspecialchars($executed_cmd); ?></span>
<?php echo "\n" . htmlspecialchars($output); ?>
        </div>
    </main>

</body>
</html>
