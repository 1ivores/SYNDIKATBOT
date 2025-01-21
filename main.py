import asyncio
import logging
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Configs
BOT_TOKEN = "8027731709:AAEIYhW1t-8mNdX7ajcYCXJqR_xTgTDWMug"

# Admin check
async def is_admin(update: Update):
    user_id = update.effective_user.id
    member = await update.effective_chat.get_member(user_id)
    return member.status in ["administrator", "creator"]

# Helper to get user id from username
async def get_user_id_by_username(chat, username):
    if username.startswith("@"):  
        username = username[1:]
    try:
        member = await chat.get_member(username)  
        return member.user.id
    except Exception as e:
        logging.error(f"Error fetching user by username {username}: {e}")
        return None

# Command functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Bot started and ready to work! Use /help to see available commands.')

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("You're not an admin.")
        return

    user_id = None

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    elif context.args:
        username = context.args[0]
        user_id = await get_user_id_by_username(update.effective_chat, username)

    if not user_id:
        await update.message.reply_text("User not found. Reply to a message or provide a valid @username.")
        return

    await context.bot.ban_chat_member(update.effective_chat.id, user_id)
    await update.message.reply_text(f"User banned.")

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("You're not an admin.")
        return

    user_id = None

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    elif context.args:
        username = context.args[0]
        user_id = await get_user_id_by_username(update.effective_chat, username)

    if not user_id:
        await update.message.reply_text("User not found. Reply to a message or provide a valid @username.")
        return

    permissions = ChatPermissions(can_send_messages=False)
    await context.bot.restrict_chat_member(update.effective_chat.id, user_id, permissions=permissions)
    await update.message.reply_text(f"User muted.")

async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("You're not an admin.")
        return

    user_id = None

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    elif context.args:
        username = context.args[0]
        user_id = await get_user_id_by_username(update.effective_chat, username)

    if not user_id:
        await update.message.reply_text("User not found. Reply to a message or provide a valid @username.")
        return

    permissions = ChatPermissions(can_send_messages=True)
    await context.bot.restrict_chat_member(update.effective_chat.id, user_id, permissions=permissions)
    await update.message.reply_text(f"User unmuted.")

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("You're not an admin.")
        return

    user_id = None

    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
    elif context.args:
        username = context.args[0]
        user_id = await get_user_id_by_username(update.effective_chat, username)

    if not user_id:
        await update.message.reply_text("User not found. Reply to a message or provide a valid @username.")
        return

    await context.bot.ban_chat_member(update.effective_chat.id, user_id)
    await update.message.reply_text(f"User kicked.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("You're not an admin.")
        return
    await update.message.reply_text(
        "/start - Start the bot\n"
        "/ban - Ban the user (reply to the user's message or provide @username)\n"
        "/mute - Mute the user (reply to the user's message or provide @username)\n"
        "/unmute - Unmute the user (reply to the user's message or provide @username)\n"
        "/kick - Kick the user (reply to the user's message or provide @username)\n"
        "/help - Show this message"
    )

def main():
    try:
        # Build application
        print("Starting bot...")
        application = Application.builder().token(BOT_TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("ban", ban))
        application.add_handler(CommandHandler("mute", mute))
        application.add_handler(CommandHandler("unmute", unmute))
        application.add_handler(CommandHandler("kick", kick))
        application.add_handler(CommandHandler("help", help_command))

        # Run the bot
        print("Bot is running...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
