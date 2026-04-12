import http.server
import socketserver
import threading
import os
import requests
import time

# 1. قسم البوابة الوهمية (عشان يضل البوت Live وما يطفي)
def run_vocal_server():
    class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is Running!")
    port = int(os.environ.get("PORT", 10000))
    try:
        with socketserver.TCPServer(("", port), HealthCheckHandler) as httpd:
            print(f"✅ Web Server started on port {port}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Web server error: {e}")

# تشغيل السيرفر في الخلفية
threading.Thread(target=run_vocal_server, daemon=True).start()

# 2. إعدادات تليجرام الخاصة بك (تم التحديث)
TOKEN = "8768413194:AAGlUEfDY3lrnQKl_mvehVA-BLv6RJb1adI"
CHAT_ID = "7692680668"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload)
        print(f"Telegram Response: {response.text}")
    except Exception as e:
        print(f"Telegram error: {e}")

# 3. تشغيل البوت
print("🚀 جاري فحص الاتصال وتفعيل البوت...")
time.sleep(2) # انتظار بسيط للتأكد من استقرار السيرفر
send_telegram_message("🔔 يا غسان، البوت اشتغل بنجاح على Render وهو الآن يراقب السوق!")

# حلقة البقاء (Loop) عشان يضل شغال 24 ساعة
while True:
    try:
        # هنا يمكنك إضافة كود تحليل الصفقات لاحقاً
        time.sleep(60) 
    except Exception as e:
        print(f"Loop error: {e}")
        time.sleep(10)
