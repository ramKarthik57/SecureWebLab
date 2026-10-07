<?php
// ====================================================================
// SecureJobLab: Clickjacking Target Endpoint (CWE-1021)
// Harmful / Destructive Action Simulation: Permanent Account Deletion
// Candidate Persona: Ram Karthik (Candidate & AppSec Specialist)
// ====================================================================

$mode = $_GET['mode'] ?? 'vulnerable';
$is_vulnerable = ($mode !== 'secure');

if (!$is_vulnerable) {
    // 🟢 SECURE MITIGATION: Strict framing prevention headers
    header("X-Frame-Options: DENY");
    header("Content-Security-Policy: frame-ancestors 'none'");
}

$action_triggered = false;
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['confirm_delete_account'])) {
    $action_triggered = true;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Critical Security Action &bull; Delete Account</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <style>
        * { box-sizing: border-box; }
        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: #FFF2F0;
        }
        .target-container {
            position: relative;
            width: 100%;
            height: 100%;
            padding: 22px 24px 0 24px;
            text-align: center;
        }
        .btn-destructive {
            background-color: #E02424;
            color: #ffffff;
            font-weight: 700;
            border: none;
            border-radius: 50px;
            font-size: 15px;
            cursor: pointer;
            box-shadow: 0 3px 8px rgba(224, 36, 36, 0.35);
            transition: all 0.2s ease;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .btn-destructive:hover {
            background-color: #BC1C1C;
            color: #ffffff;
        }
    </style>
</head>
<body>
    <div class="target-container">
        <div class="d-flex align-items-center justify-content-between mb-2">
            <span class="badge bg-danger px-2 py-1"><i class="bi bi-exclamation-octagon-fill me-1"></i> DANGER ZONE: IRREVERSIBLE</span>
            <span class="badge bg-dark">ID: #RK-99201</span>
        </div>
        <h6 class="fw-bold mb-1 text-danger d-flex align-items-center justify-content-center gap-1">
            <i class="bi bi-trash3-fill"></i> Permanently Delete Account &amp; Wipe Data
        </h6>
        <p class="text-muted small mb-0" style="line-height: 1.35; font-size: 12px;">
            Target: <strong>Ram Karthik</strong> (<code>ram.karthik@securejob.io</code>)<br>
            <span class="text-danger fw-semibold">WARNING:</span> This action permanently revokes all applications &amp; wipes all profile records!
        </p>

        <?php if ($action_triggered): ?>
            <div class="alert alert-danger py-1 px-2 small fw-bold mt-1 mb-0 border-danger shadow-sm" style="font-size: 11px;">
                💥 Permanently Delete Account &amp; Wipe Data [Fabricated Output]
            </div>
            <script>
                try {
                    window.parent.postMessage({
                        type: 'CLICKJACK_TRIGGERED',
                        mode: '<?php echo $mode; ?>',
                        victim: 'Ram Karthik (ram.karthik@securejob.io)',
                        action: 'Permanently Delete Account & Wipe Data [Fabricated Output]',
                        timestamp: new Date().toLocaleTimeString()
                    }, '*');
                } catch(e) {}
            </script>
        <?php endif; ?>

        <!-- Target Button: Positioned on the EXACT same coordinates as decoy button -->
        <form method="POST" action="" style="position: absolute; bottom: 25px; left: 50%; transform: translateX(-50%); width: 440px; max-width: 90%; height: 46px; margin: 0; padding: 0;">
            <input type="hidden" name="confirm_delete_account" value="1">
            <button type="submit" class="btn btn-destructive" id="dangerButton">
                ⚠️ Permanently Delete Account &amp; Wipe Data
            </button>
        </form>
    </div>
</body>
</html>
