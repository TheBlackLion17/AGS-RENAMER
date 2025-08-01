# plugins/rename.py

import os
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.progress import progress_for_pyrogram
from database.users import is_banned, check_user, get_caption, get_thumbnail
from info import AUTH_USERS, MAX_CONCURRENT_JOBS

@Client.on_message(filters.document | filters.video | filters.audio)
async def rename_handler(client: Client, message: Message):
    user_id = message.from_user.id

    # Ignore banned users
    if await is_banned(user_id):
        return await message.reply_text("🚫 You are banned from using this bot.")

    # Register user if new
    await check_user(user_id)

    # Download file
    media = message.document or message.video or message.audio
    file_name = media.file_name
    file_size = media.file_size

    download_path = f"./downloads/{user_id}/{file_name}"
    os.makedirs(os.path.dirname(download_path), exist_ok=True)

    m = await message.reply_text("⬇️ Downloading...")
    start_time = time.time()

    try:
        downloaded = await client.download_media(
            message,
            file_name=download_path,
            progress=progress_for_pyrogram,
            progress_args=("⬇️ Downloading...", m, start_time)
        )
    except Exception as e:
        return await m.edit(f"❌ Failed to download: `{e}`")

    # Ask for new file name
    await m.edit(f"✅ Downloaded `{file_name}`\n\nNow send me the new file name (with extension):")

    new_name_msg = await client.listen(message.chat.id)
    new_filename = new_name_msg.text

    if not new_filename or '.' not in new_filename:
        return await m.edit("❌ Invalid file name. Rename cancelled.")

    new_path = f"./downloads/{user_id}/{new_filename}"
    os.rename(downloaded, new_path)

    # Get user caption and thumbnail
    caption = await get_caption(user_id)
    thumbnail = await get_thumbnail(user_id)

    # Upload
    await m.edit("⬆️ Uploading...")
    try:
        await client.send_document(
            message.chat.id,
            document=new_path,
            file_name=new_filename,
            caption=caption.format(filename=new_filename, filesize=file_size),
            thumb=thumbnail if thumbnail else None,
            progress=progress_for_pyrogram,
            progress_args=("⬆️ Uploading...", m, time.time())
        )
        await m.delete()
    except Exception as e:
        await m.edit(f"❌ Failed to upload: `{e}`")
    finally:
        try:
            os.remove(new_path)
        except: pass
