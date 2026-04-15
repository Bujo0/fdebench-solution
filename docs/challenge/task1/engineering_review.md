# Task 1 — Engineering Review

What judges look for in your triage code. Tier 2 doesn't affect the leaderboard, but it's how finalists get picked.

## Code Quality (25% of Tier 2)

| Dimension | What judges look for |
|---|---|
| Structure (25%) | Triage engine in its own module, separate from the route handler. System prompt separate from API code. Models in a separate file from business logic. |
| Type safety (20%) | Category, Priority, Team, and MissingInfo defined as proper enums. Response modeled as a Pydantic model, not a raw dict. |
| Error handling (15%) | LLM failures handled gracefully (retry, fallback, meaningful error). API errors domain-coded, not generic 500s. |
| Testing (25%) | Unit tests for scoring logic, model validation, and API endpoint. LLM client mocked. Adversarial-style inputs tested. |
| Readability (15%) | System prompt readable and well-commented. Enum values self-documenting. Code navigable. |

## Architecture Design (30% of Tier 2)

| Dimension | What judges look for |
|---|---|
| AI pipeline (30%) | LLM interaction properly abstracted. Prompt separate from transport. Clear decision between tool calling and content parsing. |
| Decomposition (25%) | Routes → Engine → LLM Client layering. Settings separate from code. Models separate from business logic. |
| API design (20%) | `POST /triage` follows the contract. Proper status codes. Input validation before LLM call. Cost headers returned. |
| Trade-off reasoning (15%) | Awareness of model selection trade-offs. Prompt tuned for the task, not generic. |
| Scalability (10%) | Can handle concurrent signals. LLM client async. Connection pooling or load balancing considered. |

## Engineering Maturity (20% of Tier 2)

| Dimension | What judges look for |
|---|---|
| Deployment (30%) | Dockerfile exists. Deployable to a container platform. Server configured correctly. |
| Config and secrets (25%) | API keys in env vars via settings, not hardcoded. `.env.example` present. |
| Observability (20%) | Structured logging (not `print()`). Health check at `/health`. LLM usage tracked in response headers. |
| Security (25%) | No secrets in source code. Input validation to prevent prompt injection. HTTPS validation on external URLs. |

## Tips

- System prompt is the dominant token cost — prompt caching helps a lot.
- Tool calling (structured output) is usually more efficient than asking for JSON in the body.
- Triage is one LLM call per request. The differentiator is prompt quality and model choice.
