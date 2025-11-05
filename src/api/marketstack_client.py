# src/api/marketstack_client.py
from typing import Any, Dict
from .base_client import BaseApiClient

class MarketStackClient(BaseApiClient):
    def eod(self, symbols: str, limit: int = 5) -> Dict[str, Any]:
        """GET /v2/eod?symbols=...&limit=..."""
        return self.get("/v2/eod", params={"symbols": symbols, "limit": limit}).json()

    def eod_latest(self, symbols: str) -> Dict[str, Any]:
        """GET /v2/eod/latest?symbols=..."""
        return self.get("/v2/eod/latest", params={"symbols": symbols}).json()

    def exchanges(self, limit: int = 100) -> Dict[str, Any]:
        """GET /v2/exchanges?limit=..."""
        return self.get("/v2/exchanges", params={"limit": limit}).json()
