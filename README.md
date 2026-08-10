# Crypto Market Tracker

This project fetches public crypto price data from CoinGecko and appends it to `data/prices.csv`. It also writes a summary table to the GitHub Actions job summary when run in CI.

## What it does

- Fetches the current USD price and 24 hour change for Bitcoin, Ethereum, and Solana.
- Appends the results to `data/prices.csv` with a UTC timestamp.
- Publishes a readable summary in the GitHub Actions run output.

## Requirements

- Python 3.11 or newer
- Internet access for CoinGecko API requests

Install the dependency with:

```bash
pip install -r requirements.txt
```

## Run locally

1. Install dependencies.
2. Run the script:

```bash
python main.py
```

The script will print the latest prices to the terminal and append a new row set to `data/prices.csv`.

## Run with GitHub Actions

The workflow file is located at [`.github/workflows/run_tracker.yml`](.github/workflows/run_tracker.yml).

It is configured to:

- Run automatically every 15 minutes.
- Run manually from the GitHub Actions tab using workflow dispatch.
- Commit updated `data/prices.csv` back to the repository.

### Enable and use the workflow

1. Push this repository to GitHub.
2. Open the repository in GitHub and go to the Actions tab.
3. Make sure Actions are enabled for the repo.
4. Select the "Crypto Market Tracker" workflow.
5. Choose one of the following:
	- Wait for the scheduled run.
	- Click Run workflow to start it manually.

### Workflow behavior

The workflow:

1. Checks out the repository.
2. Sets up Python 3.11.
3. Installs dependencies from `requirements.txt`.
4. Runs `python main.py`.
5. Commits and pushes changes to `data/prices.csv` when new data is added.

## Output file

Historical data is stored in:

- `data/prices.csv`

If the file does not exist yet, the script creates it and writes the header automatically.

## Notes

- The data source is public, so no API key is required.
- If the API request fails, the script exits without updating the CSV.
