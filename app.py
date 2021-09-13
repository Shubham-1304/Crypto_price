import telebot
import sqlite3
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

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

app.polling()
