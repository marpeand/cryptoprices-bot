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


def getStatus(symbol, price, change, percent, interval):
    status_list = {
        'BTC':[ 
            f'#Bitcoin = {price}USD ({change}USD change) \nChange % ({interval}) = {percent}%\n\n #BTC #BTCUSD #Crypto'
        ],
        'ETH':[
            f'#Ethereum = {price}USD ({change}USD change) \nChange % ({interval}) = {percent}%\n\n #ETH #ETHUSD #Crypto'
        ],
        'SOL':[
            f'#Solana = {price}USD ({change}USD change) \nChange % ({interval}) = {percent}%\n\n #SOL #SOLUSD #Crypto'
        ],
        'DOGE':[
            f'#DOGE = {price}USD ({change}USD change) \nChange % ({interval}) = {percent}%\n\n #DOGE #DOGEUSD #Crypto'
        ]
    }

    return status_list[symbol][0]



def tweet(api, message):
    try:
        api.update_status(message)
        print(f'status updated')
    except tweepy.errors.Forbidden:
        print('Can`t tweet message!')

def main():
    symbols = ['BTC', 'ETH', 'SOL', 'DOGE']
    api = createAPI()
    interval = '1h'

    for symbol in symbols:
        changeResponse = getpriceChange(symbol, interval)
        priceResponse = getPrice(symbol)

        price = float(priceResponse['price'])
        price_change = float(changeResponse['priceChange'])
        change_percent = float(changeResponse['priceChangePercent'])

        tweet(api, getStatus(symbol, price, price_change, change_percent, interval))

        sleep(5)

if __name__ == '__main__':
    main()