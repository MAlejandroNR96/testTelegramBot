import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from datetime import date, time

CUMPLES = [
    {'nombre': 'Mily', 'fecha': date(1997, 8, 10)},
    {'nombre': 'Meli', 'fecha': date(2003, 8, 9)},
    {'nombre': 'Ale', 'fecha': date(1996, 8, 12)},
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
    print('LLEGO')
    job = context.job
    texto='Mensaje de prueba que se ejecuta cada 1 min'
    context.bot.send_message(job.context, text=texto)


def test(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    i = 2
    context.job_queue.run_repeating(testAlarm, i, context=chat_id, name=str(chat_id))
    text = 'El mensaje de prueba comienza a correr ahora'
    update.message.reply_text(text)


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def stop_test(bot, update):
    chat_id = bot.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), update)
    text = 'Prueba detenida' if job_removed else 'La prueba no se esta ejecutando'
    bot.message.reply_text(text)


def main() -> None:
    updater = Updater(os.environ['TOKEN'])
    # updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("test", test))
    dispatcher.add_handler(CommandHandler("stop", stop_test))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
