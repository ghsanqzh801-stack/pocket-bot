import http.server
import socketserver
import threading
import os
import requests
import time

# 1. قسم البوابة الوهمية (عشان Render ما يطفي البوت)
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

# 2. إعدادات تليجرام وبوت التداول (تأكد من صحة التوكن والـ ID)
TOKEN = "7724147771:AAH8N_1R_pXq2L5_Z9v9Z_Z9v9Z9v9Z9v9Z" # حط التوكن تبعك هون
CHAT_ID = "6190543210" # حط معرف الشات تبعك هون

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

# 3. حلقة العمل الأساسية (البوت بيفضل شغال وما بيخرج)
print("🚀 البوت بدأ العمل ومراقب السوق...")
send_telegram_message("✅ تم تشغيل البوت بنجاح على Render!")

while True:
    try:
        # هون بكون كود التحليل تبعك (مثال بسيط)
        # print("تحليل السوق الحالي...") 
        time.sleep(30) # البوت بينتظر 30 ثانية وبيرجع يكرر عشان ما يطفي
    except Exception as e:
        print(f"Main loop error: {e}")
        time.sleep(10)
