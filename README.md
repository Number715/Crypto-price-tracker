# Cryptocurrency Price Tracker and Visualizer

A collection of Python scripts to fetch and visualize cryptocurrency prices, offering both current market insights and historical trends.

## Overview

This repository contains two Python scripts designed to help you track and understand cryptocurrency market data:

* `coin_historic_prices_edit.py`: Visualizes the price history of selected cryptocurrencies over the past year using Matplotlib.
* `coin_refactor_price.py`: Displays the current market prices of selected cryptocurrencies in an interactive bar chart using Plotly.

Both scripts interact with the CoinGecko API to retrieve data and require an API key for operation.

## Features

### `coin_historic_prices_edit.py`

This script focuses on historical price data, allowing users to see trends over time.

* **Interactive Coin Selection:** Prompts the user to enter one or more cryptocurrency IDs (e.g., `bitcoin`, `ethereum`) separated by commas.
* **Historical Price Chart:** Displays a line graph showing the price of the selected coins in USD over the last 365 days.
* **Clear Visualization:** The plot includes a title, axis labels (Date and Price in USD), a legend to identify each coin, and formatted dates on the x-axis.
* **Error Handling:** Gracefully handles API request errors and cases where historical data is not found for a given coin.

### `coin_refactor_price.py`

This script provides real-time current price visualization with interactive capabilities.

* **Current Price Visualization:** Fetches and displays the current price of user-specified cryptocurrencies in USD.
* **Interactive Bar Chart:** Generates a dynamic and interactive bar chart using Plotly, allowing users to hover over bars for precise price information.
* **User-Friendly Input:** Prompts the user to enter one or more cryptocurrency IDs (e.g., `bitcoin`, `ethereum`) separated by commas.
* **Robust Error Handling:** Includes comprehensive error handling for API request failures, JSON decoding issues, and invalid coin IDs.

## Prerequisites

* **Python 3.x** installed on your system.
* The following Python libraries:
    * `requests`
    * `matplotlib`
    * `plotly`

    You can install these using pip:
    ```bash
    pip install requests matplotlib plotly
    ```
* **CoinGecko API Key:** Both scripts require a CoinGecko API key. You need to obtain this key and set it as an environment variable named `COINGECKO_API`.

## API Information

Both scripts utilize the **CoinGecko API** for cryptocurrency data.

* **Base URL:** `https://api.coingecko.com/api/v3`
* **Endpoints Used:**
    * `/coins/markets` (for current market data and coin ID lookup)
    * `/coins/{coin_id}/market_chart` (for historical data)
* **API Key:** An API key is required and should be passed in the `x-cg-demo-api-key` header.
* **Documentation:** You can find more details about the CoinGecko API at [https://www.coingecko.com/en/api](https://www.coingecko.com/en/api).

## Usage

### Setting up the API Key

Before running either script, obtain your CoinGecko API key and set it as an environment variable.

**On Linux/macOS:**
```bash
export COINGECKO_API="your_api_key_here"
