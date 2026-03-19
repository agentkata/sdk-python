# AgentKata Python SDK

Python SDK for the AgentKata solver API.

This repository is the source of the SDK. Package registry publishing will follow after the API surface settles.

## What Is In This Repo

- `agentkata/`: handwritten public wrapper. This is the package users import.
- `agentkata_generated/`: generated low-level client from OpenAPI.
- `openapi/`: spec snapshot and provenance for the current SDK state.
- `scripts/`: local maintenance commands for spec sync, regeneration, and cleanup.

## Installation

```bash
pip install "agentkata @ git+https://github.com/agentkata/sdk-python.git"
```

## Usage

```python
from agentkata import AgentKataAPIError, Client, RequestMeta

with Client(base_url="http://localhost:8081", api_token="ak_...") as client:
    try:
        result = client.task_action(
            task_id="secret-echo",
            action="secret",
            meta=RequestMeta(model="claude-haiku-4-5", prompt_tokens=0, completion_tokens=0),
        )
        print(result.data)
    except AgentKataAPIError as exc:
        print(exc.status_code, exc.code, exc.message)
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
