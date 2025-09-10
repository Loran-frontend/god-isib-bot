from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

TOKEN = open("./token.txt").readline()

admins_list = {
        1276598143, # Семён - Староста 0
        2095826659, # Максим - Староста 1
        5009803881, # Данила - Профорг
        8153282128, # Влад - Раб Профорга
        }
black_list = {
        1746213456, # Катя (ЯМЫ ФАНАТЫ КАТИ)
        }

SMS = "Друзья,ㅤоченьㅤважноеㅤсообщение!"

async def mention_index(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.effective_chat is None:
        return
    
    if "@all" in update.message.text:
        if not update.effective_user.id in admins_list: # Проверка, что отправитель админ
            return

        admins = await context.bot.get_chat_administrators(update.effective_chat.id) # Получение админов
        users = [user.user for user in admins if not(user.user.is_bot) and not(user.user.id in black_list)] # Проверка на бота и черный список + перевод в user
        
        mentions = ""

        for letter, user in zip(SMS, users):
            mentions += '[' + str(letter) + '](tg://user?id=' + str(user.id) + ')'
  
        if mentions:
            await update.message.reply_text(
                mentions+SMS[len(users):],
                parse_mode=ParseMode.MARKDOWN
            )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), mention_index))
    app.run_polling()

if __name__ == "__main__":
    main()
