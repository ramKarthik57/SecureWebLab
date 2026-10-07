<?php
// ====================================================================
// SecureJobLab: Document Viewer Compatibility Forwarder
// Canonical Implementation: view_resume.php
// Course: 20CYS403 Web Application Security
// ====================================================================

// Forward all requests and parameters cleanly to canonical view_resume.php
$queryString = !empty($_SERVER['QUERY_STRING']) ? '?' . $_SERVER['QUERY_STRING'] : '';
header("Location: view_resume.php" . $queryString, true, 302);
exit;
