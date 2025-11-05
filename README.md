# Selenium Python Home Task

## ⚙️ Setup Instructions

### Clone the project

```bash
git clone 
cd selenium-python-example
```

### Create and activate a virtual environment then Install project dependencies

#### For Windows:
```bash
pip install uv
uv venv
.\env\Scripts\activate
uv sync --all-extras --dev
```

#### For Mac:
```bash
python3 -m pip install uv
uv venv
source .venv/bin/activate
uv sync --all-extras --dev
```

## 🏃‍♂️ Running Tests

```bash
pytest --driver <firefox/chrome_headless> --device=<iPhone SE/Galaxy S20 Ultra>
```

When no browser was selected then chrome will be used by default.

## 📊 Viewing Test Results

### Install Allure Commandline To View Test results

#### For Windows:

Allure documentations [here](https://allurereport.org/) 

```bash
scoop install allure
```

#### For Mac:

```bash
brew install allure
```

### View Results Locally:

```bash
allure serve allure-results
```

### API 

## 🧪 Automated API Tests — Marketstack API v2

Below is the summary of automated test cases implemented for the **Marketstack API (v2)**  
based on the official documentation: [https://docs.apilayer.com/marketstack/docs/marketstack-api-v2-v-2-0-0](https://docs.apilayer.com/marketstack/docs/marketstack-api-v2-v-2-0-0)

| # | Test Name | Endpoint | Method | Validation Performed | Purpose / Description |
|---|------------|-----------|---------|----------------------|-----------------------|
| **1** | `test_eod_v2_returns_data_for_symbol` | `/v2/eod?symbols={symbol}` | `GET` | ✅ Verifies non-empty `data[]` list<br>✅ Confirms correct `symbol` in response<br>✅ Validates presence and types of fields: `date`, `open`, `high`, `low`, `close`, `volume`<br>✅ Checks timestamp format (ISO 8601) | Ensures historical End-of-Day (EOD) data is correctly returned for a single stock symbol. |
| **2** | `test_eod_v2_supports_multiple_symbols` | `/v2/eod?symbols=AAPL,MSFT` | `GET` | ✅ Validates data for multiple symbols<br>✅ Confirms each symbol exists in the response<br>✅ Checks numeric OHLC values | Confirms API supports comma-separated symbol queries and returns data for each. |
| **3** | `test_eod_latest_v2_is_consistent` | `/v2/eod/latest?symbols={symbol}` | `GET` | ✅ Validates `data[]` non-empty<br>✅ Ensures `symbol` matches request<br>✅ Validates EOD structure and ISO date | Checks that latest EOD data matches API contract and symbol consistency. |
| **4** | `test_exchanges_v2_contains_known_mic` | `/v2/exchanges` | `GET` | ✅ Verifies exchange list is not empty<br>✅ Ensures MIC identifiers (e.g., XNAS, XNYS) exist | Confirms that the list of exchanges is returned correctly and includes major ones. |

---

### 🔍 Test Validation Strategy

Each test validates:
- API structure (keys like `data`, `symbol`, `open`, `close`, `volume`)
- Data type correctness (numbers, timestamps)
- Response consistency between single and multi-symbol queries
- Coverage of both historical (`/v2/eod`) and latest (`/v2/eod/latest`) endpoints

| Validation Type                 | Description                                                                                               | Reason for Use                                                                                             |
| ------------------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Key presence validation**     | Every test checks for expected JSON keys (`symbol`, `date`, `open`, `close`, etc.) using assertions.      | Detects incomplete or malformed responses, ensuring data structure matches API contract.                   |
| **Data type validation**        | Confirms numeric fields (`open`, `high`, `low`, `close`, `volume`) are integers or floats.                | Prevents silent type mismatches (e.g., values returned as strings). Ensures consistency for calculations.  |
| **Timestamp format validation** | Normalizes `date` field (e.g., `2025-11-04T00:00:00+0000`) and validates with `datetime.fromisoformat()`. | Ensures all date fields follow ISO 8601 standard with timezone offset. Prevents downstream parsing errors. |
| **Response completeness**       | Asserts `data[]` list is not empty and contains expected number of records.                               | Guarantees the API actually returns usable data and prevents false positives.                              |
| **Symbol consistency**          | Checks that returned symbols match the requested ones, even for multi-symbol queries.                     | Detects incorrect filtering or backend errors that return wrong data sets.                                 |
| **Known MIC validation**        | Verifies presence of known exchange codes like `XNAS` (NASDAQ) and `XNYS` (NYSE).                         | Serves as a sanity check to ensure exchange metadata coverage and proper mapping.                          |

---

### 🧰 How to Run the Tests

1️⃣ **Set your API key**  
```bash
export MARKETSTACK_API_KEY="your_api_key_here"
```
2️⃣ **Run pytest**  
```bash 
pytest -vv tests/test_marketstack_api_v2.py
```

### ✅ Expected Output Example
```bash 
tests/test_marketstack_api_v2.py::test_eod_v2_returns_data_for_symbol[AAPL] PASSED
tests/test_marketstack_api_v2.py::test_eod_v2_supports_multiple_symbols[AAPL,MSFT] PASSED
tests/test_marketstack_api_v2.py::test_eod_latest_v2_is_consistent[MSFT] PASSED
tests/test_marketstack_api_v2.py::test_exchanges_v2_contains_known_mic PASSED
```