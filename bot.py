import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import date, time

CUMPLES = [
    {'nombre': 'Mily', 'fecha': date(1997, 8, 7)},
    {'nombre': 'Ale', 'fecha': date(1996, 8, 5)}
]

def start(update: Update, context: CallbackContext) -> None:
    # print('update.message')
    # print(update.message)

    # print('update.bot')
    # print(update.bot)

    # print('update')
    # print(update)

    chat_id = update.message.chat_id
    t = time(10, 00, 00, 000000)
    context.job_queue.run_daily(alarm, t,days=tuple(range(7)), context=update, name='bDay')
    text = 'Po po po po po'
    update.message.reply_text(text)


def alarm(context: CallbackContext) -> None:
    job = context.job
    cumple=False
    today = date.today()
    for i in CUMPLES:
        if(i['fecha'].day == today.day and i['fecha'].month == today.month):
            cumple=True
            edad = today.year-i['fecha'].year
            texto='Muchas Felicidades '+i['nombre']+' en tus '+str(edad)+' años'
            context.bot.send_message(job.context, text=texto)

    if(cumple==False):
        context.bot.send_message(job.context, text='Nadie cumple hoy')
    else:
        context.bot.send_message(job.context, text='Ya lo felicite!!!')


def testAlarm(context: CallbackContext) -> None:
    job = context.job
    texto='Mensaje de prueba que se ejecuta cada 1 min'
    context.bot.send_message(job.context, text=texto)


def test(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    i = 60
    context.job_queue.run_repeating(testAlarm, i)
    text = 'El mensaje de prueba comienza a correr ahora'
    update.message.reply_text(text)


def stop_test(bot, update, job_queue):
    job_queue.stop()
    bot.send_message(chat_id=update.message.chat_id,text='Prueba detenida!')


def main() -> None:
    updater = Updater(os.environ['TOKEN'])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("test", test))
    dispatcher.add_handler(CommandHandler("stop", stop_test))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()