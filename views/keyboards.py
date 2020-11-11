from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from models.lessons import Lessons

cancel_kb = ReplyKeyboardMarkup([['Отмена']], resize_keyboard=True)
main_kb = ReplyKeyboardMarkup([['Свободные занятия', 'Мои записи']], resize_keyboard=True)


def lessons_dates_kb(lessons_dates):
    row_1, row_2, row_3 = [], [], []
    row_4 = ['Отмена']

    for i in lessons_dates:
        if len(row_1) != 4:
            row_1.append(lessons_dates[lessons_dates.index(i)])
        elif len(row_2) != 4:
            row_2.append(lessons_dates[lessons_dates.index(i)])
        else:
            row_3.append(lessons_dates[lessons_dates.index(i)])

    keyboard = [row_1, row_2, row_3, row_4]

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

