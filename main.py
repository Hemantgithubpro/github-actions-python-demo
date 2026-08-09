import csv
import datetime
import os
import requests


def fetch_market_data():
  """Fetches public market data (no API key required)."""
  url = "https://api.coingecko.com/api/v3/simple/price"
  params = {
      "ids": "bitcoin,ethereum,solana",
      "vs_currencies": "usd",
      "include_24hr_change": "true",
  }
  headers = {"User-Agent": "GitHubActions-SampleProject/1.0"}

  response = requests.get(url, params=params, headers=headers, timeout=10)
  response.raise_for_status()
  return response.json()


def save_to_csv(data, timestamp_str):
  """Appends price data rows into data/prices.csv."""
  os.makedirs("data", exist_ok=True)
  csv_filepath = os.path.join("data", "prices.csv")
  file_exists = os.path.isfile(csv_filepath)

  with open(csv_filepath, mode="a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # Write CSV header on initial file creation
    if not file_exists:
      writer.writerow(["timestamp_utc", "asset", "price_usd", "change_24h"])

    for asset_id, stats in data.items():
      writer.writerow([
          timestamp_str,
          asset_id,
          stats.get("usd", 0.0),
          round(stats.get("usd_24h_change", 0.0), 2),
      ])


def main():
  now_str = datetime.datetime.now(datetime.timezone.utc).strftime(
      "%Y-%m-%d %H:%M:%S"
  )
  print(f"=== Market Tracker Job Executed At: {now_str} UTC ===")

  try:
    data = fetch_market_data()
  except Exception as e:
    print(f"Error fetching data: {e}")
    return

  # 1. Append data to CSV history file
  save_to_csv(data, now_str)
  print("Successfully appended price records to data/prices.csv")

  # 2. Write GitHub Step Summary UI Table
  summary_lines = [
      f"### 📈 Market Snapshot (`{now_str} UTC`)",
      "| Asset | Price (USD) | 24h Change |",
      "| :--- | :--- | :--- |",
  ]

  for asset_id, stats in data.items():
    price = stats.get("usd", 0.0)
    change = stats.get("usd_24h_change", 0.0)
    trend = "🟢" if change >= 0 else "🔴"

    print(f"[{asset_id.upper()}] ${price:,.2f} | 24h: {change:+.2f}%")
    summary_lines.append(
        f"| **{asset_id.capitalize()}** | `${price:,.2f}` | {trend}"
        f" `{change:+.2f}%` |"
    )

  summary_filepath = os.getenv("GITHUB_STEP_SUMMARY")
  if summary_filepath:
    with open(summary_filepath, "a", encoding="utf-8") as f:
      f.write("\n".join(summary_lines) + "\n")


if __name__ == "__main__":
  main()