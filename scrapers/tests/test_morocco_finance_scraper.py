#!/usr/bin/env python3
"""
Tests for morocco_finance_scraper.py
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import the scraper module
sys.path.insert(0, str(Path(__file__).parent.parent))

from bs4 import BeautifulSoup
from morocco_finance_scraper import parse_row, apply_transform


def test_parse_row_from_sample_page():
    """Test parsing a row from the sample HTML fixture."""
    # Load the sample HTML
    sample_html_path = Path(__file__).parent / "sample_page.html"
    with open(sample_html_path, 'r') as f:
        html_content = f.read()
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Find the first row
    row = soup.select_one("table.market-table > tbody > tr")
    assert row is not None, "Could not find row in sample page"
    
    # Define field configuration matching config_example.yml
    fields_config = {
        'symbol': {
            'selector': 'td.symbol',
            'attr': 'text',
            'transform': 'strip'
        },
        'name': {
            'selector': 'td.name',
            'attr': 'text',
            'transform': 'strip'
        },
        'price': {
            'selector': 'td.price',
            'attr': 'text',
            'transform': 'float_maybe'
        },
        'change': {
            'selector': 'td.change',
            'attr': 'text',
            'transform': 'strip'
        },
        'market_time': {
            'selector': 'td.time',
            'attr': 'text',
            'transform': 'datetime_maybe'
        }
    }
    
    # Parse the row
    result = parse_row(row, fields_config)
    
    # Assert the parsed values
    assert result['symbol'] == 'ABC', f"Expected symbol 'ABC', got {result['symbol']}"
    assert result['name'] == 'Banque A', f"Expected name 'Banque A', got {result['name']}"
    assert result['price'] == 123.45, f"Expected price 123.45, got {result['price']}"
    assert isinstance(result['price'], float), f"Expected price to be float, got {type(result['price'])}"
    assert result['change'] == '+1.23%', f"Expected change '+1.23%', got {result['change']}"
    
    # Check datetime parsing
    assert result['market_time'] is not None, "market_time should not be None"
    assert isinstance(result['market_time'], datetime), f"Expected market_time to be datetime, got {type(result['market_time'])}"
    assert result['market_time'].year == 2025, f"Expected year 2025, got {result['market_time'].year}"
    assert result['market_time'].month == 12, f"Expected month 12, got {result['market_time'].month}"
    assert result['market_time'].day == 9, f"Expected day 9, got {result['market_time'].day}"
    
    print("All assertions passed!")


def test_apply_transform_strip():
    """Test strip transform."""
    assert apply_transform("  hello  ", "strip") == "hello"
    assert apply_transform("test", "strip") == "test"


def test_apply_transform_float():
    """Test float_maybe transform."""
    assert apply_transform("123.45", "float_maybe") == 123.45
    assert apply_transform("1,234.56", "float_maybe") == 1234.56
    assert apply_transform("$99.99", "float_maybe") == 99.99
    assert apply_transform("invalid", "float_maybe") is None


def test_apply_transform_int():
    """Test int_maybe transform."""
    assert apply_transform("123", "int_maybe") == 123
    assert apply_transform("1,234", "int_maybe") == 1234
    assert apply_transform("invalid", "int_maybe") is None


def test_apply_transform_datetime():
    """Test datetime_maybe transform."""
    result = apply_transform("2025-12-09 15:30:00", "datetime_maybe")
    assert result is not None
    assert isinstance(result, datetime)
    assert result.year == 2025
    assert result.month == 12
    assert result.day == 9
    assert apply_transform("invalid", "datetime_maybe") is None


if __name__ == '__main__':
    test_apply_transform_strip()
    test_apply_transform_float()
    test_apply_transform_int()
    test_apply_transform_datetime()
    test_parse_row_from_sample_page()
    print("\nAll tests passed!")
