import tweepy
import requests
from os import environ
from time import sleep


def createAPI():

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

def getpriceChange(symbol, interval):
    return requests.get(f"https://api.binance.com/api/v3/ticker?symbol={symbol}USDT&windowSize={interval}").json()

def getPrice(symbol):
    return requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT").json()


def getStatus(symbol, price, change, percent, interval, emoji):

    status = f"#{symbol} Stats 📊📈📉 (last {interval})\n\n Price : {price} #USDT💵\n \
Variation : {percent}% ({change}USDT💵) {emoji}\n\n\
#cryptonews #cryptomarket #crypto #blockchain #trading"

    return status


def tweet(api, message):
    try:
        api.update_status(message)
        print(f'status updated')
    except tweepy.errors.Forbidden:
        print('Can`t tweet message!')

def main():
    symbols = ['BTC', 'ETH', 'SOL', 'BNB', 'ADA', 'XMR', 'LTC','DOGE']
    api = createAPI()
    interval = '1h'

    for symbol in symbols:
        changeResponse = getpriceChange(symbol, interval)
        priceResponse = getPrice(symbol)

        price = float(priceResponse['price'])
        price_change = float(changeResponse['priceChange'])
        change_percent = float(changeResponse['priceChangePercent'])

        emoji = "🔴⬇️" if change_percent < 0 else "🟢⬆️"

        status = getStatus(symbol, price, price_change, change_percent, interval, emoji)

        tweet(api, status)

        sleep(1)

if __name__ == '__main__':
    main()