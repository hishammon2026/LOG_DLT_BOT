import asyncio
import os
from pyrogram import Client, filters, idle
from pyrogram.enums import MessageServiceType
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# നിന്റെ വിവരങ്ങൾ
API_ID = "28390522"
API_HASH = "bb6e4438855b6c9ac8d9f0d999a664c4"
BOT_TOKEN = "7906597848:AAFjMbx4k4L_3uOZ7HzkQdjQmtT86udr3tk"

app = Client("JoinDeleterBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Render-ന്റെ പോർട്ട് പ്രശ്നം ഒഴിവാക്കാനുള്ള സർവർ
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running")

def run_health_server():
    # Render നൽകുന്ന പോർട്ട് എടുക്കുന്നു, ഇല്ലെങ്കിൽ 10000 ഉപയോഗിക്കുന്നു
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"Web server started on port {port}")
    server.serve_forever()

@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 CleanGate ബോട്ട് സജീവമാണ്!")

@app.on_message(filters.service)
async def handle_service(client, message):
    if message.new_chat_members or message.left_chat_member:
        try:
            await message.delete()
        except:
            pass
    if message.new_chat_members:
        for member in message.new_chat_members:
            if member.is_self:
                await client.send_message(message.chat.id, "🚀 **Join msg delete started!**")

async def main():
    # വെബ് സർവർ ബാക്ക്ഗ്രൗണ്ടിൽ റൺ ചെയ്യുന്നു
    threading.Thread(target=run_health_server, daemon=True).start()
    
    await app.start()
    print("Bot is live...")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
