"""
E2E Test: Complex Query with Filtering
Test complex query capabilities with filtering conditions.
"""

import json
import time
import os
from playwright.sync_api import sync_playwright, Page, expect

# Configuration
APPLICATION_URL = "http://localhost:5173"
SCREENSHOT_DIR = "/opt/asw/projects/personal/tac/tac-5/agents/9226d179/e2e_test_runner_0_1/img/complex_query"
TEST_QUERY = "Show users older than 30 who live in cities starting with 'S'"

def run_test():
    """Execute the E2E test for complex queries"""
    test_result = {
        "test_name": "Complex Query with Filtering",
        "status": "failed",
        "screenshots": [],
        "error": None
    }

    try:
        with sync_playwright() as p:
            # Launch browser in headed mode
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            # Step 1: Navigate to the application
            print("Step 1: Navigating to application...")
            page.goto(APPLICATION_URL)
            page.wait_for_load_state("networkidle")
            time.sleep(1)

            # Step 2: Take screenshot of initial state
            print("Step 2: Taking screenshot of initial state...")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "01_initial_state.png")
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)

            # Step 3: Clear the query input
            print("Step 3: Clearing query input...")
            query_input = page.locator("#query-input")
            query_input.click()
            query_input.fill("")

            # Step 4: Enter the complex query
            print(f"Step 4: Entering query: '{TEST_QUERY}'")
            query_input.fill(TEST_QUERY)
            time.sleep(0.5)

            # Step 5: Take screenshot of query input
            print("Step 5: Taking screenshot of query input...")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "02_query_input.png")
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)

            # Step 6: Click Query button
            print("Step 6: Clicking Query button...")
            query_button = page.locator("#query-button")
            query_button.click()

            # Wait for results to appear
            print("Waiting for results...")
            page.wait_for_selector("#results-section", state="visible", timeout=10000)
            time.sleep(2)  # Additional wait for rendering

            # Step 7: Verify results appear with filtered data
            print("Step 7: Verifying results appear...")
            results_section = page.locator("#results-section")
            if not results_section.is_visible():
                test_result["error"] = "(Step 7 ❌) Results section is not visible"
                return test_result

            # Step 8: Verify the generated SQL contains WHERE clause
            print("Step 8: Verifying SQL contains WHERE clause...")
            sql_display = page.locator("#sql-display")
            sql_text = sql_display.inner_text()
            if "WHERE" not in sql_text.upper():
                test_result["error"] = "(Step 8 ❌) Generated SQL does not contain WHERE clause"
                return test_result

            # Step 9: Take screenshot of SQL translation
            print("Step 9: Taking screenshot of SQL translation...")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "03_sql_translation.png")
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)

            # Step 10: Count the number of results returned
            print("Step 10: Counting results...")
            results_container = page.locator("#results-container")
            # Look for table rows (excluding header)
            result_rows = results_container.locator("table tbody tr")
            result_count = result_rows.count()
            print(f"Found {result_count} results")

            # Verify we have some results
            if result_count == 0:
                test_result["error"] = "(Step 10 ❌) No results returned from query"
                return test_result

            # Step 11: Take screenshot of filtered results
            print("Step 11: Taking screenshot of filtered results...")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "04_filtered_results.png")
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)

            # Step 12: Click Hide button
            print("Step 12: Clicking Hide button...")
            hide_button = page.locator("#toggle-results")
            hide_button.click()
            time.sleep(0.5)

            # Verify Hide button text changed to Show (which means results are hidden)
            button_text = hide_button.inner_text()
            if button_text != "Show":
                test_result["error"] = f"(Step 12 ❌) Hide button text is '{button_text}', expected 'Show'"
                return test_result

            # Step 13: Take screenshot of final state
            print("Step 13: Taking screenshot of final state...")
            screenshot_path = os.path.join(SCREENSHOT_DIR, "05_final_state.png")
            page.screenshot(path=screenshot_path)
            test_result["screenshots"].append(screenshot_path)

            # Success criteria checks
            print("\nVerifying success criteria...")

            # Check screenshot count
            if len(test_result["screenshots"]) != 5:
                test_result["error"] = f"Expected 5 screenshots, but got {len(test_result['screenshots'])}"
                return test_result

            # All checks passed
            test_result["status"] = "passed"
            print("\n✅ All test steps completed successfully!")

            # Close browser
            browser.close()

    except Exception as e:
        test_result["error"] = f"Unexpected error: {str(e)}"
        print(f"\n❌ Test failed with error: {str(e)}")

    return test_result

if __name__ == "__main__":
    print("=" * 80)
    print("E2E Test: Complex Query with Filtering")
    print("=" * 80)

    result = run_test()

    print("\n" + "=" * 80)
    print("Test Results")
    print("=" * 80)
    print(json.dumps(result, indent=2))
