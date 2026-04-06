import os
import requests
from telegram import Bot
import time

# قراءة متغيرات البيئة
TOKEN = os.environ.get("8624246936:AAGIB6_YZCmcvw8Bt6Q_D75sd4yRYbAtcwM")
CHAT_ID = os.environ.get(" -1003594557268")

# التحقق من وجود المتغيرات
if not TOKEN:
    raise Exception("❌ خطأ: متغير البيئة TOKEN غير موجود")
if not CHAT_ID:
    raise Exception("❌ خطأ: متغير البيئة CHAT_ID غير موجود")

# إنشاء البوت
bot = Bot(token=TOKEN)
print("✅ البوت جاهز للعمل")

def get_gold_price():
    try:
        url = "https://api.metals.live/v1/spot/gold"
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        price_usd = data[0]["price"]
    except Exception as e:
        print("خطأ في جلب سعر الذهب:", e)
        return None

    try:
        fx_url = "https://api.exchangerate.host/latest?base=USD&symbols=YER"
        fx_data = requests.get(fx_url).json()
        yer_rate = fx_data["rates"]["YER"]
    except Exception as e:
        print("خطأ في جلب سعر الصرف:", e)
        yer_rate = 600  # fallback

    gold_24_usd = price_usd
    gold_22_usd = price_usd * 0.916
    gold_21_usd = price_usd * 0.875
    gold_18_usd = price_usd * 0.75

    gold_24_yer = gold_24_usd * yer_rate
    gold_22_yer = gold_22_usd * yer_rate
    gold_21_yer = gold_21_usd * yer_rate
    gold_18_yer = gold_18_usd * yer_rate

    msg = f"""
📊 أسعار الذهب الآن:

🥇 عيار 24: {gold_24_usd:.2f}$ | {gold_24_yer:,.0f} ريال
🥈 عيار 22: {gold_22_usd:.2f}$ | {gold_22_yer:,.0f} ريال
🥉 عيار 21: {gold_21_usd:.2f}$ | {gold_21_yer:,.0f} ريال
💍 عيار 18: {gold_18_usd:.2f}$ | {gold_18_yer:,.0f} ريال

💱 1$ = {yer_rate:,.0f} ريال
⏰ تحديث كل 5 دقائق
"""
    return msg

while True:
    try:
        message = get_gold_price()
        if message:
            bot.send_message(chat_id=CHAT_ID, text=message)
            print("✅ تم الإرسال")
        else:
            print("⚠️ رسالة فارغة")
    except Exception as e:
        print("❌ خطأ في إرسال الرسالة:", e)
    time.sleep(300)  # تحديث كل 5 دقائق