#!/usr/bin/env python3
"""
Config-driven web scraper for Moroccan financial data sources.
Supports BeautifulSoup parsing, multiple output formats, and robots.txt compliance.
"""

import sys
import time
import yaml
import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse
from pathlib import Path
from datetime import datetime
from dateutil import parser as dateutil_parser
import pandas as pd
from tqdm import tqdm


def load_config(config_path):
    """Load YAML configuration file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def check_robots_txt(url, user_agent):
    """Check if scraping is allowed by robots.txt."""
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    
    rp = RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception as e:
        print(f"Warning: Could not read robots.txt: {e}")
        return True  # Assume allowed if robots.txt is unavailable


def apply_transform(value, transform):
    """Apply a transform function to a value."""
    if value is None:
        return None
    
    if transform == "strip":
        return value.strip() if isinstance(value, str) else value
    elif transform == "float_maybe":
        try:
            # Remove common currency symbols and commas
            cleaned = value.replace(',', '').replace('$', '').replace('€', '').replace('MAD', '').strip()
            return float(cleaned)
        except (ValueError, AttributeError):
            return None
    elif transform == "int_maybe":
        try:
            cleaned = value.replace(',', '').strip()
            return int(cleaned)
        except (ValueError, AttributeError):
            return None
    elif transform == "datetime_maybe":
        try:
            return dateutil_parser.parse(value)
        except (ValueError, AttributeError, TypeError):
            return None
    else:
        return value


def extract_field(row, field_config):
    """Extract a field from a row element using the field configuration."""
    selector = field_config.get('selector')
    attr = field_config.get('attr', 'text')
    transform = field_config.get('transform')
    
    element = row.select_one(selector)
    if not element:
        return None
    
    # Extract the attribute
    if attr == 'text':
        value = element.get_text()
    else:
        value = element.get(attr)
    
    # Apply transform
    if transform:
        value = apply_transform(value, transform)
    
    return value


def parse_row(row, fields_config):
    """Parse a single row element into a dictionary."""
    result = {}
    for field_name, field_config in fields_config.items():
        result[field_name] = extract_field(row, field_config)
    return result


def fetch_page(url, config):
    """Fetch a page with retry logic."""
    headers = {
        'User-Agent': config.get('user_agent', 'FinMarBot/1.0')
    }
    
    timeout = config.get('timeout_seconds', 15)
    max_retries = config.get('max_retries', 3)
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise


def scrape_page(url, config):
    """Scrape a single page and return parsed data."""
    # Check robots.txt
    if not check_robots_txt(url, config.get('user_agent', 'FinMarBot/1.0')):
        raise PermissionError(f"Scraping not allowed by robots.txt: {url}")
    
    # Fetch the page
    response = fetch_page(url, config)
    soup = BeautifulSoup(response.content, 'lxml')
    
    # Parse rows
    parsing_config = config['parsing']
    row_selector = parsing_config['row_selector']
    fields_config = parsing_config['fields']
    
    rows = soup.select(row_selector)
    data = []
    for row in rows:
        parsed_row = parse_row(row, fields_config)
        data.append(parsed_row)
    
    # Check for next page
    next_page_selector = config.get('pagination', {}).get('next_page_selector')
    next_url = None
    if next_page_selector:
        next_link = soup.select_one(next_page_selector)
        if next_link:
            next_url = urljoin(url, next_link.get('href'))
    
    return data, next_url


def save_data(df, config):
    """Save data to configured output formats."""
    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)
    
    site_name = config['site_name']
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_filename = f"{site_name}_{timestamp}"
    
    output_config = config.get('output', {})
    
    # Save to CSV
    if output_config.get('csv', False):
        csv_path = output_dir / f"{base_filename}.csv"
        df.to_csv(csv_path, index=False)
        print(f"Saved CSV: {csv_path}")
    
    # Save to Parquet
    if output_config.get('parquet', False):
        parquet_path = output_dir / f"{base_filename}.parquet"
        df.to_parquet(parquet_path, index=False)
        print(f"Saved Parquet: {parquet_path}")
    
    # Save to PostgreSQL
    if output_config.get('postgres', False):
        postgres_config = output_config.get('postgres_config', {})
        uri = postgres_config.get('uri')
        table_name = postgres_config.get('table_name')
        
        if uri and table_name:
            from sqlalchemy import create_engine
            engine = create_engine(uri)
            df.to_sql(table_name, engine, if_exists='append', index=False)
            print(f"Saved to PostgreSQL table: {table_name}")


def main(config_path):
    """Main scraper function."""
    config = load_config(config_path)
    
    print(f"Starting scraper for: {config['site_name']}")
    print(f"Start URL: {config['start_url']}")
    
    all_data = []
    current_url = config['start_url']
    rate_limit = config.get('rate_limit_seconds', 2)
    
    page_count = 0
    while current_url:
        page_count += 1
        print(f"\nScraping page {page_count}: {current_url}")
        
        try:
            data, next_url = scrape_page(current_url, config)
            all_data.extend(data)
            print(f"Parsed {len(data)} rows")
            
            current_url = next_url
            
            # Rate limiting
            if current_url:
                time.sleep(rate_limit)
        
        except Exception as e:
            print(f"Error scraping page: {e}")
            break
    
    # Convert to DataFrame and save
    if all_data:
        df = pd.DataFrame(all_data)
        print(f"\nTotal rows scraped: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        save_data(df, config)
    else:
        print("No data scraped")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python morocco_finance_scraper.py <config.yml>")
        sys.exit(1)
    
    main(sys.argv[1])
