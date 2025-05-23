from pathlib import Path
from operator import itemgetter
import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import sys

# --- Configuration ---
API_BASE_URL = "https://api.coingecko.com/api/v3"
MARKETS_ENDPOINT = "/coins/markets"
MARKET_CHART_ENDPOINT = "/coins/{coin_id}/market_chart"
API_KEY = os.environ.get("COINGECKO_API")

# Check if the API key is available
if not API_KEY:
    print("Error: COINGECKO_API environment variable not set.")
    print("Please set COINGECKO_API environment variable with your API key.")
    sys.exit(1)

HEADERS = {
    "accept": "application/json",
    "x-cg-demo-api-key": API_KEY
}
CURRENCY = 'usd'
DAYS = 365
MARKET_DATA_PER_PAGE = 250
PLOT_TITLE = f"Prices of Selected Coins Over Past Year ({CURRENCY.upper()})"
DATE_FORMAT = '%b %Y'
PLOT_STYLE = 'dark_background'

def fetch_market_data():
    """Fetches and sorts the current market data for cryptocurrencies."""
    url = f"{API_BASE_URL}{MARKETS_ENDPOINT}"
    params = {'vs_currency': CURRENCY, 'per_page': MARKET_DATA_PER_PAGE}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()  
    market_data = response.json()
    return market_data

def create_coin_info(market_data):
    """Creates a dictionary mapping coin IDs to their names."""
    return {coin['id']: coin['name'] for coin in market_data}

def fetch_historical_data(coin_id):
    """Fetches historical market chart data for a given coin ID."""
    url = f"{API_BASE_URL}{MARKET_CHART_ENDPOINT.format(coin_id=coin_id)}"
    params = {'vs_currency': CURRENCY, 'days': DAYS}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def process_historical_data(historical_data):
    """Processes historical data to extract dates and prices."""
    if 'prices' in historical_data:
        prices_info = historical_data['prices']
        timestamps_ms = [coin[0] for coin in prices_info]
        prices = [coin[1] for coin in prices_info]
        dates = [datetime.fromtimestamp(ts / 1000) for ts in timestamps_ms]
        return dates, prices
    else:
        raise ValueError("Key 'prices' not found in historical data.")

def plot_coin_prices(ax, dates, prices, label):
    """Plots the price history of a coin on the given axes."""
    ax.plot(dates, prices, label=label)

def format_plot(fig, ax):
    """Formats the plot with labels, title, legend, and date formatting."""
    ax.set_xlabel("Date", fontsize=16)
    ax.set_ylabel(f"Price ({CURRENCY.upper()})", fontsize=16)
    ax.set_title(PLOT_TITLE, fontsize=24)
    ax.legend()
    fig.autofmt_xdate()
    date_formatter = mdates.DateFormatter(DATE_FORMAT)
    ax.xaxis.set_major_formatter(date_formatter)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.tight_layout()

def main():
    """Main function to run the cryptocurrency price plotting tool."""
    try:
        market_data = fetch_market_data()
        print(f"Status code (market data): 200")
        coin_info = create_coin_info(market_data)
        available_ids = list(coin_info.keys())
    except requests.exceptions.RequestException as e:
        print(f"Error fetching market data: {e}")
        return

    while True:
        coin_ids_input = input(
            f"Enter one or more coin IDs separated by a comma "
            f"(e.g., bitcoin, ethereum):\n"
            f"Enter 'quit' to exit the session. "
        ).lower()

        if coin_ids_input == 'quit':
            print('Exiting the session.')
            break

        if not coin_ids_input:
            print("Please enter a valid coin ID.")
            continue

        requested_ids = [coin_id.strip() for coin_id in
                         coin_ids_input.split(',')]
        found_coins, not_found_coins = [], []

        for coin_id in requested_ids:
            if coin_id in available_ids:
                found_coins.append(coin_id)
            else:
                not_found_coins.append(coin_id)

        if found_coins:
            plt.style.use(PLOT_STYLE)
            fig, ax = plt.subplots()
            for coin_id in found_coins:
                try:
                    historical_data = fetch_historical_data(coin_id)
                    print(f"ID: {coin_id}\tStatus Code (historical data): 200")
                    dates, prices = process_historical_data(historical_data)
                    coin_name = coin_info.get(coin_id, coin_id)
                    plot_coin_prices(ax, dates, prices, coin_name)
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching data for {coin_id}: {e}")
                except ValueError as e:
                    print(f"Error processing data for {coin_id}: {e}")

            format_plot(fig, ax)
            plt.show()
        elif not requested_ids: # Handles empty input from users.
            print("Please enter a valid coin ID.")
        # Should ideally not happen if input is processed correctly
        elif not found_coins and not not_found_coins:
            pass  # No coins were processed

        if not_found_coins:
            print(f"Coin IDs not found in the current data: "
                  f"{', '.join(not_found_coins)}")
        break


if __name__ == "__main__":
    main()