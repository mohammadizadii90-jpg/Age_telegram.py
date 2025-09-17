import telebot
import datetime
import jdatetime
from hijridate import Gregorian
from dateutil.relativedelta import relativedelta
import time

TOKEN = "8446883205:AAFmJiiyhx0U_XcmbtDnchX780QsHZYOjj4"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "سلام 👋\n"
        "تاریخ تولدت رو بفرست:\n\n"
        "📌 اگر میلادی هست: 2000-05-12\n"
        "📌 اگر شمسی هست: 1380-02-23"
    )

@bot.message_handler(func=lambda m: True)
def get_birthday(message):
    try:
        text = message.text.strip().replace("/", "-")
        year, month, day = map(int, text.split("-"))

        if year > 1500:  
            # ورودی میلادی
            bdate = datetime.date(year, month, day)
        else:  
            # ورودی شمسی
            bdate = jdatetime.date(year, month, day).togregorian()

        today = datetime.date.today()

        # محاسبه دقیق سن
        diff = relativedelta(today, bdate)
        age_text = f"{diff.years} سال و {diff.months} ماه و {diff.days} روز"

        # تاریخ‌ها
        bdate_shamsi = jdatetime.date.fromgregorian(date=bdate)
        bdate_qamari = Gregorian(bdate.year, bdate.month, bdate.day).to_hijri()

        response = f"""
👶 سن شما: {age_text}
📅 تاریخ میلادی: {bdate}
📅 تاریخ شمسی: {bdate_shamsi}
📅 تاریخ قمری: {bdate_qamari}
"""
        bot.reply_to(message, response)

    except Exception as e:
        bot.reply_to(message, "❌ لطفا تاریخ درست وارد کن (مثال: 2000-05-12 یا 1380-02-23)")

# اجرای پایدار
while True:
    try:
        print("✅ ربات روشن شد و در حال کاره ...")
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print("❌ خطا:", e)
        time.sleep(5)  # ۵ ثانیه صبر کن بعد دوباره اجرا کن
