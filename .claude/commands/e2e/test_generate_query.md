# E2E Test: Natural Language Query Generator

Test the natural language query generator feature that helps users discover interesting queries they can ask about their data.

## User Story

As a user
I want to generate example natural language queries based on my uploaded tables
So that I can quickly explore my data and learn what kinds of questions I can ask

## Test Steps

1. Navigate to the `Application URL`
2. Take a screenshot of the initial state
3. **Verify** the page title is "Natural Language SQL Interface"
4. **Verify** core UI elements are present:
   - Query input textbox
   - Query button
   - Upload Data button
   - Generate Query button (with plaid styling)
   - Available Tables section

5. Click "Upload Data" button
6. Click on "Users Data" sample data button
7. **Verify** the users table appears in the Available Tables section
8. Take a screenshot showing the users table has been loaded

9. Click the "✨ Generate Query" button
10. **Verify** the query input field is populated with generated text
11. **Verify** the generated query references the "users" table
12. **Verify** the generated query is in natural language (not SQL)
13. Take a screenshot of the first generated query

14. Click the "Query" button to execute the generated query
15. **Verify** the query executes successfully
16. **Verify** results are displayed
17. Take a screenshot of the query results

18. Click the "✨ Generate Query" button again
19. **Verify** the query input field is populated with a new query (should be different from the first)
20. **Verify** the new query also references the "users" table
21. Take a screenshot of the second generated query

22. Click the "✨ Generate Query" button a third time
23. **Verify** the query input field is populated with another query
24. Take a screenshot of the third generated query

## Success Criteria
- Generate Query button is visible with plaid styling
- Button generates contextually relevant queries based on available tables
- Generated queries are in natural language (not SQL)
- Generated queries reference actual table and column names
- Each generated query is different (variety)
- Generated queries are limited to 2 sentences or less
- Generated queries can be successfully executed using the Query button
- Query input field is overwritten (not appended) when generating new queries
- Button shows loading state during query generation
- At least 4 screenshots are taken demonstrating the feature
