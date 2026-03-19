"""Thin ergonomic wrapper over the generated solver client."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

from agentkata_generated.api.solver_api import SolverApi
from agentkata_generated.api_client import ApiClient
from agentkata_generated.configuration import Configuration
from agentkata_generated.exceptions import ApiException
from agentkata_generated.models.action_envelope import ActionEnvelope
from agentkata_generated.models.action_request import ActionRequest
from agentkata_generated.models.execution_meta import ExecutionMeta
from agentkata_generated.models.health_response import HealthResponse
from agentkata_generated.models.restart_envelope import RestartEnvelope
from agentkata_generated.models.submit_envelope import SubmitEnvelope
from agentkata_generated.models.submit_params import SubmitParams
from agentkata_generated.models.submit_request import SubmitRequest

from .errors import AgentKataAPIError

RequestMeta = ExecutionMeta
EnvelopeT = TypeVar('EnvelopeT', ActionEnvelope, RestartEnvelope, SubmitEnvelope)


class Client:
    """Client exposes a stable, small API for solver users."""

    def __init__(
        self,
        *,
        base_url: str,
        api_token: str,
    ) -> None:
        configuration = Configuration(
            host=_normalize_base_url(base_url),
            access_token=api_token,
        )
        self._api_client = ApiClient(configuration=configuration)
        self._solver_api = SolverApi(api_client=self._api_client)

    def __enter__(self) -> Client:
        return self

    def __exit__(self, _exc_type: object, _exc_value: object, _traceback: object) -> None:
        self.close()

    def close(self) -> None:
        pool_manager = getattr(self._api_client.rest_client, 'pool_manager', None)
        if pool_manager is not None and hasattr(pool_manager, 'clear'):
            pool_manager.clear()

    def health(self) -> HealthResponse:
        return self._solver_api.get_health()

    def task_action(
        self,
        *,
        task_id: str,
        action: str,
        payload: dict[str, Any] | None = None,
        meta: RequestMeta | None = None,
    ) -> ActionEnvelope:
        return _call_solver(
            self._solver_api.task_action,
            task_id=task_id,
            action=action,
            action_request=ActionRequest(params=payload or {}, meta=meta),
        )

    def submit_task(
        self,
        *,
        task_id: str,
        answer: Any,
        meta: RequestMeta | None = None,
    ) -> SubmitEnvelope:
        return _call_solver(
            self._solver_api.submit_task,
            task_id=task_id,
            submit_request=SubmitRequest(
                params=SubmitParams(answer=answer),
                meta=meta,
            ),
        )

    def restart_task(self, *, task_id: str) -> RestartEnvelope:
        return _call_solver(self._solver_api.restart_task, task_id=task_id)

    def track_task_action(
        self,
        *,
        track_id: str,
        task_id: str,
        action: str,
        payload: dict[str, Any] | None = None,
        meta: RequestMeta | None = None,
    ) -> ActionEnvelope:
        return _call_solver(
            self._solver_api.track_task_action,
            track_id=track_id,
            task_id=task_id,
            action=action,
            action_request=ActionRequest(params=payload or {}, meta=meta),
        )

    def submit_track_task(
        self,
        *,
        track_id: str,
        task_id: str,
        answer: Any,
        meta: RequestMeta | None = None,
    ) -> SubmitEnvelope:
        return _call_solver(
            self._solver_api.submit_track_task,
            track_id=track_id,
            task_id=task_id,
            submit_request=SubmitRequest(
                params=SubmitParams(answer=answer),
                meta=meta,
            ),
        )

    def restart_track(self, *, track_id: str) -> RestartEnvelope:
        return _call_solver(self._solver_api.restart_track, track_id=track_id)


def _call_solver(operation: Callable[..., EnvelopeT], /, **kwargs: Any) -> EnvelopeT:
    try:
        return operation(**kwargs)
    except ApiException as exc:
        raise AgentKataAPIError.from_generated(exc) from exc


def _normalize_base_url(base_url: str) -> str:
    trimmed = base_url.rstrip('/')
    if trimmed.endswith('/api/agent'):
        return trimmed
    return f'{trimmed}/api/agent'
