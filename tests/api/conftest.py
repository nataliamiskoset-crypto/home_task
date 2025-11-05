# tests/conftest.py
import os
import pytest
from dotenv import load_dotenv
from src.api.marketstack_client import MarketStackClient

load_dotenv()

def pytest_addoption(parser):
    parser.addoption(
        "--marketstack-key",
        action="store",
        default="2ffd6c350f75578c656c863d214f08ef",
        help="MarketStack API key (or env MARKETSTACK_API_KEY)",
    )

@pytest.fixture(scope="session")
def api_key(pytestconfig) -> str:
    key = pytestconfig.getoption("--marketstack-key") or os.getenv("MARKETSTACK_API_KEY")
    if not key:
        pytest.skip("Missing MarketStack API key. Set env MARKETSTACK_API_KEY or use --marketstack-key.")
    return key

@pytest.fixture(scope="session")
def marketstack(api_key) -> MarketStackClient:
    return MarketStackClient(base_url="https://api.marketstack.com", access_key=api_key)
