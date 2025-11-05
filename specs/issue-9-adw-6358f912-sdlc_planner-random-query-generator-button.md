# Feature: Random Natural Language Query Generator Button

## Feature Description
This feature adds a new button to the UI that generates interesting, contextually-aware natural language queries based on the current database schema and table structure. When clicked, the button uses the LLM (via llm_processor.py) to analyze available tables and their columns, then generates a natural language query that users can execute manually. The generated query always overwrites the existing content in the query input field and is limited to two sentences maximum. The button uses the plaid styling to match the existing "Upload Data" button aesthetic.

## User Story
As a user exploring my uploaded data
I want a button that generates example natural language queries based on my tables
So that I can quickly discover interesting insights and learn what kinds of questions I can ask without having to think of queries myself

## Problem Statement
Users often struggle to think of meaningful queries when first exploring their data. They may not know what columns exist or what kinds of questions make sense for their dataset. This creates friction in the user experience and prevents users from getting value from the application quickly. Additionally, users may be unsure about the query syntax or phrasing that works best with the natural language-to-SQL conversion.

## Solution Statement
We will add a "✨ Generate Query" button positioned alongside the existing primary action buttons (Query and Upload Data) in the query controls section. This button will call a new backend endpoint `/api/generate-query` that uses the existing llm_processor.py module to generate contextually-aware natural language queries. The queries will be based on the current database schema, referencing actual table and column names, and will be limited to two sentences maximum. The button will use plaid styling to differentiate it from the primary Query button while maintaining visual consistency with the Upload Data button.

## Relevant Files
Use these files to implement the feature:

### Backend Files
- **app/server/core/llm_processor.py** - Contains the LLM integration logic. Will add new functions `generate_query_with_openai()`, `generate_query_with_anthropic()`, and `generate_natural_language_query()` to generate contextually-aware queries based on database schema. This module already has the OpenAI and Anthropic client setup patterns we can follow.

- **app/server/core/sql_processor.py** - Contains `get_database_schema()` function that provides table and column information needed to generate contextual queries.

- **app/server/server.py** - FastAPI application. Will add new endpoint `POST /api/generate-query` that calls the query generation logic and returns the generated natural language query.

- **app/server/core/data_models.py** - Contains Pydantic models for API requests/responses. Will add `GenerateQueryRequest` and `GenerateQueryResponse` models.

### Frontend Files
- **app/client/index.html** - Contains the main UI structure. Will add the new "✨ Generate Query" button in the `.query-controls` section using class `plaid-button`.

- **app/client/src/main.ts** - Contains the TypeScript application logic. Will add `initializeGenerateQuery()` function to handle button clicks, call the API, and populate the query input field.

- **app/client/src/api/client.ts** - Contains API client methods. Will add `generateQuery()` method to call the new backend endpoint.

- **app/client/src/style.css** - Contains all styling. Will add `.plaid-button` class for the button styling (gradient background similar to primary button but with distinct visual identity).

- **app/client/src/types.d.ts** - Contains TypeScript type definitions. Will add `GenerateQueryRequest` and `GenerateQueryResponse` interfaces.

### Test Files
- **app/server/tests/core/test_llm_processor.py** - Will add tests for the new query generation functions.

### New Files
- **.claude/commands/e2e/test_random_query_generator.md** - E2E test file that validates the random query generator button functionality, ensures queries are generated based on schema, verifies 2-sentence limit, confirms overwrite behavior, and validates the plaid styling.

## Implementation Plan

### Phase 1: Foundation
First, we'll extend the backend infrastructure to support query generation. This includes adding new Pydantic data models for the request/response, implementing the LLM query generation logic that analyzes database schema and creates contextually-aware queries, and creating a new FastAPI endpoint to expose this functionality. The query generation will leverage the existing LLM provider routing logic (OpenAI/Anthropic) already established in llm_processor.py.

### Phase 2: Core Implementation
Next, we'll implement the frontend UI components and integration. This includes adding the "✨ Generate Query" button to the HTML with plaid styling, implementing the TypeScript click handler that calls the backend API, adding the API client method, and ensuring the generated query overwrites (not appends to) the query input field. The button will display a loading state during API calls and handle errors gracefully.

### Phase 3: Integration
Finally, we'll ensure end-to-end integration works seamlessly. This includes verifying the button appears correctly positioned with other action buttons using flexbox justify-content: space-apart, testing the full flow from button click through API call to query population, validating error handling when no tables exist, ensuring the generated queries are executable by the existing query execution flow, and creating comprehensive E2E tests that validate the entire feature.

## Step by Step Tasks

### 1. Backend Data Models
- Add `GenerateQueryRequest` model to `app/server/core/data_models.py` (empty model, no parameters needed)
- Add `GenerateQueryResponse` model with fields: `query: str`, `tables_used: List[str]`, `error: Optional[str] = None`
- Write unit tests in `app/server/tests/core/test_query_generator.py` to validate the data models serialize/deserialize correctly

### 2. Backend Query Generation Logic
- Add `generate_query_with_openai(schema_info: Dict[str, Any]) -> str` function to `app/server/core/llm_processor.py`
  - Use OpenAI client to generate natural language queries based on schema
  - Include prompt instructions: max 2 sentences, reference actual table/column names, make it interesting and specific
  - Use higher temperature (0.8) for variety in query generation
  - Clean up response (remove quotes if present)
- Add `generate_query_with_anthropic(schema_info: Dict[str, Any]) -> str` function to `app/server/core/llm_processor.py`
  - Mirror OpenAI implementation but use Anthropic client
  - Use same prompt instructions and temperature settings
- Add `generate_natural_language_query(schema_info: Dict[str, Any]) -> str` function to `app/server/core/llm_processor.py`
  - Route to appropriate LLM provider (prioritize OpenAI if available, fall back to Anthropic)
  - Validate that schema_info contains tables (raise error if empty)
- Add comprehensive unit tests in `app/server/tests/core/test_llm_processor.py` covering:
  - Query generation with OpenAI
  - Query generation with Anthropic
  - Provider routing logic
  - Error handling when no tables exist
  - Validation that queries are limited to 2 sentences

### 3. Backend API Endpoint
- Add `POST /api/generate-query` endpoint to `app/server/server.py`
  - Accept `GenerateQueryRequest` (empty body)
  - Call `get_database_schema()` to get current schema
  - Return error response if no tables exist
  - Call `generate_natural_language_query(schema_info)`
  - Extract table names mentioned in query (simple string matching)
  - Return `GenerateQueryResponse` with query and tables_used
  - Include comprehensive error handling and logging
- Test endpoint manually using curl or Postman

### 4. Frontend TypeScript Types
- Add `GenerateQueryRequest` interface to `app/client/src/types.d.ts` (empty interface)
- Add `GenerateQueryResponse` interface with: `query: string`, `tables_used: string[]`, `error?: string`

### 5. Frontend API Client
- Add `generateQuery(): Promise<GenerateQueryResponse>` method to `app/client/src/api/client.ts`
  - Make POST request to `/generate-query` endpoint
  - Send empty JSON body
  - Return typed response

### 6. Frontend UI - Button HTML
- Add "✨ Generate Query" button to `app/client/index.html` in the `.query-controls` section
  - Use id `generate-query-button`
  - Use class `plaid-button`
  - Position after "Upload Data" button
  - Include sparkle emoji (✨) before "Generate Query" text

### 7. Frontend UI - Button Styling
- Verify `.plaid-button` styles exist in `app/client/src/style.css` (already exists based on codebase review)
- If needed, adjust positioning of `.query-controls` to ensure proper spacing with `justify-content: space-between` or `gap` property

### 8. Frontend Logic - Button Handler
- Add `initializeGenerateQuery()` function to `app/client/src/main.ts`
  - Get button element by id `generate-query-button`
  - Get query input element by id `query-input`
  - Add click event listener
  - On click:
    - Disable button
    - Show loading state (replace button content with loading spinner)
    - Call `api.generateQuery()`
    - On success: populate query input field with generated query (overwrite existing content)
    - On error: display error message using existing `displayError()` function
    - Re-enable button and restore original text
    - Focus query input field after population
- Call `initializeGenerateQuery()` from `DOMContentLoaded` event listener

### 9. E2E Test Creation
- Create `.claude/commands/e2e/test_random_query_generator.md` with test steps:
  - Navigate to application
  - Verify Generate Query button exists with plaid styling
  - Upload sample data (users table)
  - Click Generate Query button multiple times (3x)
  - Verify each generated query:
    - Is different from previous queries
    - References actual table/column names
    - Is in natural language (not SQL)
    - Is 2 sentences or less
    - Overwrites previous content in input field
  - Execute one generated query to verify it works
  - Take screenshots at each step
  - Include success criteria matching the feature requirements

### 10. Integration Testing
- Start server and client (`./scripts/start.sh`)
- Manually test the complete flow:
  - Upload sample data
  - Click Generate Query button
  - Verify query populates input field
  - Click button multiple times to verify variety
  - Execute generated query to ensure it works
  - Test error handling (try before uploading data)
- Fix any issues discovered during manual testing

### 11. Run Validation Commands
Execute all validation commands listed below to ensure zero regressions and feature works correctly

## Testing Strategy

### Unit Tests
- **Backend Models**: Test `GenerateQueryRequest` and `GenerateQueryResponse` serialization/deserialization
- **Query Generation Functions**: Test `generate_query_with_openai()`, `generate_query_with_anthropic()`, and `generate_natural_language_query()` with mocked LLM responses
- **Provider Routing**: Test that correct LLM provider is selected based on API key availability
- **Error Handling**: Test behavior when no tables exist, when API keys are missing, when LLM API calls fail
- **Query Validation**: Test that generated queries meet requirements (2 sentences max, reference schema, natural language)

### Integration Tests
- **API Endpoint**: Test `/api/generate-query` endpoint returns valid responses
- **Frontend Integration**: Test button click triggers API call and populates input field
- **End-to-End Flow**: Test complete user journey from uploading data to generating and executing queries

### Edge Cases
- **No tables in database**: Should return error message "No tables available. Please upload data first."
- **Empty schema**: Should handle gracefully
- **Multiple tables**: Should generate queries that may reference one or multiple tables
- **API key not configured**: Should return appropriate error message
- **LLM API failures**: Should propagate error to frontend with user-friendly message
- **Network errors**: Should display error without breaking UI
- **Rapid button clicking**: Button should be disabled during API call to prevent duplicate requests
- **Very long table/column names**: Should handle without breaking prompt

## Acceptance Criteria
- ✅ "✨ Generate Query" button appears in query controls section with plaid styling
- ✅ Button is positioned with justify-apart spacing from other buttons
- ✅ Clicking button calls `/api/generate-query` endpoint
- ✅ Generated queries are based on actual database schema (reference real table/column names)
- ✅ Generated queries are limited to 2 sentences maximum
- ✅ Generated queries are in natural language (not SQL syntax)
- ✅ Generated query overwrites (not appends) existing content in query input field
- ✅ Button shows loading state during API call (disabled with spinner)
- ✅ Multiple clicks generate different queries (variety via temperature=0.8)
- ✅ Error message displayed when no tables exist: "No tables available. Please upload data first."
- ✅ Generated queries can be successfully executed using the Query button
- ✅ Query input field receives focus after query is populated
- ✅ All existing tests pass with zero regressions
- ✅ New E2E test validates complete feature functionality
- ✅ Feature works with both OpenAI and Anthropic LLM providers

## Validation Commands
Execute every command to validate the feature works correctly with zero regressions.

- Read `.claude/commands/test_e2e.md` to understand how to execute E2E tests
- Read and execute `.claude/commands/e2e/test_random_query_generator.md` to validate the random query generator functionality works end-to-end
- `cd app/server && uv run pytest` - Run server tests to validate the feature works with zero regressions
- `cd app/server && uv run pytest tests/core/test_llm_processor.py -v` - Run LLM processor tests specifically to validate query generation
- `cd app/server && uv run pytest tests/core/test_query_generator.py -v` - Run query generator tests to validate data models
- `cd app/client && bun tsc --noEmit` - Run frontend type checking to validate TypeScript types are correct
- `cd app/client && bun run build` - Run frontend build to validate the feature works with zero regressions
- Manual validation: Start server and client, upload sample data, click Generate Query button 5 times, verify each query is different and references actual schema, execute one query to confirm it works

## Notes

### Design Decisions
- **Plaid Styling**: Using the existing plaid button style creates visual consistency with the Upload Data button while differentiating from the primary Query button. This indicates a secondary but important action.
- **Overwrite Behavior**: Always overwriting the query input (vs appending) provides a cleaner UX and matches user expectations for a "generate" action.
- **2 Sentence Limit**: Keeps queries concise and focused, improving readability and ensuring they fit well in the input field.
- **Temperature 0.8**: Higher temperature encourages variety in generated queries so users see different suggestions each time.
- **LLM Provider Routing**: Following existing pattern of prioritizing OpenAI, falling back to Anthropic, ensures consistency with the rest of the application.

### Future Enhancements
- Add query templates/categories (aggregations, filtering, joins, etc.) that users can select
- Store query history so users can revisit previously generated queries
- Add "like/dislike" feedback to improve query quality over time
- Support query complexity levels (simple, medium, complex)
- Generate multiple queries at once and let users choose
- Add tooltips explaining what each generated query does

### Security Considerations
- Query generation uses the same LLM providers as SQL generation, so security model is consistent
- Generated queries are natural language only (not SQL), so no SQL injection risk at this stage
- Users must manually execute queries, providing opportunity to review before execution
- Database schema information is already exposed via `/api/schema` endpoint, so no new security surface

### Performance Notes
- Query generation requires LLM API call (~500-2000ms depending on provider)
- Button disabled during generation prevents duplicate requests
- Loading state provides clear feedback during API call
- No caching implemented initially (each click generates fresh query for variety)

### API Key Configuration
- Feature requires either `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` environment variable
- Error message guides users to configure API key if missing
- Follows existing pattern in llm_processor.py for provider selection
