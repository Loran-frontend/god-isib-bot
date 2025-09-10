from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

TOKEN = open("./token.txt").readline()

async def mention_index(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.effective_chat is None:
        return
    
    if "@all" in update.message.text:
        chat_id = update.effective_chat.id
				
        admins = await context.bot.get_chat_administrators(chat_id)

        if all(update.effective_user.id != int(f) for f in open('./adminlist.txt').readline().split()):
            return

        mentions = []
        for admin in admins:
            user = admin.user
            if user.is_bot or any(user.id == int(f) for f in open('./blacklist.txt').readline().split()):
                continue
            link = f"[{'ㅤ'}](tg://user?id={user.id})"
            mentions.append(link)


        if mentions:
            await update.message.reply_text(
                "".join(mentions),
                parse_mode=ParseMode.MARKDOWN
            )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), mention_index))
    app.run_polling()

if __name__ == "__main__":
    main()
