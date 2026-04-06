import requests
from telegram import Bot
import time
import os

TOKEN = os.getenv("8624246936:AAGIB6_YZCmcvw8Bt6Q_D75sd4yRYbAtcwM")
CHAT_ID = os.getenv("-1003594557268")

bot = Bot(token=TOKEN)

last_message_id = None

def get_gold_price():
    gold_url = "https://api.gold-api.com/price/XAU"
    gold_data = requests.get(gold_url).json()
    price_usd = gold_data["price"]

    fx_url = "https://api.exchangerate-api.com/v4/latest/USD"
    fx_data = requests.get(fx_url).json()
    yer_rate = fx_data["rates"]["YER"]

    gold_24_usd = price_usd
    gold_22_usd = price_usd * 0.916
    gold_21_usd = price_usd * 0.875
    gold_18_usd = price_usd * 0.75

    gold_24_yer = gold_24_usd * yer_rate
    gold_22_yer = gold_22_usd * yer_rate
    gold_21_yer = gold_21_usd * yer_rate
    gold_18_yer = gold_18_usd * yer_rate

    message = f"""
📊 أسعار الذهب الآن:

🥇 عيار 24:
{gold_24_usd:.2f}$ | {gold_24_yer:,.0f} ريال

🥈 عيار 22:
{gold_22_usd:.2f}$ | {gold_22_yer:,.0f} ريال

🥉 عيار 21:
{gold_21_usd:.2f}$ | {gold_21_yer:,.0f} ريال

💍 عيار 18:
{gold_18_usd:.2f}$ | {gold_18_yer:,.0f} ريال

💱 الدولار:
1$ = {yer_rate:,.0f} ريال

⏰ تحديث تلقائي
"""
    return message

while True:
    try:
        msg = get_gold_price()
        bot.send_message(chat_id=CHAT_ID, text=msg)
        print("تم الإرسال")
    except Exception as e:
        print(e)

    time.sleep(300)