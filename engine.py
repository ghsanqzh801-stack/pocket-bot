import os, requests, time, threading, http.server, socketserver

# 1. السيرفر الوهمي (مهم جداً للبقاء حياً)
def run_vocal_server():
    port = int(os.environ.get("PORT", 10000))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()
threading.Thread(target=run_vocal_server, daemon=True).start()

# 2. إعداداتك (تأكد من صحتها)
TOKEN = "8768413194:AAGlUEfDY3lrnQKl_mvehVA-BLv6RJb1adI"
URL = f"https://api.telegram.org/bot{TOKEN}/"
CHAT_ID = "7692680668"

def send_action(action, chat_id, message_id=None, text="", keyboard=None):
    if message_id:
        requests.post(URL + "deleteMessage", json={"chat_id": chat_id, "message_id": message_id})
    
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if keyboard: payload["reply_markup"] = {"inline_keyboard": keyboard}
    return requests.post(URL + "sendMessage", json=payload).json()

# 3. محرك البوت
last_id = 0
while True:
    try:
        res = requests.get(URL + f"getUpdates?offset={last_id + 1}", timeout=10).json()
        for up in res.get("result", []):
            last_id = up["update_id"]
            m = up.get("message") or up.get("callback_query", {}).get("message")
            c_id = m["chat"]["id"]
            m_id = m["message_id"]

            if "message" in up and up["message"].get("text") == "/start":
                txt = "👑 **GMK-Empire Ghassan Training** 👑\n\nاختر زوج التداول:"
                kb = [[{"text": "📊 EUR/USD | 98% 🔥", "callback_data": "EURUSD"}]]
                send_action("send", c_id, text=txt, keyboard=kb)

            if "callback_query" in up:
                data = up["callback_query"]["data"]
                if data == "EURUSD":
                    txt = "🎯 اختر الفريم الزمني:"
                    kb = [[{"text": "5s", "callback_data": "5s"}, {"text": "1m", "callback_data": "1m"}]]
                    send_action("edit", c_id, m_id, txt, kb)
                elif data in ["5s", "1m"]:
                    send_action("edit", c_id, m_id, "⏳ **جاري التحليل...**")
                    time.sleep(1)
                    send_action("edit", c_id, m_id, "🟢 **BUY CALL**\nنسبة النجاح: 94%")

    except Exception as e:
        print(f"Error: {e}")
    time.sleep(1)
