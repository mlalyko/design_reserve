from telegram import ParseMode
from telegram.ext import ConversationHandler

from views import keyboards
from models.lessons import Lessons
from datetime import date, datetime
from data.config import slots

DATE_OF_LESSONS = 1


def lessons_dates_request(update, context):
    # TODO: add admins root
    text = f'Пришли мне даты занятий через запятую в формате: 01.02.20, 18.03.20.'
    update.message.reply_text(text, reply_markup=keyboards.cancel_kb)

    return DATE_OF_LESSONS


def new_lessons_handler(update, context):
    received_text = update.effective_message.text

    try:
        lessons_dates = received_text.split(', ')
        lessons_dates = [datetime.strptime(i, '%d.%m.%y').date() for i in lessons_dates]
        successful_imported_dates = []

        for i in lessons_dates:
            if i not in [lesson.date for lesson in Lessons.objects()] and i > date.today():
                Lessons(date=i, slots=slots).save()
                successful_imported_dates.append(i.strftime('%d.%m.%y (%a)'))

        all_lessons_from_db = sorted([lesson.date for lesson in Lessons.objects()])
        text = f'Добавились даты: {", ".join(successful_imported_dates)}\n' \
               f'Все даты занятий: {", ".join([i.strftime("%d.%m.%y (%a)") for i in all_lessons_from_db])}'

        update.message.reply_text(text)

        return ConversationHandler.END

    except ValueError:
        text = 'Пришлите список дат <b>в формате: 01.02.20, 18.03.20</b>'
        update.message.reply_text(text, parse_mode=ParseMode.HTML)



