-- ====================================================================
-- SecureJobLab: Database Schema & Seed Data (UTF-8 Verified)
-- Course: 20CYS403 Web Application Security
-- Persona: Ram Karthik (Candidate & AppSec Specialist)
-- ====================================================================

CREATE DATABASE IF NOT EXISTS `securejoblab` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `securejoblab`;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `feedback`;
DROP TABLE IF EXISTS `applications`;
DROP TABLE IF EXISTS `jobs`;
DROP TABLE IF EXISTS `users`;
SET FOREIGN_KEY_CHECKS = 1;

-- 1. Users Table (Authentication & RBAC)
CREATE TABLE `users` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `username` VARCHAR(50) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `full_name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(120) NOT NULL,
  `role` VARCHAR(20) NOT NULL DEFAULT 'candidate',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Seed Credentials (12 Working Accounts for System Access)
INSERT INTO `users` (`id`, `username`, `password`, `full_name`, `email`, `role`) VALUES
(1, 'candidate', '$2y$10$3n2K5GqJp3.16z2r90zGq.Bsmk6hL8e5zJ3.7E3V4G6k18N1dM3C2', 'Ram Karthik', 'ram.karthik@securejob.io', 'candidate'),
(2, 'recruiter', '$2y$10$3n2K5GqJp3.16z2r90zGq.Bsmk6hL8e5zJ3.7E3V4G6k18N1dM3C2', 'Sarah Jenkins (Recruiter)', 'sarah.jenkins@techrecruit.io', 'company'),
(3, 'admin', '$2y$10$3n2K5GqJp3.16z2r90zGq.Bsmk6hL8e5zJ3.7E3V4G6k18N1dM3C2', 'System Administrator', 'admin@securejoblab.local', 'admin'),
(4, 'ram.karthik', '$2y$10$3n2K5GqJp3.16z2r90zGq.Bsmk6hL8e5zJ3.7E3V4G6k18N1dM3C2', 'Ram Karthik (AppSec Specialist)', 'ram.karthik@securejob.io', 'candidate'),
(5, 'sarah.recruiter', '$2y$10$eEskhU960hGkUuQWq4Q41.r1Xq6pG0dM9jEw9bJ1F2O8N1dM3C2', 'Sarah Jenkins (Lead Recruiter)', 'sarah.recruiter@securejob.io', 'company'),
(6, 'vikram.sharma', '$2y$10$h9h4wY4gK0jZ7L4pE1Xq6pG0dM9jEw9bJ1F2O8N1dM3C2', 'Vikram Sharma (Staff AppSec)', 'vikram.sharma@securejob.io', 'candidate'),
(7, 'priya.nair', '$2y$10$k1w9sF8xL2mQ0r8tE1Xq6pG0dM9jEw9bJ1F2O8N1dM3C2', 'Priya Nair (Cloud Security)', 'priya.nair@securejob.io', 'candidate'),
(8, 'arun.devsec', '$2y$10$m3t8vP7qZ9jK2l4wE1Xq6pG0dM9jEw9bJ1F2O8N1dM3C2', 'Arun Kumar (DevSecOps Lead)', 'arun.kumar@securejob.io', 'candidate'),
(9, 'ananya.audit', '$2y$10$p5r7xW2sK8jM1n6yE1Xq6pG0dM9jEw9bJ1F2O8N1dM3C2', 'Ananya Sen (Compliance Auditor)', 'ananya.sen@securejob.io', 'company'),
(10, 'rohit.soc', '$2y$10$q9s4zX8mK1jL5o2wE1Xq6pG0dM9jEw9bJ1F2O8N1dM3C2', 'Rohit Verma (SOC Analyst L2)', 'rohit.verma@securejob.io', 'candidate'),
(11, 'meera.pentest', '$2y$10$r2t6yW9pL4jN7q3xE1Xq6pG0dM9jEw9bJ1F2O8N1dM3C2', 'Meera Patel (Penetration Tester)', 'meera.patel@securejob.io', 'candidate'),
(12, 'karthik.manager', '$2y$10$s8u1zV3qM5jP9r4yE1Xq6pG0dM9jEw9bJ1F2O8N1dM3C2', 'Karthik Rajan (Infosec Manager)', 'karthik.rajan@securejob.io', 'admin');

-- 2. Jobs Table (Job Postings & Full CRUD with clean ₹ salaries)
CREATE TABLE `jobs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `title` VARCHAR(120) NOT NULL,
  `company` VARCHAR(120) NOT NULL,
  `location` VARCHAR(100) NOT NULL,
  `salary` VARCHAR(60) NOT NULL,
  `job_type` VARCHAR(50) NOT NULL DEFAULT 'Full-time',
  `department` VARCHAR(80) NOT NULL DEFAULT 'Engineering',
  `description` TEXT NOT NULL,
  `secret_notes` TEXT NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `jobs` (`id`, `title`, `company`, `location`, `salary`, `job_type`, `department`, `description`, `secret_notes`) VALUES
(1, 'Senior Cybersecurity Engineer', 'Amazon Web Services (AWS)', 'Bangalore / Hybrid', '₹28,00,000 / yr', 'Full-time', 'Information Security', 'Architect automated application security scanning, threat modeling, and defensive frameworks for cloud native services.', 'CONFIDENTIAL: Salary band max ₹32 LPA. Clearance Level 3.'),
(2, 'Application Security Specialist', 'Stripe Payments', 'Bangalore / Remote', '₹24,00,000 / yr', 'Full-time', 'Product Security', 'Identify vulnerabilities across high-throughput financial APIs, perform manual code review, and build defensive tooling.', 'CONFIDENTIAL: Sign-on equity grant 1,200 RSUs approved.'),
(3, 'Cloud Security Operations Analyst', 'Microsoft India', 'Hyderabad', '₹20,00,000 / yr', 'Full-time', 'Cloud Operations', 'Monitor cloud security telemetry, investigate SIEM alerts, and execute incident response runbooks.', 'CONFIDENTIAL: Shift rotation bonus ₹30,000/month.'),
(4, 'Full Stack Security Engineer', 'Razorpay', 'Bangalore / Onsite', '₹22,00,000 / yr', 'Full-time', 'FinTech Security', 'Develop resilient web services, integrate SAST/DAST pipelines, and audit authentication and payment gateway workflows.', 'CONFIDENTIAL: Candidate shortlisted for final interview round.'),
(5, 'DevSecOps Automation Engineer', 'CRED Tech', 'Bangalore / Remote', '₹26,00,000 / yr', 'Full-time', 'Infrastructure', 'Build zero-trust CI/CD deployment gates, secure Kubernetes container runtime, and automate vulnerability remediation.', 'CONFIDENTIAL: Budget flexibility up to ₹29 LPA.');

-- 3. Applications Table
CREATE TABLE `applications` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `job_title` VARCHAR(120) NOT NULL,
  `company` VARCHAR(120) NOT NULL,
  `applicant_name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(120) NOT NULL,
  `phone` VARCHAR(30) NOT NULL,
  `experience` VARCHAR(50) NOT NULL,
  `cover_note` TEXT NOT NULL,
  `resume_file` VARCHAR(255) NOT NULL,
  `status` VARCHAR(50) NOT NULL DEFAULT 'In Review',
  `applied_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `applications` (`id`, `job_title`, `company`, `applicant_name`, `email`, `phone`, `experience`, `cover_note`, `resume_file`, `status`) VALUES
(1, 'Senior Cybersecurity Engineer', 'Amazon Web Services (AWS)', 'Ram Karthik', 'ram.karthik@securejob.io', '+91 98765 43210', '3+ Years in AppSec', 'Passionate about defensive web architectures and cloud security.', 'lab_files/resume.txt', 'Interview Scheduled'),
(2, 'Application Security Specialist', 'Stripe Payments', 'Ram Karthik', 'ram.karthik@securejob.io', '+91 98765 43210', '3+ Years in AppSec', 'Extensive experience auditing web APIs and implementing OWASP defenses.', 'lab_files/resume.txt', 'Under Review');

-- 4. Feedback / Reviews Table (For XSS & CSRF Demonstration)
CREATE TABLE `feedback` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `author` VARCHAR(100) NOT NULL,
  `comment` TEXT NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `feedback` (`id`, `author`, `comment`) VALUES
(1, 'Tech Recruiter (AWS)', 'Ram Karthik demonstrated outstanding technical depth in secure code review and cloud architecture defense.'),
(2, 'Lead Security Architect (Stripe)', 'Solid understanding of OWASP Top 10 vulnerabilities, parameterization, and cryptographic session protection.');
