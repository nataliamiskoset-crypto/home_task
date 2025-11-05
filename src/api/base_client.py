# src/api/base_client.py
from typing import Any, Dict, Optional
import requests

class BaseApiClient:
    def __init__(self, base_url: str, access_key: str, timeout: int = 15):
        self.base_url = base_url.rstrip("/")
        self.access_key = access_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        params = dict(params or {})
        params["access_key"] = self.access_key
        resp = self.session.get(self._url(path), params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp
