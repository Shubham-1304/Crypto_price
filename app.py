import telebot
import sqlite3
import requests
import json
from flask import Flask,request
from dotenv import load_dotenv
import os

load_dotenv()
server=Flask(__name__)
def cwc(msg):
    curl="https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    params={'symbol':msg,'convert':'INR'}
    headers={'X-CMC_PRO_API_KEY':os.getenv("token")}
    req=requests.get(curl,headers=headers,params=params).json()
    write_json(req)
    try:
        price=req['data'][msg]['quote']['INR']['price']
        return price
    except:
        return "No data"


def write_json(r,filename='response_c.json'):
    with open(filename,'w') as f:
        json.dump(r,f,indent=4,ensure_ascii=False)

app=telebot.TeleBot(os.getenv("token2"))
@app.message_handler(commands=['start'])
def greet(message):
    app.reply_to(message,f"{message.text}")

@app.message_handler(func=lambda m:True)
def crypto(message):
    try:
        price=cwc(message.text)
        app.reply_to(message,f"{price}")
    except:
        app.reply_to(message,"wrong input")
    try:
        connection=sqlite3.connect('data.db')
        cursor=connection.cursor()
        query="INSERT INTO info VALUES(?,?,?)"
        cursor.execute(query,(message.chat.id,message.chat.first_name,message.chat.last_name))
        connection.commit()
        connection.close()
    except:
        pass
        #print("No Data")

@server.route('/',methods=['POST'])
def getMessage():
    app.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "0",200

@server.route('/')
def webhook():
    app.remove_webhook()
    app.set_webhook(url='https://crypto--price.herokuapp.com/'+os.getenv("token2"))
    return "0",200

if __name__=='__main__':
    server.run(host="0.0.0.0",port=int(os.environ.get('PORT',5000)))
