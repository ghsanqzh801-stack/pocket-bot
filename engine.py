import http.server
import socketserver
import threading
import os
import requests
import time

# 1. السيرفر الوهمي لبقاء البوت شغال على Render
def run_vocal_server():
    class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is Running!")
    port = int(os.environ.get("PORT", 10000))
    with socketserver.TCPServer(("", port), HealthCheckHandler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_vocal_server, daemon=True).start()

# 2. إعداداتك
TOKEN = "8768413194:AAGlUEfDY3lrnQKl_mvehVA-BLv6RJb1adI"
CHAT_ID = "7692680668"

# قائمة أزواج وهمية حالياً (رح نربطها بالمنصة بالخطوة الجاية)
assets = [
    {"name": "EUR/USD (OTC)", "payout": 92, "status": "ممتاز 🔥"},
    {"name": "XAU/USD (OTC)", "payout": 89, "status": "جيد جداً ✅"},
    {"name": "GBP/JPY (OTC)", "payout": 85, "status": "متوسط ⚠️"},
]

def send_main_menu():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # ترتيب حسب النسبة الأعلى
    sorted_assets = sorted(assets, key=lambda x: x['payout'], reverse=True)
    
    keyboard = []
    for asset in sorted_assets:
        keyboard.append([{"text": f"📊 {asset['name']} | {asset['payout']}% | {asset['status']}", "callback_data": asset['name']}])
    
    payload = {
        "chat_id": CHAT_ID,
        "text": "✨ **لوحة التحكم الاحترافية** ✨\n\nاختر الزوج المطلوب للتحليل (مرتبة حسب السيولة):",
        "reply_markup": {"inline_keyboard": keyboard},
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

# 3. مراقبة الأوامر (Listening)
last_update_id = 0
while True:
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_update_id + 1}"
        updates = requests.get(url).json()
        
        for update in updates.get("result", []):
            last_update_id = update["update_id"]
            if "message" in update and update["message"].get("text") == "/start":
                send_main_menu()
                
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(2)
