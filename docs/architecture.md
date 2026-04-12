# Architecture

> *Describe your system design, data flow, AI pipeline, and key tradeoffs. Commander Kapoor reads this — make it count.*

## System Overview

<!-- High-level description of your solution architecture. What components does your system have? How do they interact? -->

## AI Pipeline

<!-- How does your triage logic work? What models do you use? How do you structure prompts? Do you use chain-of-thought, few-shot examples, or multi-step reasoning? -->

## Data Flow

<!-- Walk through what happens from the moment a signal hits `POST /triage` to when the response is returned. Include any preprocessing, model calls, postprocessing, and validation steps. -->

## API Design

<!-- How did you structure your FastAPI (or other framework) application? What middleware, error handling, and validation do you use? -->

### Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | Health check — returns 200 if the service is alive |
| `/triage` | POST | Accepts a signal, returns a triage decision |

### Response Headers

<!-- Do you include X-Model-Name, X-Prompt-Tokens, X-Completion-Tokens for cost tracking? -->

## Infrastructure

<!-- How is your solution deployed? What cloud services, containers, or platforms do you use? Include a deployment diagram if helpful. -->

## Key Tradeoffs

<!-- What decisions did you make and why? Model size vs. latency? Accuracy vs. cost? Complexity vs. maintainability? What would you change if this were going to production for real? -->

## What I'd Change for Production

<!-- If Commander Kapoor called tomorrow and said "ship it to all 6 teams," what would you change? Caching? Rate limiting? Monitoring? Multi-region? Be honest. -->
