from pyrogram import Client, filters
from pyrogram.enums import MessageServiceType
from pyrogram.errors import FloodWait
import asyncio

# നിന്റെ വിവരങ്ങൾ ഇവിടെ നൽകുക
API_ID = "28390522"
API_HASH = "bb6e4438855b6c9ac8d9f0d999a664c4"
BOT_TOKEN = "7906597848:AAFjMbx4k4L_3uOZ7HzkQdjQmtT86udr3tk"

app = Client("JoinDeleterBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 **CleanGate ബോട്ട് സജീവമാണ്!**\n\n"
        "ആളുകൾ കയറുന്നതും ഇറങ്ങുന്നതുമായ മെസ്സേജുകൾ മാത്രം ഞാൻ ഡിലീറ്റ് ചെയ്യും. "
        "മറ്റ് മെസ്സേജുകൾക്കൊന്നും ഒരു കുഴപ്പവും സംഭവിക്കില്ല. "
        "എന്നെ ഗ്രൂപ്പിൽ അഡ്മിൻ ആക്കിയാൽ ഉടൻ പണി തുടങ്ങും!"
    )

# ബോട്ടിനെ അഡ്മിൻ ആക്കിയാൽ അറിയിപ്പ് നൽകാൻ
@app.on_message(filters.service)
async def handle_service(client, message):
    chat_id = message.chat.id

    # പുതിയ ആളുകൾ ജോയിൻ ചെയ്യുമ്പോൾ (New Members)
    if message.new_chat_members:
        # അത് ബോട്ട് തന്നെയാണോ എന്ന് നോക്കുന്നു
        for member in message.new_chat_members:
            if member.is_self:
                await client.send_message(chat_id, "🚀 **Join msg delete started!**")
        
        # ജോയിൻ മെസ്സേജ് ഡിലീറ്റ് ചെയ്യുന്നു
        try:
            await message.delete()
        except:
            pass

    # ആളുകൾ ഗ്രൂപ്പ് വിട്ടു പോകുമ്പോൾ (Left Members)
    elif message.left_chat_member:
        try:
            await message.delete()
        except:
            pass

# പഴയ മെസ്സേജുകൾ ക്ലീൻ ചെയ്യാൻ (ബോട്ട് ആഡ് ആയ ഉടനെ മാത്രം)
@app.on_message(filters.new_chat_members)
async def clean_history(client, message):
    for member in message.new_chat_members:
        if member.is_self:
            async for msg in client.get_chat_history(message.chat.id, limit=500):
                # ഇവിടെയാണ് ഫിൽറ്റർ - ജോയിൻ/ലെഫ്റ്റ് മെസ്സേജ് ആണെങ്കിൽ മാത്രം ഡിലീറ്റ് ചെയ്യും
                if msg.service in [MessageServiceType.NEW_CHAT_MEMBERS, MessageServiceType.LEFT_CHAT_MEMBER]:
                    try:
                        await msg.delete()
                        await asyncio.sleep(0.4) # സ്പാം ആവാതിരിക്കാൻ
                    except:
                        continue

app.run()
