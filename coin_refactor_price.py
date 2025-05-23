from operator import itemgetter
import requests
import json
import plotly.express as px
import os
import sys

# Constants
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/markets"
API_KEY = os.environ.get("COINGECKO_API")

# # Check if the API key is available
if not API_KEY:
    print("Error: COINGECKO_API environment variable not set.")
    print("Please set COINGECKO_API environment variable with your API key.")
    sys.exit(1)

HEADERS = {
    "accept": "application/json",
    "x-cg-demo-api-key": API_KEY
}
CURRENCY = "usd"
PROMPT_MESSAGE = (
    "Enter one or more coins separated by a comma (e.g., bitcoin, ethereum):\n"
    "Enter 'quit' to exit the session. "
)
TITLE = f"Prices of Selected Coins ({CURRENCY.upper()})"
X_LABEL = 'Name'
Y_LABEL = 'Price'
TITLE_FONT_SIZE = 28
AXIS_TITLE_FONT_SIZE = 20

class CryptoPriceFetcher:
    """Fetches and displays cryptocurrency prices."""
    def __init__(self):
        """Store all the ids, names, prices of each coin"""
        self.all_coin_ids = []
        self.all_coin_names = []
        self.all_coin_prices = []

    def fetch_coin_data(self):
        """Fetches cryptocurrency market data from the CoinGecko API."""
        try:
            response = requests.get(COINGECKO_API_URL, headers=HEADERS, 
            params={'vs_currency': CURRENCY})
            response.raise_for_status()
            print(f"Status Code: {response.status_code}")
            coin_data = response.json()
            sorted_coin_data = sorted(coin_data, key=itemgetter('current_price')
                                      , reverse=True)
            self.all_coin_ids = [coin['id'] for coin in sorted_coin_data]
            self.all_coin_names = [coin['name'] for coin in sorted_coin_data]
            self.all_coin_prices = [coin['current_price'] for coin in 
                                    sorted_coin_data]
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error Making API Request: {e}")
            return False
        except json.JSONDecodeError:
            print(f"Error Decoding JSON response from API")
            return False
        except Exception as e:
            print(f"Error Calling the API")
            return False

    def find_selected_coins(self, input_coin_ids):
        """Finds the data for the coins specified by the user."""
        found_coins = []
        not_found_coins = []
        for input_coin_id in input_coin_ids:
            if input_coin_id in self.all_coin_ids:
                index = self.all_coin_ids.index(input_coin_id)
                found_coins.append({
                    'name': self.all_coin_names[index],
                    'price': self.all_coin_prices[index]
                })
            else:
                not_found_coins.append(input_coin_id)
        return found_coins, not_found_coins

    def plot_coin_prices(self, coin_names, coin_prices):
        """Generates and displays a bar chart of coin prices."""
        fig = px.bar(
            x=coin_names,
            y=coin_prices,
            title=TITLE,
            labels={'x': X_LABEL, 'y': Y_LABEL},
            hover_name=coin_names
        )
        fig.update_layout(
            title_font_size=TITLE_FONT_SIZE,
            xaxis_title_font_size=AXIS_TITLE_FONT_SIZE,
            yaxis_title_font_size=AXIS_TITLE_FONT_SIZE
        )
        fig.show()

if __name__ == "__main__":
    fetcher = CryptoPriceFetcher()
    if not fetcher.fetch_coin_data():
        exit()

    while True:
        user_input = input(PROMPT_MESSAGE).lower()

        if user_input == 'quit':
            print("Exiting the session.")
            break

        if not user_input.strip():
            print("Please enter a valid Coin.")
            continue

        input_coin_ids = [coin_id.strip() for coin_id in user_input.split(',')]

        found_coins, not_found_coins = fetcher.find_selected_coins(input_coin_ids)

        if found_coins:
            selected_coin_names = [coin['name'] for coin in found_coins]
            selected_coin_prices = [coin['price'] for coin in found_coins]
            fetcher.plot_coin_prices(selected_coin_names, selected_coin_prices)

        if not_found_coins:
            print(f"Coin IDs not found in the current data: {', '
                                .join(not_found_coins)}")
        break