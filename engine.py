import os, requests, time, threading, http.server, socketserver

# خادم البقاء
def run_vocal_server():
    port = int(os.environ.get("PORT", 10000))
    with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()
threading.Thread(target=run_vocal_server, daemon=True).start()

TOKEN = "8768413194:AAGlUEfDY3lrnQKl_mvehVA-BLv6RJb1adI"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def tg(method, data):
    return requests.post(URL + method, json=data).json()

last_id = 0
user_data = {}

while True:
    try:
        res = requests.get(URL + f"getUpdates?offset={last_id + 1}", timeout=5).json()
        for up in res.get("result", []):
            last_id = up["update_id"]
            m = up.get("message") or up.get("callback_query", {}).get("message")
            c_id = m["chat"]["id"]
            m_id = m["message_id"]

            if "message" in up and up["message"].get("text") == "/start":
                txt = "✨ **لوحة التحكم الاحترافية** ✨\n\nاختر الزوج المطلوب للتحليل (مرتبة حسب السيولة):"
                kb = [
                    [{"text": "🔥 ممتاز | EUR/USD (OTC) | 92%", "callback_data": "a_EURUSD"}],
                    [{"text": "✅ جيد جداً | XAU/USD (OTC) | 89%", "callback_data": "a_XAUUSD"}],
                    [{"text": "⚠️ متوسط | GBP/JPY (OTC) | 85%", "callback_data": "a_GBPJPY"}]
                ]
                tg("sendMessage", {"chat_id": c_id, "text": txt, "parse_mode": "Markdown", "reply_markup": {"inline_keyboard": kb}})

            if "callback_query" in up:
                data = up["callback_query"]["data"]
                if data.startswith("a_"):
                    asset = data.replace("a_", "")
                    user_data[c_id] = asset
                    # تحديث نفس الرسالة بالفريمات (احترافية)
                    txt = f"💹 **الزوج المختار:** `{asset}`\n\nحدد الفريم الزمني بدقة:"
                    kb = [[{"text": "5s", "callback_data": "t_5s"}, {"text": "1m", "callback_data": "t_1m"}, {"text": "5m", "callback_data": "t_5m"}]]
                    tg("editMessageText", {"chat_id": c_id, "message_id": m_id, "text": txt, "parse_mode": "Markdown", "reply_markup": {"inline_keyboard": kb}})

                elif data.startswith("t_"):
                    # مسح القائمة وظهور الإشارة فوراً
                    tg("deleteMessage", {"chat_id": c_id, "message_id": m_id})
                    tg("sendMessage", {"chat_id": c_id, "text": f"🚀 **إشارة قوية لزوج {user_data.get(c_id)}**\nالقرار: **BUY CALL 🟢**", "parse_mode": "Markdown"})
    except: pass
    time.sleep(0.4)
