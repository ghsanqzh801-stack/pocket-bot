import os, requests, time, threading, http.server, socketserver

# --- 1. إعدادات السيرفر لبقاء البوت حياً ---
def run_vocal_server():
    port = int(os.environ.get("PORT", 10000))
    with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()
threading.Thread(target=run_vocal_server, daemon=True).start()

# --- 2. بيانات البوت ---
TOKEN = "8768413194:AAGlUEfDY3lrnQKl_mvehVA-BLv6RJb1adI"
URL = f"https://api.telegram.org/bot{TOKEN}/"

# صور الفخامة (ثور ودب)
BULL_IMG = "https://w0.peakpx.com/wallpaper/144/952/HD-wallpaper-bull-stock-market-neon-green-bull-trading-green-bull.jpg"
BEAR_IMG = "https://w0.peakpx.com/wallpaper/601/104/HD-wallpaper-bear-market-stock-market-trading-red-bear.jpg"

# دالة لمسح الرسائل السابقة وإرسال جديد
def delete_and_send(chat_id, message_id, text, keyboard=None, photo=None):
    try: requests.post(URL + "deleteMessage", json={"chat_id": chat_id, "message_id": message_id})
    except: pass
    
    payload = {"chat_id": chat_id, "parse_mode": "Markdown"}
    if photo:
        payload.update({"photo": photo, "caption": text, "reply_markup": {"inline_keyboard": keyboard} if keyboard else None})
        return requests.post(URL + "sendPhoto", json=payload).json()
    else:
        payload.update({"text": text, "reply_markup": {"inline_keyboard": keyboard} if keyboard else None})
        return requests.post(URL + "sendMessage", json=payload).json()

# --- 3. منطق البوت ---
last_update_id = 0
user_state = {} # لحفظ اختيار المستخدم

while True:
    try:
        updates = requests.get(URL + f"getUpdates?offset={last_update_id + 1}").json()
        for up in updates.get("result", []):
            last_update_id = up["update_id"]
            chat_id = up.get("message", {}).get("chat", {}).get("id") or up.get("callback_query", {}).get("message", {}).get("chat", {}).get("id")
            msg_id = up.get("message", {}).get("message_id") or up.get("callback_query", {}).get("message", {}).get("message_id")
            
            # أمر البداية
            if "message" in up and up["message"].get("text") == "/start":
                txt = "👑 **GMK-Empire Ghassan Training** 👑\n\nأهلاً بك في أقوى نظام تحليل ذكي.\nيرجى اختيار زوج التداول (مرتبة حسب السيولة):"
                # هنا نضع أهم الأزواج (سيتم ربط البقية لاحقاً)
                kb = [
                    [{"text": "📊 EUR/USD (OTC) | 98% 🔥", "callback_data": "asset_EURUSD"}],
                    [{"text": "📊 XAU/USD (OTC) | 95% 🚀", "callback_data": "asset_XAUUSD"}],
                    [{"text": "📊 GBP/JPY (OTC) | 92% ✅", "callback_data": "asset_GBPJPY"}]
                ]
                delete_and_send(chat_id, msg_id, txt, kb)

            # عند اختيار الزوج
            elif "callback_query" in up:
                data = up["callback_query"]["data"]
                
                if data.startswith("asset_"):
                    user_state[chat_id] = {"asset": data.split("_")[1]}
                    txt = f"🎯 الزوج: *{user_state[chat_id]['asset']}*\n\nالآن، حدد **الفريم الزمني** بدقة للتحليل العميق:"
                    kb = [
                        [{"text": "5s", "callback_data": "f_5s"}, {"text": "10s", "callback_data": "f_10s"}, {"text": "15s", "callback_data": "f_15s"}],
                        [{"text": "30s", "callback_data": "f_30s"}, {"text": "1m", "callback_data": "f_1m"}, {"text": "5m", "callback_data": "f_5m"}],
                        [{"text": "🔙 رجوع", "callback_data": "start"}]
                    ]
                    delete_and_send(chat_id, msg_id, txt, kb)

                elif data.startswith("f_"):
                    # مح
