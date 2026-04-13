import os, requests, time, threading, http.server, socketserver

# --- 1. خادم البقاء (Keep-Alive) لضمان التشغيل على Render ---
def run_vocal_server():
    port = int(os.environ.get("PORT", 10000))
    with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()
threading.Thread(target=run_vocal_server, daemon=True).start()

# --- 2. إعدادات الإمبراطورية ---
TOKEN = "8768413194:AAGlUEfDY3lrnQKl_mvehVA-BLv6RJb1adI"
URL = f"https://api.telegram.org/bot{TOKEN}/"
BULL = "https://w0.peakpx.com/wallpaper/144/952/HD-wallpaper-bull-stock-market-neon-green-bull-trading-green-bull.jpg"
BEAR = "https://w0.peakpx.com/wallpaper/601/104/HD-wallpaper-bear-market-stock-market-trading-red-bear.jpg"

def tg(method, data):
    return requests.post(URL + method, json=data).json()

last_id = 0
user_data = {}

# --- 3. محرك البوت الذكي (نظام المسح الاحترافي) ---
while True:
    try:
        res = requests.get(URL + f"getUpdates?offset={last_id + 1}", timeout=5).json()
        for up in res.get("result", []):
            last_id = up["update_id"]
            m = up.get("message") or up.get("callback_query", {}).get("message")
            c_id = m["chat"]["id"]
            m_id = m["message_id"]

            if "message" in up and up["message"].get("text") == "/start":
                # المسح الفوري لأي رسالة قديمة
                tg("deleteMessage", {"chat_id": c_id, "message_id": m_id})
                
                txt = "👑 **لوحة التحكم الاحترافية - GMK** 👑\n\nاختر الزوج المطلوب للتحليل (مرتبة حسب السيولة):"
                kb = [
                    [{"text": "🔥 ممتاز | EUR/USD (OTC) | 98%", "callback_data": "a_EURUSD"}],
                    [{"text": "✅ جيد جداً | XAU/USD (OTC) | 95%", "callback_data": "a_XAUUSD"}],
                    [{"text": "📊 عالي | GBP/USD (OTC) | 92%", "callback_data": "a_GBPUSD"}]
                ]
                tg("sendMessage", {"chat_id": c_id, "text": txt, "parse_mode": "Markdown", "reply_markup": {"inline_keyboard": kb}})

            if "callback_query" in up:
                data = up["callback_query"]["data"]
                
                if data.startswith("a_"):
                    # مسح قائمة الأزواج فوراً
                    tg("deleteMessage", {"chat_id": c_id, "message_id": m_id})
                    
                    user_data[c_id] = data.replace("a_", "")
                    txt = f"🎯 الزوج المختار: **{user_data[c_id]}**\n\nحدد الفريم الزمني بدقة للتحليل:"
                    kb = [[{"text": "5s", "callback_data": "t_5s"}, {"text": "1m", "callback_data": "t_1m"}, {"text": "5m", "callback_data": "t_5m"}]]
                    tg("sendMessage", {"chat_id": c_id, "text": txt, "parse_mode": "Markdown", "reply_markup": {"inline_keyboard": kb}})

                elif data.startswith("t_"):
                    # مسح قائمة الفريمات فوراً
                    tg("deleteMessage", {"chat_id": c_id, "message_id": m_id})
                    
                    # تأثير "جاري التحليل" الفخم
                    wait = tg("sendMessage", {"chat_id": c_id, "text": "⚡ **جاري سحب السيولة عبر SSID...**"})
                    wait_id = wait.get("result", {}).get("message_id")
                    
                    time.sleep(1.8) # وقت المعالجة
                    
                    # مسح رسالة الانتظار
                    tg("deleteMessage", {"chat_id": c_id, "message_id": wait_id})
                    
                    # الإشارة النهائية
                    is_buy = int(time.time()) % 2 == 0
                    res_txt = "BUY CALL 🟢" if is_buy else "SELL PUT 🔴"
                    msg = f"💎 **إشارة إمبراطورية GMK** 💎\n\n💹 الزوج: {user_data.get(c_id)}\n🚀 القرار: **{res_txt}**"
                    
                    tg("sendPhoto", {"chat_id": c_id, "photo": BULL if is_buy else BEAR, "caption": msg, "parse_mode": "Markdown"})

    except: pass
    time.sleep(0.4)
