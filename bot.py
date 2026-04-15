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

# Render Port Handling
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# --- ഇതാണ് നീ ചോദിച്ച സ്റ്റാർട്ട് മെസ്സേജ് ---
@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 **ഹലോ മുത്തേ, ഞാൻ റെഡിയാണ്!**\n\n"
        "എന്നെ നിന്റെ ഗ്രൂപ്പിലോ ചാനലിലോ **Admin** ആക്കി ഇട്ടാൽ മതി. "
        "ആളുകൾ ജോയിൻ ചെയ്യുമ്പോൾ വരുന്ന ആ മെസ്സേജുകൾ എല്ലാം ഞാൻ സ്പോട്ട് ഡിലീറ്റ് ആക്കിക്കോളാം.\n\n"
        "**പവർ ഓഫ് ക്ലീൻ ഗേറ്റ്!** 🧹"
    )

@app.on_message(filters.service)
async def handle_service(client, message):
    chat_id = message.chat.id
    
    # സർവീസ് മെസ്സേജുകൾ ഡിലീറ്റ് ചെയ്യുന്നു
    if message.service in [MessageServiceType.NEW_CHAT_MEMBERS, MessageServiceType.LEFT_CHAT_MEMBER]:
        try:
            await message.delete()
        except:
            pass

    # ഗ്രൂപ്പിൽ ബോട്ട് ആഡ് ആകുമ്പോൾ വരുന്ന മെസ്സേജ്
    if message.new_chat_members:
        for member in message.new_chat_members:
            if member.is_self:
                await client.send_message(chat_id, "🚀 **Join msg delete started!**")

async def main():
    threading.Thread(target=run_health_server, daemon=True).start()
    await app.start()
    print("Bot is live with all features!")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
