import http.server
import socketserver
import threading
import os

# --- قسم السيرفر الوهمي عشان Render ما يطفي البوت ---
def run_vocal_server():
    class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is Running!")

    # Render بيستخدم بورت 10000 غالباً بشكل تلقائي
    port = int(os.environ.get("PORT", 10000))
    with socketserver.TCPServer(("", port), HealthCheckHandler) as httpd:
        print(f"Serving at port {port}")
        httpd.serve_forever()

# تشغيل السيرفر في خلفية الكود
threading.Thread(target=run_vocal_server, daemon=True).start()

# --- حط كود البوت تبعك (التحليل وتليجرام) تحت هاد السطر ---
print("البوت بدأ العمل الآن...")

# ملاحظة لغسان: انسخ كود الـ WebSocket والتحليل تبعك هون
# وإذا بدك بساعدك بدمجهم سوا بس ابعتلي الكود الأساسي
