import tweepy
import requests
from os import environ
from time import sleep


def create_API():

    keys = {
        'CONSUMER_KEY':         environ['CONSUMER_KEY'],
        'CONSUMER_SECRET':      environ['CONSUMER_SECRET'],
        'ACCESS_TOKEN':         environ['ACCESS_TOKEN'],
        'ACCESS_TOKEN_SECRET':  environ['ACCESS_TOKEN_SECRET']
    }

    auth = tweepy.OAuthHandler(keys['CONSUMER_KEY'], keys['CONSUMER_SECRET'])
    auth.set_access_token(keys['ACCESS_TOKEN'], keys['ACCESS_TOKEN_SECRET'])
    api = tweepy.API(auth)

    return api

def get_price_last_hour(coin, interval):
    response = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=0&interval={interval}").json()
    price_last_hour = response['prices'][0][1]
    return price_last_hour

def get_price(coin):
    response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd")
    return response.json()[f"{coin}"]['usd']

def generate_status(coin, price, price_1h, interval):
    price_change = round(price - price_1h, 2)
    change_percent = round(((price/price_1h) * 100) - 100, 2)

    emoji = "🔴⬇️" if change_percent < 0 else "🟢⬆️"

    status = f"#{coin} Stats 📊📈📉 (last hour)\n\n Price : {price} USD💵\n \
Variation : {change_percent}% ({price_change}USD💵) {emoji}\n\n\
#cryptonews #cryptomarket #crypto #blockchain #trading"

    return status

def tweet_status(api, message):
    try:
        api.update_status(message)
        print(f'status updated')
    except tweepy.errors.Forbidden:
        print('Can`t tweet status!')

def main():
    coins = [
        'bitcoin', 'ethereum', 'solana', 
        'binancecoin', 'cardano', 'monero', 
        'litecoin','dogecoin'
    ]
    
    API = create_API()
    interval = 'hourly'

    for coin in coins:
        price = float(get_price(coin))
        sleep(6) # sleep necessary to prevent 429 Too Many Requests error.
        price_1h = float(get_price_last_hour(coin, interval))

        status = generate_status(coin, price, price_1h, interval)

        tweet_status(API, status)

        sleep(1)

if __name__ == '__main__':
    main()
