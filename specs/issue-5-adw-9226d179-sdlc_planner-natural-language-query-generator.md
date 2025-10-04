# Feature: Random Natural Language Query Generator

## Feature Description
Add a button that generates interesting natural language queries based on the existing database tables and their structure. The button will use the LLM to create contextually relevant queries (maximum 2 sentences) and automatically populate the query input field, overwriting any existing content. This feature helps users discover query possibilities and learn how to interact with their data.

## User Story
As a user
I want to generate example natural language queries based on my uploaded tables
So that I can quickly explore my data and learn what kinds of questions I can ask

## Problem Statement
Users may not know what types of questions they can ask about their data, especially when working with new or unfamiliar datasets. This creates friction in the user experience and may prevent users from fully utilizing the natural language SQL interface capabilities.

## Solution Statement
Add a "Generate Query" button that analyzes the current database schema (tables, columns, data types, and row counts) and uses the existing LLM processor to generate contextually relevant, interesting natural language queries. The generated queries will be automatically inserted into the query input field, ready for the user to execute or modify. The button will use a plaid/checkered design pattern to distinguish it from primary action buttons.

## Relevant Files
Use these files to implement the feature:

- **app/server/core/llm_processor.py** - Contains LLM integration functions for OpenAI and Anthropic. Will be extended to add a new function for generating natural language queries based on database schema.

- **app/server/server.py** - FastAPI server with existing endpoints. Will add a new `/api/generate-query` endpoint that accepts the current schema and returns a generated natural language query.

- **app/server/core/data_models.py** - Contains Pydantic models for request/response validation. Will add new models for the generate query endpoint.

- **app/server/core/sql_processor.py** - Contains `get_database_schema()` function that returns current database structure. Will be used to provide schema information to the query generator.

- **app/client/src/main.ts** - Main TypeScript file with UI logic and event handlers. Will add event handler for the new "Generate Query" button and logic to populate the query input field.

- **app/client/src/api/client.ts** - API client with methods for backend communication. Will add a new method to call the generate query endpoint.

- **app/client/index.html** - HTML structure with query section. Will add the new "Generate Query" button in the query controls section with appropriate spacing.

- **app/client/src/style.css** - Contains all CSS styles including button styles. Will add styles for the plaid-style button to differentiate it from primary and secondary buttons.

- **app/client/src/types.d.ts** - TypeScript type definitions for API responses. Will add types for the generate query response.

### New Files
- **.claude/commands/e2e/test_generate_query.md** - E2E test file to validate the natural language query generator feature works correctly with screenshots demonstrating the functionality.

- **app/server/tests/core/test_query_generator.py** - Unit tests for the query generation logic to ensure it generates valid queries based on different schema configurations.

## Implementation Plan

### Phase 1: Foundation
Create the backend infrastructure for query generation, including the LLM processor function, data models, and API endpoint. This phase establishes the core logic for analyzing database schemas and generating contextually relevant natural language queries using the existing LLM integration.

### Phase 2: Core Implementation
Implement the frontend button with plaid styling, wire up the API call, and add logic to populate the query input field. This phase creates the user-facing interface and ensures smooth integration with existing UI components.

### Phase 3: Integration
Add comprehensive tests (unit and E2E), validate error handling, ensure the feature works with both OpenAI and Anthropic providers, and verify the feature integrates seamlessly with existing query execution flow.

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Backend Data Models
- Open `app/server/core/data_models.py`
- Add `GenerateQueryRequest` model (empty request or can include optional parameters like query style preference)
- Add `GenerateQueryResponse` model with fields: `query` (str), `tables_used` (List[str]), `error` (Optional[str])
- Ensure models follow existing patterns in the file

### 2. Backend Query Generation Logic
- Open `app/server/core/llm_processor.py`
- Create new function `generate_natural_language_query(schema_info: Dict[str, Any]) -> str`
- Function should format schema information into a prompt for the LLM
- Prompt should instruct the LLM to generate an interesting, specific query based on the available tables and columns
- Prompt should specify: maximum 2 sentences, must reference actual tables/columns, should be interesting/insightful
- Add functions for both `generate_query_with_openai()` and `generate_query_with_anthropic()` following existing patterns
- Add routing logic similar to existing `generate_sql()` function that prioritizes OpenAI if available
- Format prompt to encourage diverse query types (aggregations, filters, joins if multiple tables exist)
- Add error handling for cases where no tables exist

### 3. Backend API Endpoint
- Open `app/server/server.py`
- Add new POST endpoint `/api/generate-query` with response model `GenerateQueryResponse`
- Endpoint should get current database schema using `get_database_schema()`
- Validate that at least one table exists (return error if no tables)
- Call the new LLM query generation function
- Return generated query with list of tables referenced
- Add appropriate logging similar to other endpoints
- Add error handling with try/except blocks

### 4. Backend Unit Tests
- Create `app/server/tests/core/test_query_generator.py`
- Test query generation with single table schema
- Test query generation with multiple tables schema
- Test error handling when no tables exist
- Test that generated queries reference actual table/column names
- Test that queries are within 2 sentence limit
- Mock LLM responses to avoid actual API calls in tests

### 5. Frontend Type Definitions
- Open `app/client/src/types.d.ts`
- Add `GenerateQueryRequest` interface (can be empty object or with optional parameters)
- Add `GenerateQueryResponse` interface matching backend model
- Ensure types align with backend Pydantic models

### 6. Frontend API Client
- Open `app/client/src/api/client.ts`
- Add new method `generateQuery()` that calls POST `/api/generate-query`
- Follow existing patterns for error handling and response typing
- Return `Promise<GenerateQueryResponse>`

### 7. Frontend Plaid Button Styling
- Open `app/client/src/style.css`
- Add new `.plaid-button` class with distinctive plaid/checkered pattern styling
- Use CSS gradient or repeating patterns to create plaid effect
- Ensure button has similar size/padding to primary and secondary buttons
- Add hover states and transitions consistent with existing buttons
- Use colors that complement existing color palette but stand out
- Add disabled state styling

### 8. Frontend HTML Structure
- Open `app/client/index.html`
- In the `.query-controls` div, add new button with id `generate-query-button` and class `plaid-button`
- Button text: "Generate Query" or "✨ Generate Query"
- Place button with `justify-content: space-between` or similar spacing so it's visually separated from Query and Upload Data buttons
- Update container div styling if needed to accommodate three buttons with proper spacing

### 9. Frontend Button Logic
- Open `app/client/src/main.ts`
- Create new function `initializeGenerateQuery()`
- Add event listener to `generate-query-button`
- On click: disable button, show loading state, call `api.generateQuery()`
- On success: populate `query-input` textarea with generated query (overwrite existing content)
- On error: display error message using existing `displayError()` function
- On complete: re-enable button
- Handle edge case where no tables exist (show friendly message)
- Call `initializeGenerateQuery()` in the DOMContentLoaded event listener

### 10. Create E2E Test File
- Read `.claude/commands/test_e2e.md` to understand E2E test format
- Read `.claude/commands/e2e/test_basic_query.md` as a reference example
- Create `.claude/commands/e2e/test_generate_query.md`
- Test steps should include:
  1. Upload sample data (users table)
  2. Verify "Generate Query" button is present
  3. Click "Generate Query" button
  4. Verify query input field is populated with generated text
  5. Verify generated query references the "users" table
  6. Take screenshot of generated query
  7. Click "Query" button to execute generated query
  8. Verify results are displayed successfully
  9. Take screenshot of results
  10. Click "Generate Query" again to verify different query is generated
  11. Take screenshot of second generated query
- Include proper user story, success criteria, and verification steps

### 11. Manual Testing and Validation
- Start the development server using `./scripts/start.sh`
- Upload sample data (users, products, or events)
- Click the "Generate Query" button multiple times
- Verify each generated query is different and contextually relevant
- Verify queries reference actual table and column names
- Verify queries are executable (copy and run them)
- Test with single table and multiple tables
- Test button disabled state during generation
- Test error handling when no tables exist
- Test with both OpenAI and Anthropic (if both API keys available)

### 12. Execute Validation Commands
- Run all validation commands listed in the "Validation Commands" section below
- Ensure all tests pass with zero errors
- Ensure E2E test captures all required screenshots
- Ensure build completes successfully
- Fix any issues discovered during validation

## Testing Strategy

### Unit Tests
- **Test query generation logic** (`test_query_generator.py`):
  - Test with single table containing various column types (TEXT, INTEGER, REAL, DATE)
  - Test with multiple tables to ensure queries can leverage joins
  - Test with empty database (no tables) - should return appropriate error
  - Test that generated queries reference actual table and column names from schema
  - Test query length constraint (maximum 2 sentences)
  - Mock LLM API calls to avoid rate limits and ensure deterministic tests

- **Test API endpoint**:
  - Test successful query generation response format
  - Test error response when no tables exist
  - Test response includes `tables_used` field with correct table references

### Edge Cases
- **No tables in database**: Should return error message "No tables available. Please upload data first."
- **Single table with minimal columns**: Should still generate a valid, interesting query
- **Multiple tables with complex schemas**: Should generate queries that may use joins or reference multiple tables
- **Very long table/column names**: Should handle gracefully without breaking prompt
- **Special characters in table/column names**: Should properly escape/handle in generated queries
- **LLM API failure**: Should catch errors and return user-friendly message
- **LLM returns invalid format**: Should validate response and handle gracefully
- **Button clicked multiple times rapidly**: Should prevent concurrent requests (disable button during generation)
- **Query input field has existing content**: Should overwrite without confirmation (as specified)

## Acceptance Criteria
- ✅ New "Generate Query" button appears in the query controls section with distinctive plaid styling
- ✅ Button is visually separated from "Query" and "Upload Data" buttons (using space-between or similar spacing)
- ✅ Clicking the button calls the backend API and generates a natural language query
- ✅ Generated query is automatically populated into the query input field, overwriting any existing content
- ✅ Generated queries are contextually relevant, referencing actual table and column names
- ✅ Generated queries are limited to maximum 2 sentences
- ✅ Button shows loading state during query generation
- ✅ Error handling works when no tables exist or API call fails
- ✅ Feature works with both OpenAI and Anthropic LLM providers
- ✅ Generated queries are executable (can be run using the Query button)
- ✅ Each click generates a different query (variety in generated queries)
- ✅ All existing functionality remains unchanged (no regressions)
- ✅ Unit tests pass for query generation logic
- ✅ E2E test validates the complete user flow with screenshots
- ✅ Frontend build completes without errors
- ✅ Backend tests pass without errors

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md`, then read and execute `.claude/commands/e2e/test_generate_query.md` to validate the natural language query generator functionality works end-to-end with visual proof via screenshots

- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run unit tests for query generator to validate logic

- `cd app/server && uv run pytest` - Run all server tests to validate the feature works with zero regressions

- `cd app/client && bun run tsc --noEmit` - Run TypeScript type checking to validate frontend code

- `cd app/client && bun run build` - Run frontend build to validate the feature compiles correctly with zero errors

## Notes

### LLM Prompt Engineering Considerations
- The prompt should encourage variety in generated queries to make each generation interesting
- Consider including instructions for different query types: aggregations (COUNT, AVG, SUM), filtering (WHERE), sorting (ORDER BY), limiting (LIMIT), and joins (when multiple tables available)
- Prompt should explicitly state to use actual table and column names from the provided schema
- Consider adding temperature/randomness to LLM calls to increase variety in generated queries

### Future Enhancements (Not in Scope)
- Query history/favorites to save generated queries users found useful
- Query complexity selector (simple/medium/complex)
- Query category selector (aggregation/filtering/join/etc.)
- "Explain Query" feature that describes what the generated query does
- Save/bookmark particularly useful generated queries

### Design Notes
- The plaid button design helps users recognize this as a creative/generative feature distinct from primary actions
- Overwriting the query input field (rather than appending) ensures clean UX and prevents confusion
- The 2-sentence limit ensures queries remain focused and comprehensible
- Justifying apart from primary buttons helps users discover the feature without it being too prominent or distracting

### Performance Considerations
- Query generation requires an LLM API call, which typically takes 1-3 seconds
- Button should show clear loading state to set expectations
- Consider caching schema info if this becomes a performance bottleneck
- API timeout should be reasonable (e.g., 10 seconds) to handle slow LLM responses
