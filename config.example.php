<?php
// ====================================================================
// SecureJobLab: Central Configuration Template (Example)
// Course: 20CYS403 Web Application Security
// Copy this file to 'config.php' and adjust settings as needed.
// ====================================================================

define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_NAME', 'securejoblab');
define('DB_PORT', 3306);

define('APP_NAME', 'SecureJobLab');
define('APP_COURSE', '20CYS403 — Web Application Security');
define('APP_STUDENT_NAME', 'Ram Karthik G');
define('APP_VERSION', '2.0.0');

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
