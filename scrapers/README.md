# FinMar Scrapers

Config-driven web scrapers for Moroccan financial data sources.

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

1. Copy `config_example.yml` to a new config file (e.g., `config_mysite.yml`)
2. Edit the configuration to match your target site's structure
3. Run the scraper:

```bash
python morocco_finance_scraper.py config_mysite.yml
```

### Configuration

The YAML configuration file defines:

- **Site settings**: URL, user agent, rate limiting, timeouts
- **Parsing rules**: CSS selectors for rows and fields
- **Field transforms**: `strip`, `float_maybe`, `int_maybe`, `datetime_maybe`
- **Output formats**: CSV, Parquet, PostgreSQL
- **Pagination**: Selector for "next page" link

Example configuration structure:

```yaml
site_name: "example_site"
start_url: "https://example.com/data"
user_agent: "FinMarBot/1.0"
rate_limit_seconds: 2
timeout_seconds: 15
max_retries: 3
parsing:
  row_selector: "table.data > tbody > tr"
  fields:
    field_name:
      selector: "td.class"
      attr: "text"  # or "href", "title", etc.
      transform: "strip"  # or "float_maybe", "int_maybe", "datetime_maybe"
output:
  csv: true
  parquet: true
  postgres: false
```

## Robots.txt Compliance

The scraper automatically checks and respects `robots.txt` rules for each site.

## Output

Data is saved to:
- CSV: `output/{site_name}_YYYYMMDD_HHMMSS.csv`
- Parquet: `output/{site_name}_YYYYMMDD_HHMMSS.parquet`
- PostgreSQL: As configured in `postgres_config`

## Development

Run tests:

```bash
pytest tests/
```

## Field Transforms

- `strip`: Remove leading/trailing whitespace
- `float_maybe`: Parse as float, return None on failure
- `int_maybe`: Parse as integer, return None on failure
- `datetime_maybe`: Parse as datetime using dateutil, return None on failure
