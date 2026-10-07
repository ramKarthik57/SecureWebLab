<?php
// ====================================================================
// SecureJobLab: Resume & Document Viewer Endpoint (CWE-22)
// Path Traversal URL Demonstration Page (Canonical Implementation)
// Course: 20CYS403 Web Application Security
// Persona: Ram Karthik (Candidate & AppSec Specialist)
// ====================================================================

require_once __DIR__ . '/config.php';
ensure_session_started();

// Mode Switcher (via query parameter or session)
if (isset($_GET['mode'])) {
    $_SESSION['appsec_mode'] = ($_GET['mode'] === 'secure') ? 'secure' : 'vulnerable';
}
$mode = $_SESSION['appsec_mode'] ?? 'vulnerable';
$is_vuln = ($mode !== 'secure');

// Target file from URL parameter
$file = $_GET['file'] ?? 'resume.txt';

$content = '';
$resolved_path = '';
$traversal_detected = false;
$access_blocked = false;
$block_reason = '';

if ($is_vuln) {
    // ----------------------------------------------------------------
    // 🔴 INTENTIONALLY VULNERABLE TRAINING IMPLEMENTATION (CWE-22)
    // Direct concatenation of user-controlled $_GET['file'] parameter into file path.
    // An evaluator can modify the URL to:
    // view_resume.php?file=../lab_private_target.txt
    // to escape the designated 'lab_files/' directory and read the root fixture!
    // ----------------------------------------------------------------
    $base_dir = __DIR__ . '/lab_files/';
    $target_path = $base_dir . $file;
    $resolved_path = @realpath($target_path) ?: $target_path;

    if (strpos($file, '..') !== false || strpos($file, '/') !== false || strpos($file, '\\') !== false) {
        $traversal_detected = true;
    }

    if (file_exists($target_path)) {
        $content = @file_get_contents($target_path);
    } else {
        $content = "ERROR 404: File not found at resolved server path:\n" . $target_path;
    }
} else {
    // ----------------------------------------------------------------
    // 🟢 SECURE MITIGATED IMPLEMENTATION (CWE-22 Mitigated)
    // 1. basename() extraction strips all directory traversal tokens (../, ..\)
    // 2. Strict whitelist check verifies against authorized documents
    // 3. realpath boundary check ensures file never escapes lab_files/
    // ----------------------------------------------------------------
    $safe_file = basename($file);
    $whitelist = ['resume.txt', 'coverletter.txt', 'certificate.txt', 'skills.txt', 'assignment.txt'];
    $base_dir  = realpath(__DIR__ . '/lab_files');
    $target_path = $base_dir . DIRECTORY_SEPARATOR . $safe_file;
    $real_target = @realpath($target_path);

    if (strpos($file, '..') !== false) {
        $traversal_detected = true;
    }

    if (in_array($safe_file, $whitelist, true) && $real_target && strpos($real_target, $base_dir) === 0 && file_exists($real_target)) {
        $content = @file_get_contents($real_target);
        $resolved_path = $real_target;
    } else {
        $access_blocked = true;
        $block_reason = "ACCESS DENIED (CWE-22 Mitigated): The requested file '" . htmlspecialchars($file) . "' is not permitted. Strict basename() extraction sanitized it to '" . htmlspecialchars($safe_file) . "', and whitelist validation rejected it.";
        $resolved_path = $base_dir . DIRECTORY_SEPARATOR . '[ACCESS_DENIED]';
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Candidate Resume Viewer &bull; SecureJobLab (CWE-22 Demo)</title>
    
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
            color: #C9D1D9;
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
            <span class="fw-semibold small text-muted"><i class="bi bi-file-earmark-person text-primary me-1"></i>Document &amp; Resume Viewer</span>
        </div>

        <div class="d-flex align-items-center gap-2">
            <!-- Mode Switcher -->
            <?php if ($is_vuln): ?>
                <a href="view_resume.php?file=<?php echo urlencode($file); ?>&mode=secure" class="btn btn-sm btn-outline-danger fw-bold rounded-pill px-3">
                    <i class="bi bi-shield-slash me-1"></i> VULNERABLE MODE (Click for Secure)
                </a>
            <?php else: ?>
                <a href="view_resume.php?file=<?php echo urlencode($file); ?>&mode=vulnerable" class="btn btn-sm btn-success fw-bold rounded-pill px-3">
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
                    <i class="bi bi-browser-chrome fs-4 text-warning"></i>
                    <h5 class="fw-bold mb-0 text-dark">Directory / Path Traversal (CWE-22) — URL Parameter Demonstration</h5>
                </div>
                <span class="badge bg-dark">Course: 20CYS403</span>
            </div>
            <p class="text-muted small mb-3" style="line-height: 1.6;">
                The file name is retrieved directly from the <strong><code>?file=</code></strong> parameter in your browser's address bar.
                You can <strong>physically edit the browser URL</strong> to perform Path Traversal, escaping <code>lab_files/</code> to access restricted files in the parent directory!
            </p>

            <div class="d-flex align-items-center gap-2 flex-wrap mb-3">
                <span class="small fw-bold text-dark">Current Browser URL Parameter:</span>
                <span class="code-url-badge">?file=<?php echo htmlspecialchars($file); ?></span>
            </div>

            <!-- Quick 1-Click URL Mutators -->
            <div class="d-flex align-items-center gap-2 flex-wrap">
                <span class="small text-muted fw-bold">Test URLs:</span>
                <a href="view_resume.php?file=resume.txt" class="payload-btn btn btn-sm btn-outline-primary">
                    <i class="bi bi-file-earmark-person"></i> ?file=resume.txt (Normal)
                </a>
                <a href="view_resume.php?file=../lab_private_target.txt" class="payload-btn btn btn-sm <?php echo $is_vuln ? 'btn-danger text-white' : 'btn-outline-danger'; ?>">
                    <i class="bi bi-key-fill"></i> ?file=../lab_private_target.txt (Synthetic Target)
                </a>
                <a href="view_resume.php?file=../../lab_private_target.txt" class="payload-btn btn btn-sm <?php echo $is_vuln ? 'btn-danger text-white' : 'btn-outline-danger'; ?>">
                    <i class="bi bi-hdd-network"></i> ?file=../../lab_private_target.txt (Deep Traversal)
                </a>
                <a href="view_resume.php?file=../database.sql" class="payload-btn btn btn-sm btn-outline-secondary">
                    <i class="bi bi-database"></i> ?file=../database.sql
                </a>
                <a href="view_resume.php?file=coverletter.txt" class="payload-btn btn btn-sm btn-outline-secondary">
                    <i class="bi bi-file-text"></i> ?file=coverletter.txt
                </a>
            </div>
        </div>

        <!-- Exploit / Defense Status Banner -->
        <?php if ($is_vuln && $traversal_detected): ?>
            <div class="alert alert-danger shadow-sm border-danger d-flex align-items-center gap-3 mb-4 rounded-3 p-3">
                <i class="bi bi-exclamation-triangle-fill fs-3 text-danger"></i>
                <div>
                    <h6 class="fw-bold mb-1 text-danger">🔴 PATH TRAVERSAL EXPLOIT SUCCESSFUL (CWE-22)</h6>
                    <div class="small">The server traversed out of <code>lab_files/</code> and read <strong><code><?php echo htmlspecialchars($file); ?></code></strong> directly via unsanitized URL parameter concatenation!</div>
                </div>
            </div>
        <?php elseif (!$is_vuln && $access_blocked): ?>
            <div class="alert alert-success shadow-sm border-success d-flex align-items-center gap-3 mb-4 rounded-3 p-3">
                <i class="bi bi-shield-check fs-3 text-success"></i>
                <div>
                    <h6 class="fw-bold mb-1 text-success">🟢 PATH TRAVERSAL BLOCKED &amp; MITIGATED (CWE-22)</h6>
                    <div class="small">Defense Active: <code>basename()</code> stripped directory tokens and whitelist validation rejected <strong><code><?php echo htmlspecialchars($file); ?></code></strong>!</div>
                </div>
            </div>
        <?php elseif ($is_vuln): ?>
            <div class="alert alert-warning shadow-sm border-warning d-flex align-items-center gap-3 mb-4 rounded-3 p-3">
                <i class="bi bi-info-circle-fill fs-3 text-warning"></i>
                <div>
                    <h6 class="fw-bold mb-1 text-dark">🔴 VULNERABLE MODE ACTIVE — Ready for Traversal Demonstration</h6>
                    <div class="small">Currently viewing standard file. Change <code>?file=resume.txt</code> to <code>?file=../lab_private_target.txt</code> in the address bar to exploit.</div>
                </div>
            </div>
        <?php else: ?>
            <div class="alert alert-success shadow-sm border-success d-flex align-items-center gap-3 mb-4 rounded-3 p-3">
                <i class="bi bi-shield-check fs-3 text-success"></i>
                <div>
                    <h6 class="fw-bold mb-1 text-success">🟢 SECURE MODE ACTIVE — Whitelist &amp; basename() Enforced</h6>
                    <div class="small">Only authorized candidate files (resume.txt, coverletter.txt, certificate.txt, skills.txt) can be opened.</div>
                </div>
            </div>
        <?php endif; ?>

        <!-- Server Metadata Bar -->
        <div class="card border-0 shadow-sm p-3 mb-3 bg-white rounded-3">
            <div class="row g-2 small">
                <div class="col-md-4">
                    <span class="text-muted fw-semibold">Requested File (URL Parameter):</span>
                    <div class="fw-bold text-dark font-monospace"><?php echo htmlspecialchars($file); ?></div>
                </div>
                <div class="col-md-5">
                    <span class="text-muted fw-semibold">Resolved Server Path:</span>
                    <div class="text-muted font-monospace"><?php echo htmlspecialchars($resolved_path); ?></div>
                </div>
                <div class="col-md-3 text-md-end">
                    <span class="text-muted fw-semibold">Security Enforcement:</span>
                    <div>
                        <?php if ($is_vuln): ?>
                            <span class="badge bg-danger-subtle text-danger border border-danger-subtle fw-bold">Unsanitized file_get_contents</span>
                        <?php else: ?>
                            <span class="badge bg-success-subtle text-success border border-success-subtle fw-bold">basename() + Whitelist Checked</span>
                        <?php endif; ?>
                    </div>
                </div>
            </div>
        </div>

        <!-- File Content Display -->
        <div class="terminal-viewer">
<?php
if ($access_blocked) {
    echo "================================================================================\n";
    echo "403 FORBIDDEN — SECURITY INTERCEPTION (CWE-22 MITIGATED)\n";
    echo "================================================================================\n\n";
    echo $block_reason . "\n\n";
    echo "Enforced Whitelist: ['resume.txt', 'coverletter.txt', 'certificate.txt', 'skills.txt']\n";
    echo "Storage Sandbox   : lab_files/ (Relative escaping strictly prohibited)\n";
} else {
    echo htmlspecialchars($content);
}
?>
        </div>
    </main>

</body>
</html>
