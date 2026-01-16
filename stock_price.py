import yfinance as yf
import os
from dotenv import load_dotenv
import math
import requests

def get_stock_price(tickers):
    load_dotenv()
    change_in_percents = []
    messages = []
    try:
        if not tickers:
            print('Please provide atleat one ticker')
        if len(tickers) > 1:
            for ticker in tickers:
                stock = yf.Ticker(ticker)
                data = stock.history(period="2d")

                if(len(data)< 2):
                    print('None')
                    continue

                yesterday = data.iloc[-2]["Close"]
                today = data.iloc[-1]["Close"]

                change_percent = ((today-yesterday)/yesterday)*100
                change_percent = round(change_percent,2)
                change_in_percents.append(change_percent)
                messages.append(f'Stock {ticker} closed at {today}. Stock price for {ticker} - has changed by {change_percent} % today.')
    except Exception as e:
        print(e)
        raise(e)
    
    if messages:
        send_notification(messages)
            
def send_notification(messages):
    print('sending', messages)
    payload = {"token": os.getenv("PUSHOVER_API_TOKEN"),
    "user":os.getenv("PUSHOVER_USER_KEY"),
    "title": "Stock Alert!",
    "message": "".join(messages) if isinstance(messages, list) else messages}

    requests.post("https://api.pushover.net/1/messages.json", data=payload)


if __name__ == "__main__":
    get_stock_price(["AAPL","FTNT","QQQ", "NVDA","VIG","SPY","SPAXX","VTIVX","SCHB","SCHD","VEU","VTI","VXUS","FDRXX"])
