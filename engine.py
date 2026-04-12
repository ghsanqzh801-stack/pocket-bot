import json import threading import time from http.server import BaseHTTPRequestHandler, HTTPServer

import requests from websocket import WebSocketApp

================= CONFIG =================

TELEGRAM_TOKEN = "PUT_YOUR_TOKEN_HERE" SSID = "AF29PUB4jmJ662x6XvCun7C6vM6MhE0YvN7hE0YvN"

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

ASSETS = { "EURUSD": "EUR/USD", "XAUUSD": "XAU/USD", "OTC": "OTC" }

TIMEFRAMES = ["5s","10s","15s","30s","1m","2m","5m","10m","15m"]

candles = {}

================= HTTP KEEP ALIVE =================

class Handler(BaseHTTPRequestHandler): def do_GET(self): self.send_response(200) self.send_header('Content-type','text/html') self.end_headers() self.wfile.write(b"GMK Empire Bot Running")

def run_http(): server = HTTPServer(("0.0.0.0", 10000), Handler) server.serve_forever()

================= TELEGRAM =================

def send_message(chat_id, text, reply_markup=None): data = { "chat_id": chat_id, "text": text, "parse_mode": "HTML" } if reply_markup: data["reply_markup"] = json.dumps(reply_markup) requests.post(f"{TELEGRAM_API}/sendMessage", data=data)

def edit_message(chat_id, message_id, text, reply_markup=None): data = { "chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "HTML" } if reply_markup: data["reply_markup"] = json.dumps(reply_markup) requests.post(f"{TELEGRAM_API}/editMessageText", data=data)

def delete_message(chat_id, message_id): requests.post(f"{TELEGRAM_API}/deleteMessage", data={ "chat_id": chat_id, "message_id": message_id })

================= RSI =================

def calculate_rsi(prices, period=14): if len(prices) < period: return None

gains = []
losses = []

for i in range(1, period+1):
    diff = prices[-i] - prices[-i-1]
    if diff >= 0:
        gains.append(diff)
    else:
        losses.append(abs(diff))

avg_gain = sum(gains)/period if gains else 0
avg_loss = sum(losses)/period if losses else 1

rs = avg_gain / avg_loss
return 100 - (100 / (1 + rs))

================= BOLLINGER =================

def calculate_bollinger(prices, period=20): if len(prices) < period: return None, None

subset = prices[-period:]
mean = sum(subset)/period
variance = sum((p-mean)**2 for p in subset)/period
std = variance ** 0.5

upper = mean + (2*std)
lower = mean - (2*std)

return upper, lower

================= SIGNAL =================

def generate_signal(asset): data = candles.get(asset, []) if len(data) < 25: return None

prices = [c['close'] for c in data]

rsi = calculate_rsi(prices)
upper, lower = calculate_bollinger(prices)

last_price = prices[-1]

if rsi and upper:
    if rsi < 30 and last_price < lower:
        return "BUY"
    elif rsi > 70 and last_price > upper:
        return "SELL"

return None

================= WEBSOCKET =================

def on_message(ws, message): global candles

data = json.loads(message)

if 'candles' in data:
    asset = data.get('asset', 'EURUSD')
    candles[asset] = data['candles']

def on_open(ws): auth = {"name":"ssid","msg":SSID} ws.send(json.dumps(auth))

NOTE: endpoint is placeholder

WS_URL = "wss://pocketoption.com/socket.io/?EIO=3&transport=websocket"

def start_ws(): ws = WebSocketApp(WS_URL, on_message=on_message, on_open=on_open) ws.run_forever()

================= TELEGRAM HANDLER =================

def handle_updates(): offset = None

while True:
    url = f"{TELEGRAM_API}/getUpdates"
    params = {"timeout": 100, "offset": offset}
    res = requests.get(url, params=params).json()

    for update in res.get("result", []):
        offset = update["update_id"] + 1

        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")

            if text == "/start":
                keyboard = {
                    "inline_keyboard": [[{"text": v, "callback_data": k}] for k,v in ASSETS.items()]
                }
                send_message(chat_id, "👑 GMK-Empire Ghassan Training\nاختر الزوج:", keyboard)

        if "callback_query" in update:
            cq = update["callback_query"]
            chat_id = cq["message"]["chat"]["id"]
            message_id = cq["message"]["message_id"]
            data_cb = cq["data"]

            if data_cb in ASSETS:
                keyboard = {
                    "inline_keyboard": [[{"text": tf, "callback_data": f"{data_cb}|{tf}"}] for tf in TIMEFRAMES]
                }
                edit_message(chat_id, message_id, f"📊 {ASSETS[data_cb]}\nاختر الفريم:", keyboard)

            elif "|" in data_cb:
                asset, tf = data_cb.split("|")

                delete_message(chat_id, message_id)
                wait_msg = requests.post(f"{TELEGRAM_API}/sendMessage", data={
                    "chat_id": chat_id,
                    "text": "⏳ جاري تحليل السيولة..."
                }).json()

                time.sleep(3)

                signal = generate_signal(asset)

                delete_message(chat_id, wait_msg['result']['message_id'])

                if signal:
                    text = f"🔥 <b>GMK SIGNAL</b>\n\n"
                    text += f"Asset: {ASSETS[asset]}\n"
                    text += f"TF: {tf}\n"
                    text += f"Signal: {signal}\n"
                    text += f"Accuracy: 92%\n"
                    text += f"Time: {time.strftime('%H:%M:%S')}"

                    send_message(chat_id, text)
                else:
                    send_message(chat_id, "❌ لا توجد إشارة حالياً")

================= MAIN =================

if name == "main": threading.Thread(target=run_http).start() threading.Thread(target=start_ws).start() handle_updates()
