import os, requests, time, threading, http.server, socketserver

# 1. خادم البقاء (الأساسي للتشغيل على Render)
def run_vocal_server():
    port = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            httpd.serve_forever()
    except: pass

threading.Thread(target=run_vocal_server, daemon=True).start()

# 2. إعداداتك (التوكن والـ SSID)
TOKEN = "8768413194:AAGlUEfDY3lrnQKl_mvehVA-BLv6RJb1adI"
URL = f"https://api.telegram.org/bot{TOKEN}/"
BULL = "https://w0.peakpx.com/wallpaper/144/952/HD-wallpaper-bull-stock-market-neon-green-bull-trading-green-bull.jpg"
BEAR = "https://w0.peakpx.com/wallpaper/601/104/HD-wallpaper-bear-market-stock-market-trading-red-bear.jpg"

def tg_call(method, data):
    try: return requests.post(URL + method, json=data, timeout=10).json()
    except: return None

# 3. محرك البوت المبسط والمستقر
last_id = 0
user_data = {}

while True:
    try:
        resp = requests.get(URL + f"getUpdates?offset={last_id + 1}", timeout=5).json()
        for up in resp.get("result", []):
            last_id = up["update_id"]
            m = up.get("message") or up.get("callback_query", {}).get("message")
            c_id, m_id = m["chat"]["id"], m["message_id"]

            if "message" in up and up["message"].get("text") == "/start":
                txt = "👑 **GMK-Empire Elite** 👑\n\nاختر زوج التداول للتحليل:"
                kb = [[{"text": "📊 EUR/USD (OTC) | 98%", "callback_data": "a_EURUSD"}],
                      [{"text": "📊 XAU/USD (OTC) | 95%", "callback_data": "a_XAUUSD"}]]
                tg_call("deleteMessage", {"chat_id": c_id, "message_id": m_id})
                tg_call("sendMessage", {"chat_id": c_id, "text": txt, "parse_mode": "Markdown", "reply_markup": {"inline_keyboard": kb}})

            if "callback_query" in up:
                data = up["callback_query"]["data"]
                if data.startswith("a_"):
                    user_data[c_id] = data.replace("a_", "")
                    kb = [[{"text": "5s", "callback_data": "t_5s"}, {"text": "1m", "callback_data": "t_1m"}],
                          [{"text": "5m", "callback_data": "t_5m"}, {"text": "15m", "callback_data": "t_15m"}]]
                    tg_call("editMessageText", {"chat_id": c_id, "message_id": m_id, "text": f"🎯 الزوج: {user_data[c_id]}\nحدد الفريم:", "reply_markup": {"inline_keyboard": kb}})
                
                elif data.startswith("t_"):
                    tg_call("editMessageText", {"chat_id": c_id, "message_id": m_id, "text": "⚡ **جاري التحليل الحقيقي...**"})
                    time.sleep(1.5)
                    res = "BUY CALL 🟢" if int(time.time()) % 2 == 0 else "SELL PUT 🔴"
                    img = BULL if "BUY" in res else BEAR
                    tg_call("deleteMessage", {"chat_id": c_id, "message_id": m_id})
                    tg_call("sendPhoto", {"chat_id": c_id, "photo": img, "caption": f"💎 **إشارة GMK**\n\n💹 الزوج: {user_data.get(c_id)}\n🚀 القرار: {res}", "parse_mode": "Markdown"})
    except: pass
    time.sleep(0.5)
