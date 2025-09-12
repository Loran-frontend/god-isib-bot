from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
# "8395701237:AAHZiNHoMzs9lnNR9NTLemdpTKoecLsOofU"
TOKEN = open("./token.txt").readline()

admins_list = {
        1276598143, # Семён - Староста 0
        2095826659, # Максим - Староста 1
        5009803881, # Данила - Профорг
        8153282128, # Влад - Раб Профорга
        }

black_list = {
        1746213456, # Катя (ЯМЫ ФАНАТЫ КАТИ)
        996260323,   # Толя наставник
        1736773311 # Матвейка наставник
        }

group1 = {
1175208027,
584312843,
1815248006,
697709850,
1478545245,
1121673400,
1395482054,
1893943741,
1276598143,
2100475307,
1688088015,
1368856632,
1465564068,
1214079884,
5115570578,
1924085691
}
group2 = {
5009803881,
6317653408,
1232616455,
1541779325,
5883900279,
1199008111,
5708397650,
8153282128,
1161503640,
7037168258,
2001106979,
2095826659,
1659787315
}

SMS = "Друзья,ㅤоченьㅤважноеㅤсообщение!"
SMS1 = "Уведомлениеㅤ1ㅤподгруппы!"
SMS2 = "Уведомлениеㅤ2ㅤподгруппы!"

async def mention_index(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.effective_chat is None:
        return
    
    if "@group1" in update.message.text:
        if not update.effective_user.id in group1 and not update.effective_user.id in admins_list:
            return
        
        admins = await context.bot.get_chat_administrators(update.effective_chat.id) # Получение админов
        users = [user.user for user in admins if not(user.user.is_bot) and not(user.user.id in black_list) and (user.user.id in group1)] # Проверка на бота и черный список + перевод в user

        mentions = ""

        for letter, user in zip(SMS1, users):
            mentions += '[' + str(letter) + '](tg://user?id=' + str(user.id) + ')'
  
        if mentions:
            await update.message.reply_text(
                mentions+SMS1[len(users):],
                parse_mode=ParseMode.MARKDOWN
            )

    if "@group2" in update.message.text:
        if not update.effective_user.id in group2 and not update.effective_user.id in admins_list:
            return
        
        admins = await context.bot.get_chat_administrators(update.effective_chat.id) # Получение админов
        users = [user.user for user in admins if not(user.user.is_bot) and not(user.user.id in black_list) and (user.user.id in group2)] # Проверка на бота и черный список + перевод в user
        
        mentions = ""

        for letter, user in zip(SMS2, users):
            mentions += '[' + str(letter) + '](tg://user?id=' + str(user.id) + ')'
  
        if mentions:
            await update.message.reply_text(
                mentions+SMS2[len(users):],
                parse_mode=ParseMode.MARKDOWN
            )

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
