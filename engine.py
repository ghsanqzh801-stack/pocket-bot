import http.server, socketserver, threading, os, requests, time

# 1. السيرفر الوهمي
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

# 2. الإعدادات والبيانات
TOKEN = "8768413194:AAGlUEfDY3lrnQKl_mvehVA-BLv6RJb1adI"
CHAT_ID = "7692680668"

def send_msg(text, keyboard=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    if keyboard: payload["reply_markup"] = {"inline_keyboard": keyboard}
    return requests.post(url, json=payload).json()

# القائمة الأساسية
def show_assets():
    assets = [
        {"n": "EUR/USD (OTC)", "p": 92, "s": "🔥 ممتاز"},
        {"n": "XAU/USD (OTC)", "p": 89, "s": "✅ جيد جداً"},
        {"n": "GBP/JPY (OTC)", "p": 85, "s": "⚠️ متوسط"},
    ]
    kb = [[{"text": f"📊 {a['n']} | {a['p']}% | {a['s']}", "callback_data": f"asset_{a['n']}"}] for a in assets]
    send_msg("✨ **لوحة التحكم الاحترافية** ✨\n\nاختر الزوج المطلوب للتحليل:", kb)

# قائمة الفريمات (بعد اختيار الزوج)
def show_timeframes(asset_name):
    times = [
        [{"text": "5 ثواني", "callback_data": "t_5s"}, {"text": "10 ثواني", "callback_data": "t_10s"}],
        [{"text": "15 ثانية", "callback_data": "t_15s"}, {"text": "30 ثانية", "callback_data": "t_30s"}],
        [{"text": "1 دقيقة", "callback_data": "t_1m"}, {"text": "5 دقائق", "callback_data": "t_5m"}],
        [{"text": "🔙 العودة للأزواج", "callback_data": "main_menu"}]
    ]
    send_msg(f"🎯 تم اختيار: **{asset_name}**\n\nالآن اختر **الفريم الزمني** ومدة الصفقة:", times)

# 3. محرك الاستقبال (المراقب)
last_id = 0
while True:
    try:
        res = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_id+1}").json()
        for up in res.get("result", []):
            last_id = up["update_id"]
            
            # معالجة الرسائل النصية
            if "message" in up:
                if up["message"].get("text") == "/start": show_assets()
            
            # معالجة ضغطات الأزرار (Callback)
            if "callback_query" in up:
                data = up["callback_query"]["data"]
                if data.startswith("asset_"):
                    show_timeframes(data.replace("asset_", ""))
                elif data == "main_menu":
                    show_assets()
                elif data.startswith("t_"):
                    send_msg(f"⚡ **جاري التحليل العميق...**\nالفريم: {data.replace('t_', '')}\nالنتيجة ستظهر خلال ثوانٍ ⏳")
                    # (هنا سنضع كود التحليل الحقيقي في الخطوة القادمة)
                    
    except: pass
    time.sleep(1)
