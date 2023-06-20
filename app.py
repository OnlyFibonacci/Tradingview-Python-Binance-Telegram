from flask import Flask, request
import json, inspect
import telebot
from binance.spot import Spot as Client

app = Flask(__name__)

@app.route("/", methods=['POST'])
def webhook():
    # linke gelen post isteklerini parçala ve diğer fonksiyonlara dağıt.
    try:
        data = json.loads(request.data)
        ticker = data['ticker']
        exchange = data['exchange']
        price = data['price']
        side = data['side']
        quantity = data['quantity']
        telegramBotApi = data['telegramBotApi']
        telegramUserId = data['telegramUserId']
        binanceApiKey = data['binanceApiKey']
        binanceSecretKey = data['binanceSecretKey']
        params = {
            "symbol": ticker,
            "side": side,
            "type": "MARKET",
            "quantity": quantity,
        }
        binanceOrder(binanceApiKey, binanceSecretKey, params)
        telegramSender(telegramBotApi,telegramUserId,ticker,side,exchange,quantity)
    except Exception as e:
        funcName = inspect.stack()[0][3]
        print(f"{funcName}() fonsiyonunda hata oluştu: {e}")
    return {
        "code": "success"
    }

@app.route("/istek", methods=['POST'])
def tele():
    return json.loads(request.data)

def binanceOrder(apiKey : str, secretKey : str, params):
    try:
        Client(apiKey,secretKey).new_order(**params)
    except Exception as e:
        funcName = inspect.stack()[0][3]
        print(f"{funcName}() fonsiyonunda hata oluştu: {e}")


def telegramSender(botApi : str, telegramUserId : str, ticker : str, side : str, exchange : str, quantity : str):
    try:
        telebot.TeleBot(botApi).send_message(telegramUserId, f"{ticker} {side}ING on {exchange} \nQuantity : {quantity} ")
    except Exception as e:
        funcName = inspect.stack()[0][3]
        print(f"{funcName}() fonsiyonunda hata oluştu: {e}")
        
        

# app.run()
app.run(host='0.0.0.0', port = 80, debug=True)