# plugins/admin_panel.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from info import AUTH_USERS
from database.admin import ban_user, unban_user, is_banned, total_users
from database.broadcast import broadcast_message

@Client.on_message(filters.command("admin") & filters.user(AUTH_USERS))
async def admin_panel(client: Client, message: Message):
    total = await total_users()
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Broadcast", callback_data="broadcast")],
        [InlineKeyboardButton("🚫 Ban User", callback_data="ban"),
         InlineKeyboardButton("✅ Unban User", callback_data="unban")],
        [InlineKeyboardButton("👥 Total Users", callback_data="stats")]
    ])
    await message.reply_text(f"👮‍♂️ Admin Panel\nTotal Users: {total}", reply_markup=buttons)

@Client.on_callback_query(filters.user(AUTH_USERS))
async def admin_callbacks(client: Client, query: CallbackQuery):
    data = query.data
    if data == "stats":
        count = await total_users()
        await query.message.edit_text(f"📊 Total Users: {count}")
    elif data == "broadcast":
        await query.message.edit_text("📢 Reply to any message with `/broadcast` to send it to all users.")
    elif data == "ban":
        await query.message.edit_text("✏️ Send user ID to ban.")
        user_msg = await client.listen(query.message.chat.id)
        await ban_user(int(user_msg.text))
        await query.message.reply_text("✅ User banned.")
    elif data == "unban":
        await query.message.edit_text("✏️ Send user ID to unban.")
        user_msg = await client.listen(query.message.chat.id)
        await unban_user(int(user_msg.text))
        await query.message.reply_text("✅ User unbanned.")

@Client.on_message(filters.command("broadcast") & filters.user(AUTH_USERS))
async def broadcast_handler(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("📢 Reply to a message to broadcast it.")
    
    await message.reply_text("🚀 Broadcasting started...")
    total, success, failed = await broadcast_message(client, message.reply_to_message)
    await message.reply_text(f"📢 Broadcast finished!\n👥 Total: {total}\n✅ Sent: {success}\n❌ Failed: {failed}")
