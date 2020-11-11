from datetime import datetime

from telegram import ParseMode
from telegram.ext import ConversationHandler

from models.lessons import Lessons, SignedUpStudents
from models.students import Rating
from views import keyboards
from views.student_check import identify_student

LESSONS_DATE, CRAFT_THING = 1, 2


def show_lessons(update, context):
    all_dates = sorted([i.date for i in Lessons.objects()])
    all_dates = [i.strftime('%d.%m.%y (%a)') for i in all_dates]
    open_dates = [i.date.strftime('%d.%m.%y (%a)') for i in Lessons.objects() if len(i.signed_up_students) < i.slots]
    text = f'Расписание свободных занятий на ближайшее время:\n' \

    lessons_with_info = []
    for lesson in all_dates:
        if lesson in open_dates:
            lesson += ' 🟢'
        else:
            lesson += ' 🔴'

        lessons_with_info.append(lesson)
        text += f'{lesson}\n'

    text += '\n\n🟢 - есть свободные места\n🔴 - свободных мест нет, но можно встать в очередь и если они освободятся,' \
            'то вы сможете записаться'
    context.user_data['lessons_with_info'] = lessons_with_info

    update.message.reply_text(text, reply_markup=keyboards.lessons_dates_kb(lessons_with_info))
    return LESSONS_DATE


def sign_up(update, context):
    received_text = update.effective_message.text

    if received_text == 'Отмена':
        text = 'Вы отменили запись на открытый урок'
        update.message.reply_text(text, reply_markup=keyboards.main_kb, parse_mode=ParseMode.HTML)
        return ConversationHandler.END

    else:
        wanted_date = datetime.strptime(received_text[:8], '%d.%m.%y').date()
        existing_lesson = Lessons.objects(date=wanted_date)
        existing_lesson = existing_lesson.first() if existing_lesson else None

        if existing_lesson:
            context.user_data['existing_lesson'] = existing_lesson

            # если есть свободные места, то записывает на этот день
            if len(existing_lesson.signed_up_students) < existing_lesson.slots:
                existing_student = identify_student(update)

                if existing_lesson.id in existing_student.registrations:
                    text = 'Вы уже зарегистрированы на этот урок'
                    update.message.reply_text(text, reply_markup=keyboards.main_kb, parse_mode=ParseMode.HTML)
                    return ConversationHandler.END

                else:
                    text = f'Что вы планируете делать на уроке? '
                    update.message.reply_text(text, reply_markup=keyboards.cancel_kb, parse_mode=ParseMode.HTML)
                    return CRAFT_THING

            # если свободный мест нет, ставит в лист ожидания
            else:
                existing_student = identify_student(update)
                existing_student.awaiting.append(existing_lesson.id)
                existing_student.save()

                existing_lesson.awaiting_students.append(existing_student.id)
                existing_lesson.save()

                text = f'Вы добавились в лист ожидания на <b>{existing_lesson.date}</b>. Если кто-то откажется от ' \
                       f'посещения занятия, вы будете записаны и вам придёт оповещение.'

                update.message.reply_text(text, reply_markup=keyboards.main_kb, parse_mode=ParseMode.HTML)
                return ConversationHandler.END

        else:
            text = 'Нажмите на кнопку с выбором даты, чтобы записаться.'
            update.message.reply_text(
                text,
                reply_markup=keyboards.lessons_dates_kb(context.user_data.get('lessons_with_info')),
                parse_mode=ParseMode.HTML
            )


def thing_to_craft(update, context):
    received_text = update.effective_message.text

    if received_text == 'Отмена':
        text = 'Вы отменили запись на открытый урок'
        update.message.reply_text(text, reply_markup=keyboards.main_kb, parse_mode=ParseMode.HTML)
        return ConversationHandler.END

    else:
        existing_student = identify_student(update)
        existing_lesson = context.user_data.get('existing_lesson')

        existing_student.registrations.append(existing_lesson.id)
        existing_student.rating.registrations += 1
        existing_student.save()

        student_info = SignedUpStudents()
        student_info.student = existing_student.id
        student_info.confirmation = False
        student_info.craft_thing = received_text
        # TODO: нужно придумать прикольный расчёт какой-нибудь
        # student_info.probability_of_arrival =

        existing_lesson.signed_up_students.append(student_info)
        existing_lesson.save()

        text = f'Вы успешно зарегистрировались на свободный урок <b>{existing_lesson.date}</b>'
        update.message.reply_text(text, reply_markup=keyboards.main_kb, parse_mode=ParseMode.HTML)
        return ConversationHandler.END
