import os
import requests
import websocket
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# إعدادات البوت
TOKEN = "8768413194:AAGlUEfDY31rnQKl_mvehVA-BLv6RJb1adI"
CHAT_ID = "7692680668"
SSID = "2sk01k19q3ms1h169v4e03i6l3"

# سيرفر وهمي عشان Render ما يطفي البوت
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running!")

def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except: pass

def on_message(ws, message):
    if 'history' in message or 'candles' in message:
        try:
            data = json.loads(message[2:])
            price = data[1]['data'][0]['close']
            print(f"💰 السعر الآن: {price}")
        except: pass

def on_open(ws):
    auth = f'42["auth", {{"session": "{SSID}", "isDemo": 1}}]'
    ws.send(auth)
    ws.send('42["subscribe", {"asset": "XAUUSD_otc", "period": 1}]')
    send_msg("🚀 غسان! البوت انطلق مجاناً وبدأ تحليل الذهب!")

if __name__ == "__main__":
    # تشغيل السيرفر في خلفية منفصلة
    threading.Thread(target=run_health_server, daemon=True).start()
    
    # تشغيل اتصال البوكيت أوبشن
    ws = websocket.WebSocketApp(
        "wss://api-pocketoption.com/socket.io/?EIO=3&transport=websocket",
        on_open=on_open, on_message=on_message
    )
    ws.run_forever()
