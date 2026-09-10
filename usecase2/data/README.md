Data folder

- `data/raw` - raw ingested files (contains clearly labeled synthetic data for development)
- `data/processed` - staging/parquet files from ingestion
- `data/gold` - star-schema gold tables (facts & dims)

Synthetic data files are labeled `SYNTHETIC_*` and must not be represented as real data.
