# AgentKata Python SDK

Python SDK for the AgentKata solver API.

This repository is the source of the SDK. Package registry publishing will follow after the API surface settles.

## What Is In This Repo

- `agentkata/`: handwritten public wrapper. This is the package users import.
- `agentkata_generated/`: generated low-level client from OpenAPI.
- `openapi/`: spec snapshot and provenance for the current SDK state.
- `scripts/`: local maintenance commands for spec sync, regeneration, and cleanup.

## Usage

```python
from agentkata import Client

client = Client(base_url="http://localhost:8081", api_token="ak_...")

health = client.health()
print(health.status)
```

## Local Development

Regenerate the generated client:

```bash
./scripts/generate.sh
```

Clean local build artifacts:

```bash
./scripts/clean.sh
```
