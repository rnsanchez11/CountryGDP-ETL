# Country GDP ETL Pipeline

**Short Summary**  
A compact, production-oriented ETL project that extracts GDP data from a public source, transforms and cleans the dataset, and stores it in a SQLite database. This repository is designed for recruiters and technical reviewers: clear structure, documented steps, and a runnable script.

## Project Contents
- `Project.ipynb` — polished Jupyter Notebook with explanations and step-by-step execution.
- `etl.py` — standalone ETL script to run the pipeline from the command line.
- `requirements.txt` — project dependencies.
- `.github/workflows/etl.yml` — CI workflow that runs the ETL script on push (basic smoke test).
- `.gitignore` — recommended ignores for Git.
- `gdp_data.db` — (not included) will be created when running the pipeline.

## Key Features
- Logging with timestamps for traceability
- Defensive web scraping (timeout and checks)
- Clean transforms and column hygiene
- SQLite persistence for easy inspection and portability

## How to run (local)
1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the pipeline:
   ```bash
   python etl.py
   ```
4. Explore results:
   - A SQLite DB named `gdp_data.db` will be created in the repository root.
   - Use `sqlite3 gdp_data.db` or tools like DB Browser for SQLite to inspect the `country_gdp` table.

## Notes for Recruiters
- This project demonstrates web scraping, data cleaning, logging, and database integration.
- It is intentionally compact so employers can quickly run and review the pipeline.
- The notebook includes explanatory cells and outputs for transparency.

## Next steps / Extensions
- Add unit tests and a Dockerfile for reproducible environments.
- Push final dataset to a cloud storage bucket (S3, GCS).
- Add a scheduler (GitHub Actions/time-based) to refresh the dataset periodically.
