# E2E Test: Generate Query Button Styling Consistency

Test that the Generate Query button has the same visual styling as the Query button (purple gradient instead of plaid pattern).

## User Story

As a user
I want the Generate Query button to have consistent styling with the Query button
So that the interface provides a cohesive visual experience

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state showing both buttons
3. **Verify** the page title is "Natural Language SQL Interface"
4. **Verify** core UI elements are present:
   - Query input textbox
   - Query button
   - Generate Query button (✨ Generate Query)
   - Upload Data button
   - Available Tables section

5. **Verify** both buttons are visible side by side
6. Take a screenshot focusing on both buttons for visual comparison
7. **Verify** the Generate Query button has a purple gradient background (matching the Query button)
8. **Verify** the Generate Query button does NOT have a plaid pattern background
9. **Verify** the Generate Query button text is white
10. **Verify** both buttons have the same visual appearance (gradient background)

11. Hover over the Generate Query button
12. Take a screenshot of the hover state
13. **Verify** the hover effect matches the Query button hover effect (translateY and box-shadow)

14. Click "Upload Data" button
15. Click on "Users Data" sample data button
16. **Verify** the users table appears in the Available Tables section
17. Click the "✨ Generate Query" button to test functionality
18. **Verify** the query input field is populated with generated text
19. **Verify** the button still functions correctly after styling changes
20. Take a screenshot showing the generated query

## Success Criteria
- Both Query and Generate Query buttons are visible
- Generate Query button has the same purple gradient background as Query button
- Generate Query button does NOT have a plaid pattern
- Generate Query button text color is white
- Hover effects match between both buttons
- Button functionality remains intact after styling changes
- At least 4 screenshots are taken demonstrating consistent styling
