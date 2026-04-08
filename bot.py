import os
import requests
from telegram import Bot
import time
import traceback
from flask import Flask
import threading

# --- إعداد Flask لتشغيل البوت كخدمة ويب على Render ---
app = Flask(__name__)

# --- قراءة متغيرات البيئة ---
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if not TOKEN:
    raise Exception("❌ خطأ: متغير البيئة TOKEN غير موجود")
if not CHAT_ID:
    raise Exception("❌ خطأ: متغير البيئة CHAT_ID غير موجود")

bot = Bot(token=TOKEN)
print("✅ البوت جاهز للعمل")

# --- دالة جلب أسعار الذهب ---
def get_gold_price():
    try:
        url = "https://api.metals.live/v1/spot/gold"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        price_usd = data[0]["price"]
    except Exception as e:
        print("⚠️ خطأ في جلب سعر الذهب:", e)
        return None

    try:
        fx_url = "https://api.exchangerate.host/latest?base=USD&symbols=YER"
        fx_data = requests.get(fx_url, timeout=10).json()
        yer_rate = fx_data.get("rates", {}).get("YER", 600)
    except Exception as e:
        print("⚠️ خطأ في جلب سعر الصرف:", e)
        yer_rate = 600

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

# --- حلقة البوت في الخلفية ---
def run_bot_loop():
    while True:
        try:
            message = get_gold_price()
            if message:
                try:
                    bot.send_message(chat_id=CHAT_ID, text=message)
                    print("✅ تم الإرسال")
                except Exception as e:
                    print("❌ خطأ في إرسال الرسالة:", e)
                    traceback.print_exc()
            else:
                print("⚠️ لم يتم جلب البيانات، سيتم المحاولة لاحقًا")
        except Exception as e:
            print("❌ خطأ غير متوقع:", e)
            traceback.print_exc()
        time.sleep(300)  # كل 5 دقائق

# تشغيل البوت في الخلفية
threading.Thread(target=run_bot_loop, daemon=True).start()

# --- صفحة Health Check لتجنب مشاكل Render ---
@app.route("/")
def home():
    return "✅ البوت يعمل", 200

# --- تشغيل Flask ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))