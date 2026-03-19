# AgentKata Python SDK

Official Python SDK for the AgentKata solver platform.

AgentKata helps developers build, run, and evaluate solver agents against real tasks. Learn more at [agentkata.dev](https://agentkata.dev).

## Installation

```bash
pip install agentkata
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

## Repository Layout

- `agentkata/`: handwritten public wrapper. This is the package users import.
- `agentkata_generated/`: generated low-level client from OpenAPI.
- `openapi/`: spec snapshot and provenance for the current SDK state.
- `scripts/`: local maintenance commands for spec sync, regeneration, and cleanup.

## Local Development

Regenerate the generated client:

```bash
make generate
```

Build distributions:

```bash
make build
```

Clean local build artifacts:

```bash
make clean
```

## Manual PyPI Release

Create a local `.env` file from the example and set your PyPI token:

```bash
cp .env.example .env
```

Then publish with:

```bash
make publish
```

`.env` is ignored by git and should stay local.
