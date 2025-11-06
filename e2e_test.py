#!/usr/bin/env python3
"""E2E Test for Basic Query Execution"""

import json
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Configuration
BASE_PATH = Path("/opt/asw/projects/personal/tac/tac-5")
SCREENSHOT_DIR = BASE_PATH / "agents/9226d179/e2e_test_runner_0_0/img/basic_query"
APPLICATION_URL = "http://localhost:5173"
TEST_NAME = "Basic Query Execution"

# Ensure screenshot directory exists
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def run_test():
    """Execute the E2E test steps"""
    result = {
        "test_name": TEST_NAME,
        "status": "failed",
        "screenshots": [],
        "error": None
    }

    screenshots = []

    try:
        with sync_playwright() as p:
            # Launch browser in headed mode for visibility
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            # Step 1: Navigate to the application
            print("Step 1: Navigating to application...")
            page.goto(APPLICATION_URL, wait_until="networkidle", timeout=10000)
            time.sleep(1)

            # Step 2: Take screenshot of initial state
            print("Step 2: Taking screenshot of initial state...")
            screenshot_path = SCREENSHOT_DIR / "01_initial_state.png"
            page.screenshot(path=str(screenshot_path))
            screenshots.append(str(screenshot_path))
            print(f"✓ Screenshot saved: {screenshot_path}")

            # Step 3: Verify page title
            print("Step 3: Verifying page title...")
            title = page.title()
            if title != "Natural Language SQL Interface":
                result["error"] = f"(Step 3 ❌) Expected page title 'Natural Language SQL Interface', but got '{title}'"
                browser.close()
                return result
            print(f"✓ Page title verified: {title}")

            # Step 4: Verify core UI elements are present
            print("Step 4: Verifying core UI elements...")

            # Query input textbox
            query_input = page.locator('textarea[placeholder*="Ask a question"], input[placeholder*="query"]').first
            if not query_input.is_visible(timeout=5000):
                result["error"] = "(Step 4 ❌) Failed to find query input textbox"
                browser.close()
                return result
            print("✓ Query input textbox found")

            # Query button
            query_button = page.get_by_role("button", name="Query").first
            if not query_button.is_visible(timeout=5000):
                result["error"] = "(Step 4 ❌) Failed to find Query button"
                browser.close()
                return result
            print("✓ Query button found")

            # Upload Data button
            upload_button = page.get_by_role("button", name="Upload Data").first
            if not upload_button.is_visible(timeout=5000):
                result["error"] = "(Step 4 ❌) Failed to find Upload Data button"
                browser.close()
                return result
            print("✓ Upload Data button found")

            # Available Tables section
            tables_section = page.locator('text="Available Tables"').first
            if not tables_section.is_visible(timeout=5000):
                result["error"] = "(Step 4 ❌) Failed to find Available Tables section"
                browser.close()
                return result
            print("✓ Available Tables section found")

            # Step 5: Enter the query
            print("Step 5: Entering query...")
            query_text = "Show me all users from the users table"
            query_input.fill(query_text)
            time.sleep(0.5)
            print(f"✓ Query entered: {query_text}")

            # Step 6: Take screenshot of query input
            print("Step 6: Taking screenshot of query input...")
            screenshot_path = SCREENSHOT_DIR / "02_query_input.png"
            page.screenshot(path=str(screenshot_path))
            screenshots.append(str(screenshot_path))
            print(f"✓ Screenshot saved: {screenshot_path}")

            # Step 7: Click the Query button
            print("Step 7: Clicking Query button...")
            query_button.click()
            time.sleep(5)  # Wait for query to process
            print("✓ Query button clicked")

            # Step 8: Verify query results appear
            print("Step 8: Verifying query results appear...")
            # Try multiple selectors to find results
            try:
                # Look for a table element (results are likely in a table)
                page.wait_for_selector('table', timeout=10000)
                print("✓ Query results appeared (table found)")
            except PlaywrightTimeoutError:
                # If no table, look for any results container
                try:
                    page.wait_for_selector('text=/SELECT.*FROM/i', timeout=5000)
                    print("✓ Query results appeared (SQL found)")
                except PlaywrightTimeoutError:
                    result["error"] = "(Step 8 ❌) Query results did not appear"
                    browser.close()
                    return result

            # Step 9: Verify SQL translation is displayed
            print("Step 9: Verifying SQL translation...")
            sql_display = page.locator('text=/SELECT.*FROM.*users/i').first
            if not sql_display.is_visible(timeout=5000):
                result["error"] = "(Step 9 ❌) SQL translation not displayed or does not contain 'SELECT * FROM users'"
                browser.close()
                return result
            print("✓ SQL translation displayed")

            # Step 10: Take screenshot of SQL translation
            print("Step 10: Taking screenshot of SQL translation...")
            screenshot_path = SCREENSHOT_DIR / "03_sql_translation.png"
            page.screenshot(path=str(screenshot_path))
            screenshots.append(str(screenshot_path))
            print(f"✓ Screenshot saved: {screenshot_path}")

            # Step 11: Verify results table contains data
            print("Step 11: Verifying results table contains data...")
            table = page.locator('table').first
            if not table.is_visible(timeout=5000):
                result["error"] = "(Step 11 ❌) Results table not found"
                browser.close()
                return result

            rows = table.locator('tbody tr').count()
            if rows == 0:
                result["error"] = "(Step 11 ❌) Results table is empty"
                browser.close()
                return result
            print(f"✓ Results table contains {rows} rows")

            # Step 12: Take screenshot of results
            print("Step 12: Taking screenshot of results...")
            screenshot_path = SCREENSHOT_DIR / "04_results.png"
            page.screenshot(path=str(screenshot_path))
            screenshots.append(str(screenshot_path))
            print(f"✓ Screenshot saved: {screenshot_path}")

            # Step 13: Click Hide button
            print("Step 13: Clicking Hide button...")
            hide_button = page.get_by_role("button", name="Hide").first
            if not hide_button.is_visible(timeout=5000):
                result["error"] = "(Step 13 ❌) Hide button not found"
                browser.close()
                return result
            hide_button.click()
            time.sleep(0.5)
            print("✓ Hide button clicked")

            # Success!
            print("\n✅ All test steps passed!")
            result["status"] = "passed"
            result["screenshots"] = screenshots

            browser.close()

    except PlaywrightTimeoutError as e:
        result["error"] = f"Timeout error: {str(e)}"
        result["screenshots"] = screenshots
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"
        result["screenshots"] = screenshots

    return result

if __name__ == "__main__":
    print(f"Starting E2E Test: {TEST_NAME}")
    print(f"Application URL: {APPLICATION_URL}")
    print(f"Screenshot Directory: {SCREENSHOT_DIR}\n")

    result = run_test()

    # Output JSON result
    print("\n" + "="*80)
    print("TEST RESULT:")
    print("="*80)
    print(json.dumps(result, indent=2))

    # Exit with appropriate code
    sys.exit(0 if result["status"] == "passed" else 1)
