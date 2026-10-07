<?php
// ====================================================================
// SecureJobLab: Centralized Configuration Engine
// Course: 20CYS403 Web Application Security
// Author: Ram Karthik G (AppSec Specialist)
// ====================================================================

// Prevent direct execution outside entrypoints
if (!defined('SECUREJOBLAB_INIT')) {
    define('SECUREJOBLAB_INIT', true);
}

// --------------------------------------------------------------------
// 1. Database Credentials (Configurable via Environment or Defaults)
// --------------------------------------------------------------------
define('DB_HOST', getenv('DB_HOST') ?: 'localhost');
define('DB_USER', getenv('DB_USER') ?: 'root');
define('DB_PASS', getenv('DB_PASS') !== false ? getenv('DB_PASS') : '');
define('DB_NAME', getenv('DB_NAME') ?: 'securejoblab');
define('DB_PORT', (int)(getenv('DB_PORT') ?: 3306));

// --------------------------------------------------------------------
// 2. Application Identity & Academic Context
// --------------------------------------------------------------------
define('APP_NAME', 'SecureJobLab');
define('APP_FULL_TITLE', 'SecureJobLab: Dual-Engine Web Application Security Laboratory');
define('APP_COURSE', '20CYS403 — Web Application Security');
define('APP_STUDENT_NAME', 'Ram Karthik G');
define('APP_VERSION', '2.0.0');

// --------------------------------------------------------------------
// 3. Centralized Database Connection Helper
// --------------------------------------------------------------------
function get_db_connection() {
    static $conn = null;
    if ($conn === null) {
        $conn = @mysqli_connect(DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT);
        if ($conn) {
            mysqli_set_charset($conn, 'utf8mb4');
            mysqli_report(MYSQLI_REPORT_OFF);
        }
    }
    return $conn;
}

// --------------------------------------------------------------------
// 4. Helper: CSRF / Session Security
// --------------------------------------------------------------------
function ensure_session_started() {
    if (session_status() === PHP_SESSION_NONE) {
        // Enforce cookie flags for session security
        session_set_cookie_params([
            'lifetime' => 0,
            'path'     => '/',
            'httponly' => true,
            'samesite' => 'Lax'
        ]);
        session_start();
    }
}
