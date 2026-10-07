import time
from playwright.sync_api import sync_playwright

def take_screenshots():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe", headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        # 1. Sign in
        page.goto("http://localhost/SecureJobLab/login.php")
        page.fill("input[name='username']", "candidate")
        page.fill("input[name='password']", "candidate123")
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")
        time.sleep(1)

        # 2. Module 6 Vulnerable (Upload Test)
        page.goto("http://localhost/SecureJobLab/index.php?tab=lab&vuln=6&mode=vulnerable")
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)
        page.click("button:has-text('Execute Test')")
        time.sleep(1)
        page.screenshot(path="lab_5vuln_screenshots/mod6_vulnerable.png")
        print("Captured mod6_vulnerable.png")

        # 3. Module 6 Secure (Upload Blocked)
        page.goto("http://localhost/SecureJobLab/index.php?tab=lab&vuln=6&mode=secure")
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)
        page.click("button:has-text('Execute Test')")
        time.sleep(1)
        page.screenshot(path="lab_5vuln_screenshots/mod6_secure.png")
        print("Captured mod6_secure.png")

        # 4. Module 7 Vulnerable (CSRF Forgery Accepted)
        page.goto("http://localhost/SecureJobLab/index.php?tab=lab&vuln=7&mode=vulnerable")
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)
        page.click("button:has-text('Execute Test')")
        time.sleep(1)
        page.screenshot(path="lab_5vuln_screenshots/mod7_vulnerable.png")
        print("Captured mod7_vulnerable.png")

        # 5. Module 7 Secure (CSRF Blocked)
        page.goto("http://localhost/SecureJobLab/index.php?tab=lab&vuln=7&mode=secure")
        page.wait_for_load_state("networkidle")
        time.sleep(0.5)
        page.click("button:has-text('Execute Test')")
        time.sleep(1)
        page.screenshot(path="lab_5vuln_screenshots/mod7_secure.png")
        print("Captured mod7_secure.png")

        browser.close()

if __name__ == "__main__":
    take_screenshots()
