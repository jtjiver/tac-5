# Bug: Random Query Button Wrong Colour

## Bug Description
The "✨ Generate Query" button (referred to as "Random Query Button" by the user) currently has a plaid pattern styling that differs from the normal Query button. The button should match the colour scheme of the standard Query button, which uses a gradient from primary to secondary color (purple gradient).

**Current behavior:** The Generate Query button has a plaid background pattern with light gray base color and transparent purple overlays, giving it a distinct plaid appearance.

**Expected behavior:** The Generate Query button should match the Query button's appearance, using the same gradient background (linear-gradient from `--primary-color` to `--secondary-color`).

## Problem Statement
The Generate Query button's visual styling is inconsistent with the primary Query button, creating visual confusion. Both buttons perform query-related actions and should share the same color scheme for consistency.

## Solution Statement
Update the CSS styling for the `.plaid-button` class (used by the Generate Query button) to use the same gradient background as the `.primary-button` class, while maintaining hover effects and other interactive states.

## Steps to Reproduce
1. Start the application using `./scripts/start.sh`
2. Navigate to http://localhost:5173
3. Observe the "✨ Generate Query" button next to the "Query" button
4. Compare the colors: Query button has purple gradient, Generate Query button has plaid pattern

## Root Cause Analysis
The Generate Query button was intentionally styled with a distinctive plaid pattern using the `.plaid-button` class in `app/client/src/style.css:135-163`. This creates a visual inconsistency with the primary Query button which uses `.primary-button` class with a gradient background (`app/client/src/style.css:101-115`).

The HTML in `app/client/index.html:25` applies the `plaid-button` class to the Generate Query button, while the Query button in `app/client/index.html:23` uses the `primary-button` class.

## Relevant Files
Use these files to fix the bug:

- `app/client/src/style.css` - Contains the CSS styling for both `.primary-button` and `.plaid-button` classes. Need to update the `.plaid-button` class to match the `.primary-button` gradient styling.
  - Lines 101-115: `.primary-button` styles with gradient background
  - Lines 135-163: `.plaid-button` styles with plaid pattern that need to be updated

- `app/client/index.html` - Contains the button elements that use these CSS classes
  - Line 23: Query button with `primary-button` class
  - Line 25: Generate Query button with `plaid-button` class

### New Files
None - this is a CSS-only fix to existing files.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Update the `.plaid-button` CSS styling
- Open `app/client/src/style.css`
- Locate the `.plaid-button` class definition (lines 135-163)
- Replace the plaid background pattern with the same gradient used in `.primary-button`
- Change the background to: `background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));`
- Change the text color to: `color: white;`
- Remove the border since primary button doesn't have one: remove the `border: 2px solid var(--primary-color);` line
- Keep the hover effects consistent with `.primary-button` hover behavior
- Update hover state to match `.primary-button:hover` with transform and box-shadow

### 2. Create E2E test to validate the button styling
Read `.claude/commands/test_e2e.md` and `.claude/commands/e2e/test_basic_query.md` and `.claude/commands/e2e/test_generate_query.md` and create a new E2E test file in `.claude/commands/e2e/test_generate_query_button_styling.md` that validates the Generate Query button has the correct styling matching the Query button. The test should:
- Verify both buttons are present
- Take a screenshot showing both buttons side by side
- Visually confirm the Generate Query button has the same gradient styling as the Query button
- Verify the button still functions correctly after the styling change

### 3. Run validation commands
Execute all commands in the `Validation Commands` section to validate the bug is fixed with zero regressions.

## Validation Commands
Execute every command to validate the bug is fixed with zero regressions.

- Manual visual inspection:
  1. Start the application: `./scripts/start.sh`
  2. Navigate to http://localhost:5173
  3. Verify the "✨ Generate Query" button now has the same purple gradient as the "Query" button
  4. Verify the button hover effect matches the Query button
  5. Test button functionality by clicking it to ensure it still generates queries

- Read `.claude/commands/test_e2e.md`, then read and execute your new E2E `.claude/commands/e2e/test_generate_query_button_styling.md` test file to validate this functionality works.

- `cd app/server && uv run pytest` - Run server tests to validate the bug is fixed with zero regressions
- `cd app/client && bun tsc --noEmit` - Run frontend tests to validate the bug is fixed with zero regressions
- `cd app/client && bun run build` - Run frontend build to validate the bug is fixed with zero regressions

## Notes
- This is a purely cosmetic CSS change and should not affect any functionality
- No JavaScript changes are required
- The button's functionality (generating queries) remains unchanged
- The distinctive sparkle emoji (✨) on the button is preserved
- The fix maintains consistency with the existing design system using CSS custom properties (--primary-color and --secondary-color)
- No new dependencies or libraries are needed
