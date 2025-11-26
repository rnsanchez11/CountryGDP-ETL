#!/usr/bin/env python3
"""etl.py
Standalone ETL script for Country GDP data.
Run: python etl.py
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import logging
import sys
from pathlib import Path

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def log_progress(message):
    logger.info(message)

def extract(url: str) -> pd.DataFrame:
    log_progress(f"Extracting data from {url}")
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    table = soup.find('table')
    if table is None:
        raise RuntimeError('Table not found on page')
    df = pd.read_html(str(table))[0]
    log_progress(f"Extraction complete: {len(df)} rows retrieved")
    return df

def transform(df: pd.DataFrame) -> pd.DataFrame:
    log_progress('Starting transform step')
    df.columns = [str(c).strip().replace('\n', ' ') for c in df.columns]
    # detect GDP column
    gdp_col = None
    for c in df.columns:
        if 'GDP' in c or 'Nominal' in c:
            gdp_col = c
            break
    if gdp_col is None:
        raise RuntimeError('GDP column not detected')
    df[gdp_col] = (
        df[gdp_col]
        .astype(str)
        .str.replace('[\$,]', '', regex=True)
        .str.replace(',', '', regex=False)
        .str.extract(r'([0-9\.]+)', expand=False)
        .astype(float)
    )
    df = df.rename(columns={gdp_col: 'GDP_USD_2024'})
    df = df.loc[:, ~df.columns.duplicated()]
    log_progress('Transform step complete')
    return df

def load(df: pd.DataFrame, db_path: str = 'gdp_data.db'):
    log_progress(f'Loading data into {db_path}')
    conn = sqlite3.connect(db_path)
    df.to_sql('country_gdp', conn, if_exists='replace', index=False)
    conn.close()
    log_progress('Load complete')

def main():
    url = 'https://www.worldometers.info/gdp/gdp-by-country/'
    df = extract(url)
    df2 = transform(df)
    load(df2)
    log_progress('ETL pipeline finished successfully')

if __name__ == '__main__':
    main()
