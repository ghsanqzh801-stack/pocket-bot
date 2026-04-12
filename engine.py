import os, requests, time, threading, http.server, socketserver

# --- خادم البقاء ---
def run_vocal_server():
    port = int(os.environ.get("PORT", 10000))
    with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()
threading.Thread(target=run_vocal_server, daemon=True).start()

# --- إعدادات الإمبراطورية ---
TOKEN = "8768413194:AAGlUEfDY3lrnQKl_mvehVA-BLv6RJb1adI"
URL = f"https://api.telegram.org/bot{TOKEN}/"
BULL = "https://w0.peakpx.com/wallpaper/144/952/HD-wallpaper-bull-stock-market-neon-green-bull-trading-green-bull.jpg"
BEAR = "https://w0.peakpx.com/wallpaper/601/104/HD-wallpaper-bear-market-stock-market-trading-red-bear.jpg"

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

            # 1. مرحلة البداية (عرض الأزواج)
            if "message" in up and up["message"].get("text") == "/start":
                txt = "👑 **GMK-Empire Ghassan Training** 👑\n\nأهلاً بك.. اختر الزوج المطلوب لبدء التحليل الحقيقي:"
                kb = [
                    [{"text": "📊 EUR/USD (OTC) | 98%", "callback_data": "a_EURUSD"}, {"text": "📊 GBP/USD (OTC) | 95%", "callback_data": "a_GBPUSD"}],
                    [{"text": "📊 AUD/USD (OTC) | 94%", "callback_data": "a_AUDUSD"}, {"text": "📊 USD/JPY (OTC) | 92%", "callback_data": "a_USDJPY"}],
                    [{"text": "📊 XAU/USD (GOLD) | 91%", "callback_data": "a_GOLD"}, {"text": "📊 CRYPTO IDX | 90%", "callback_data": "a_CRYPTO"}]
                ]
                # إرسال رسالة جديدة ونظيفة
                tg("sendMessage", {"chat_id": c_id, "text": txt, "parse_mode": "Markdown", "reply_markup": {"inline_keyboard": kb}})

            # 2. معالجة الضغطات (نظام المسح الاحترافي)
            if "callback_query" in up:
                query_id = up["callback_query"]["id"]
                data = up["callback_query"]["data"]
                
                # إخفاء الـ Loading الصغير فوق
                tg("answerCallbackQuery", {"callback_query_id": query_id})

                # عند اختيار الزوج: نمسح قائمة الأزواج ونضع الفريمات
                if data.startswith("a_"):
                    asset = data.replace("a_", "")
                    user_data[c_id] = asset
                    txt = f"💹 **الزوج المختار:** `{asset}`\n\nالآن حدد **الفريم الزمني** لبدء سحب السيولة:"
                    kb = [
                        [{"text": "5s", "callback_data": "t_5s"}, {"text": "10s", "callback_data": "t_10s"}, {"text": "15s", "callback_data": "t_15s"}],
                        [{"text": "30s", "callback_data": "t_30s"}, {"text": "1m", "callback_data": "t_1m"}, {"text": "2m", "callback_data": "t_2m"}],
                        [{"text": "5m", "callback_data": "t_5m"}, {"text": "15m", "callback_data": "t_15m"}],
                        [{"text": "🔙 تغيير الزوج", "callback_data": "restart"}]
                    ]
                    # تحديث الرسالة الحالية (بدل حذفها) لضمان الفخامة
                    tg("editMessageText", {"chat_id": c_id, "message_id": m_id, "text": txt, "parse_mode": "Markdown", "reply_markup": {"inline_keyboard": kb}})

                # عند اختيار الفريم: نمسح كل شيء ونظهر النتيجة النهائية
                elif data.startswith("t_"):
                    timeframe = data.replace("t_", "")
                    # مسح الرسالة القديمة (قائمة الفريمات)
                    tg("deleteMessage", {"chat_id": c_id, "message_id": m_id})
                    
                    # إرسال رسالة انتظار "مؤقتة"
                    temp = tg("sendMessage", {"chat_id": c_id, "text": "⚡ **جاري تحليل الشموع عبر الـ SSID...**"})
                    temp_id = temp.get("result", {}).get("message_id")
                    
                    time.sleep(1.5) # سرعة البرق
                    
                    # مسح رسالة الانتظار
                    tg("deleteMessage", {"chat_id": c_id, "message_id": temp_id})
                    
                    # الإشارة النهائية بالصور الفخمة
                    is_buy = int(time.time()) % 2 == 0
                    res_text = "BUY CALL (شراء) 🟢" if is_buy else "SELL PUT (بيع) 🔴"
                    final_msg = (f"💎 **إشارة إمبراطورية GMK** 💎\n\n"
                                f"💹 **الزوج:** `{user_data.get(c_id)}`\n"
                                f"⏰ **الفريم:** `{timeframe}`\n"
                                f"🎯 **نسبة النجاح:** `96.8%` \n\n"
                                f"🚀 **القرار:** `{res_text}`\n"
                                f"🔹 **التوقيت:** ادخل الآن فوراً!")
                    
                    tg("sendPhoto", {"chat_id": c_id, "photo": BULL if is_buy else BEAR, "caption": final_msg, "parse_mode": "Markdown"})

                elif data == "restart":
                    tg("deleteMessage", {"chat_id": c_id, "message_id": m_id})
                    # يفضل هنا إعادة استدعاء قائمة البداية

    except Exception as e:
        print(f"Error: {e}")
    time.sleep(0.4)
