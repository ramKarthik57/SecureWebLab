import urllib.request, urllib.parse, http.cookiejar, json, sys

sys.stdout.reconfigure(encoding='utf-8')
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Sign in
login_data = urllib.parse.urlencode({'auth_action': 'login', 'username': 'candidate', 'password': 'candidate123'}).encode()
res = opener.open(urllib.request.Request('http://localhost/SecureJobLab/login.php', data=login_data))
print("1. Sign In:", res.getcode())

# 2. Test Module 6 Vulnerable (Upload dangerous php script)
m6_vuln_data = urllib.parse.urlencode({
    'action': 'test_lab', 'vuln_id': 6, 'mode': 'vulnerable', 'filename': 'exploit_test.php',
    'file_content': 'test_php_payload', 'reported_mime': 'application/x-php'
}).encode()
res = opener.open(urllib.request.Request('http://localhost/SecureJobLab/api.php', data=m6_vuln_data))
m6_v = json.loads(res.read().decode())
print("2. M6 Vuln:", m6_v.get('status_type'), "|", m6_v.get('exploit_status')[:65])

# 3. Test Module 6 Secure (Dangerous file rejected)
m6_sec_data = urllib.parse.urlencode({
    'action': 'test_lab', 'vuln_id': 6, 'mode': 'secure', 'filename': 'exploit_test.php',
    'file_content': 'test_php_payload', 'reported_mime': 'application/x-php'
}).encode()
res = opener.open(urllib.request.Request('http://localhost/SecureJobLab/api.php', data=m6_sec_data))
m6_s = json.loads(res.read().decode())
print("3. M6 Sec Reject:", m6_s.get('status_type'), "|", m6_s.get('exploit_status')[:65])

# 4. Test Module 6 Secure (Safe file accepted)
m6_sec_ok_data = urllib.parse.urlencode({
    'action': 'test_lab', 'vuln_id': 6, 'mode': 'secure', 'filename': 'candidate_cv.pdf',
    'file_content': '%PDF-1.4 harmless test resume document', 'reported_mime': 'application/pdf'
}).encode()
res = opener.open(urllib.request.Request('http://localhost/SecureJobLab/api.php', data=m6_sec_ok_data))
m6_s_ok = json.loads(res.read().decode())
print("4. M6 Sec Safe:", m6_s_ok.get('status_type'), "|", m6_s_ok.get('exploit_status')[:65])

# 5. Test Module 7 Vulnerable (CSRF Forgery accepted)
m7_vuln_data = urllib.parse.urlencode({
    'action': 'test_lab', 'vuln_id': 7, 'mode': 'vulnerable', 'origin': 'https://attacker-evil-job-board.xyz',
    'theme': 'hacked_dark_theme', 'notifications': 'disabled', 'is_forged': '1'
}).encode()
res = opener.open(urllib.request.Request('http://localhost/SecureJobLab/api.php', data=m7_vuln_data))
m7_v = json.loads(res.read().decode())
print("5. M7 Vuln:", m7_v.get('status_type'), "|", m7_v.get('exploit_status')[:65])

# 6. Test Module 7 Secure (Missing CSRF Token rejected)
m7_sec_data = urllib.parse.urlencode({
    'action': 'test_lab', 'vuln_id': 7, 'mode': 'secure', 'origin': 'https://attacker-evil-job-board.xyz',
    'theme': 'hacked_dark_theme', 'notifications': 'disabled', 'is_forged': '1'
}).encode()
res = opener.open(urllib.request.Request('http://localhost/SecureJobLab/api.php', data=m7_sec_data))
m7_s = json.loads(res.read().decode())
print("6. M7 Sec Blocked:", m7_s.get('status_type'), "|", m7_s.get('exploit_status')[:65])
