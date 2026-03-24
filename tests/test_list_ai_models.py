"""Tests for the ListAIModels gRPC RPC and gateway REST endpoint."""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock, patch

from apme.v1.primary_pb2 import ListAIModelsRequest
from apme_engine.daemon.primary_server import PrimaryServicer


@dataclass
class _FakeModel:
    """Minimal stand-in for abbenay_grpc.Model.

    Attributes:
        id: Model identifier.
        provider: LLM provider name.
        name: Human-readable model name.
        supports_streaming: Whether the model supports streaming.
        supports_tools: Whether the model supports tool calling.
    """

    id: str
    provider: str
    name: str
    supports_streaming: bool = True
    supports_tools: bool = True


class _FakeAbbenayClient:
    """Stand-in for AbbenayClient with a canned model list.

    Args:
        models: Pre-configured model list to return from list_models().
    """

    def __init__(self, models: list[_FakeModel]) -> None:
        self._models = models

    async def connect(self) -> None:
        pass

    async def disconnect(self) -> None:
        pass

    async def list_models(self) -> list[_FakeModel]:
        return self._models


# ---------------------------------------------------------------------------
# Primary.ListAIModels
# ---------------------------------------------------------------------------


class TestPrimaryListAIModels:
    """Test the ListAIModels gRPC method on PrimaryServicer."""

    def test_returns_models_from_abbenay(self) -> None:
        """ListAIModels returns models when Abbenay is reachable."""
        models = [
            _FakeModel(id="openai/gpt-4o", provider="openai", name="gpt-4o"),
            _FakeModel(id="anthropic/claude-sonnet-4", provider="anthropic", name="claude-sonnet-4"),
        ]
        fake_client = _FakeAbbenayClient(models)

        with (
            patch.dict(os.environ, {"APME_ABBENAY_ADDR": "127.0.0.1:50057"}),
            patch("abbenay_grpc.AbbenayClient", return_value=fake_client),
        ):
            servicer = PrimaryServicer()
            ctx = MagicMock()
            resp = asyncio.run(servicer.ListAIModels(ListAIModelsRequest(), ctx))

        assert len(resp.models) == 2
        assert resp.models[0].id == "openai/gpt-4o"
        assert resp.models[1].provider == "anthropic"

    def test_returns_empty_when_no_addr(self) -> None:
        """ListAIModels returns empty list when APME_ABBENAY_ADDR is not set."""
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("APME_ABBENAY_ADDR", None)
            servicer = PrimaryServicer()
            ctx = MagicMock()
            resp = asyncio.run(servicer.ListAIModels(ListAIModelsRequest(), ctx))

        assert len(resp.models) == 0

    def test_returns_empty_when_abbenay_unreachable(self) -> None:
        """ListAIModels returns empty list when Abbenay connection fails."""
        failing_client = AsyncMock()
        failing_client.connect = AsyncMock(side_effect=ConnectionError("refused"))

        with patch.dict(os.environ, {"APME_ABBENAY_ADDR": "127.0.0.1:50057"}):
            with patch("abbenay_grpc.AbbenayClient", return_value=failing_client):
                servicer = PrimaryServicer()
                ctx = MagicMock()
                resp = asyncio.run(servicer.ListAIModels(ListAIModelsRequest(), ctx))

        assert len(resp.models) == 0

    def test_returns_empty_when_client_not_installed(self) -> None:
        """ListAIModels returns empty list when abbenay_grpc is not installed."""
        with (
            patch.dict(os.environ, {"APME_ABBENAY_ADDR": "127.0.0.1:50057"}),
            patch.dict("sys.modules", {"abbenay_grpc": None}),
        ):
            servicer = PrimaryServicer()
            ctx = MagicMock()
            resp = asyncio.run(servicer.ListAIModels(ListAIModelsRequest(), ctx))

        assert len(resp.models) == 0
