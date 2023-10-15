from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import db

from asyncio import sleep
from PIL import Image
import os, time


@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_start(client, message):
  file = getattr(message, message.media.value)
  filename = file.file_name  
  if file.file_size > 2000 * 1024 * 1024:
     return await message.reply_text("Sᴏʀʀy Bʀᴏ Tʜɪꜱ Bᴏᴛ Iꜱ Dᴏᴇꜱɴ'ᴛ Sᴜᴩᴩᴏʀᴛ Uᴩʟᴏᴀᴅɪɴɢ Fɪʟᴇꜱ Bɪɢɢᴇʀ Tʜᴀɴ 2Gʙ")

  try:
    await message.reply_text(
      text=f"**__Pʟᴇᴀꜱᴇ Eɴᴛᴇʀ Nᴇᴡ Fɪʟᴇɴᴀᴍᴇ...__**\n\n**Oʟᴅ Fɪʟᴇ Nᴀᴍᴇ** :- `{filename}`",
	  reply_to_message_id=message.id,  
	  reply_markup=ForceReply(True)
    )    
    await sleep(30)
  except FloodWait as e:
    await sleep(e.value)
    await message.reply_text(
      text=f"**__Pʟᴇᴀꜱᴇ Eɴᴛᴇʀ Nᴇᴡ Fɪʟᴇɴᴀᴍᴇ...__**\n\n**Oʟᴅ Fɪʟᴇ Nᴀᴍᴇ** :- `{filename}`",
	  reply_to_message_id=message.id,  
	  reply_markup=ForceReply(True)
    )
  except:
    pass
@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
  reply_message = message.reply_to_message
  if (reply_message.reply_markup) and isinstance(reply_message.reply_markup, ForceReply):
    new_name = message.text 
    await message.delete() 
    msg = await client.get_messages(message.chat.id, reply_message.id)
    file = msg.reply_to_message
    media = getattr(file, file.media.value)
    if not "." in new_name:
      if "." in media.file_name:
        extn = media.file_name.rsplit('.', 1)[-1]
      else:
        extn = "mkv"
      new_name = new_name + "." + extn
    await reply_message.delete()

    # Check if the downloads directory exists and is empty.
    if os.path.exists("downloads/") and not os.listdir("downloads/"):
        # Remove the downloads directory.
        os.rmdir("downloads/")

    button = [[InlineKeyboardButton("📁 Dᴏᴄᴜᴍᴇɴᴛ",callback_data = "upload_document")]]
    if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
      button.append([InlineKeyboardButton("🎥 Vɪᴅᴇᴏ", callback_data = "upload_video")])
    elif file.media == MessageMediaType.AUDIO:
      button.append([InlineKeyboardButton("🎵 Aᴜᴅɪᴏ", callback_data = "upload_audio")])
    await message.reply(
      text=f"**Sᴇʟᴇᴄᴛ Tʜᴇ Oᴜᴛᴩᴜᴛ Fɪʟᴇ Tyᴩᴇ**\n**• Fɪʟᴇ Nᴀᴍᴇ :-**`{new_name}`",
      reply_to_message_id=file.id,
      reply_markup=InlineKeyboardMarkup(button)
    )
@Client.on_callback_query(filters.regex("upload"))
async def doc(bot, update):   
  new_name = update.message.text
  new_file_name = new_name.split(":-")[1]

  try:
    await update.message.reply_chat_action("typing")
    file = await update.message.download()
  except FloodWait as e:
    await update.message.reply_chat_action("cancel")
    await update.message.reply_text(
      text=f"**Unable to download file!**\n**Reason:** FloodWait ({e.value} seconds)."
    )
    return

  if os.path.exists(f"downloads/{new_file_name}"):
    await update.message.reply_text(
      text=f"**File already exists!**\n**Please choose a different name.**"
    )
  else:
    os.rename(file, f"downloads/{new_file_name}")
    await update.message.reply_chat_action("cancel")
    await update.message.reply_text(
        text=f"**File renamed successfully!**\n**New file name:** `{new_file_name}`"
    )
