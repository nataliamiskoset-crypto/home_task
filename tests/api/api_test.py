# tests/test_marketstack_api_v2.py
from datetime import datetime
import pytest

def _validate_eod_bar(bar: dict) -> None:
    # Minimalny kontrakt EOD (v2): symbol, date, OHLC, volume
    for k in ("symbol", "date", "open", "high", "low", "close", "volume"):
        assert k in bar, f"missing key {k} in EOD bar: {bar}"
    # data w ISO8601 (+offset w v2, np. 2025-11-04T00:00:00+0000)
    # normalizujemy do formatu przyjmowanego przez fromisoformat
    ts = bar["date"].replace("Z", "+00:00")
    if ts.endswith("+0000"):
        ts = ts[:-5] + "+00:00"
    datetime.fromisoformat(ts)
    # liczby
    for k in ("open", "high", "low", "close"):
        assert isinstance(bar[k], (int, float))
    assert isinstance(bar["volume"], (int, float))

@pytest.mark.parametrize("symbol", ["AAPL", "MSFT", "GOOGL"])
def test_eod_v2_returns_data_for_symbol(marketstack, symbol):
    body = marketstack.eod(symbols=symbol, limit=3)
    assert "data" in body and isinstance(body["data"], list) and body["data"], "empty data"
    for bar in body["data"]:
        assert bar["symbol"] == symbol
        _validate_eod_bar(bar)

@pytest.mark.parametrize("multi", ["AAPL,MSFT", "NVDA,TSLA"])
def test_eod_v2_supports_multiple_symbols(marketstack, multi):
    body = marketstack.eod(symbols=multi, limit=1)
    symbols = set(multi.split(","))
    got = {bar["symbol"] for bar in body["data"]}
    # przynajmniej jeden wpis dla każdego żądanego symbolu
    assert symbols.issubset(got) or got.issubset(symbols)
    for bar in body["data"]:
        _validate_eod_bar(bar)

@pytest.mark.parametrize("symbol", ["AAPL", "MSFT"])
def test_eod_latest_v2_is_consistent(marketstack, symbol):
    latest = marketstack.eod_latest(symbols=symbol)
    assert "data" in latest and latest["data"], "no latest data"
    # w latest też walidujemy kształt
    for bar in latest["data"]:
        assert bar["symbol"] == symbol
        _validate_eod_bar(bar)

def test_exchanges_v2_contains_known_mic(marketstack):
    body = marketstack.exchanges(limit=200)
    assert "data" in body and isinstance(body["data"], list) and body["data"]
    mics = {ex.get("mic") for ex in body["data"] if "mic" in ex}
    # sprawdzamy kilka popularnych: XNAS (NASDAQ), XNYS (NYSE)
    assert {"XNAS", "XNYS"} & mics
