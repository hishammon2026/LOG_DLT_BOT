import asyncio
from pyrogram import Client, filters, idle
from pyrogram.enums import MessageServiceType

# നിന്റെ വിവരങ്ങൾ ഇവിടെ നൽകുക
API_ID = "28390522"
API_HASH = "bb6e4438855b6c9ac8d9f0d999a664c4"
BOT_TOKEN = "7906597848:AAFjMbx4k4L_3uOZ7HzkQdjQmtT86udr3tk"

app = Client("JoinDeleterBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 CleanGate ബോട്ട് സജീവമാണ്!")

@app.on_message(filters.service)
async def handle_service(client, message):
    chat_id = message.chat.id
    if message.new_chat_members or message.left_chat_member:
        try:
            await message.delete()
        except:
            pass
    if message.new_chat_members:
        for member in message.new_chat_members:
            if member.is_self:
                await client.send_message(chat_id, "🚀 **Join msg delete started!**")

# പുതിയ പൈത്തൺ വേർഷനുകൾക്ക് വേണ്ടിയുള്ള റണ്ണിംഗ് രീതി
async def main():
    await app.start()
    print("Bot is running...")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
