from datetime import datetime

from telegram.ext import ConversationHandler

from models.lessons import Lessons, SignedUpStudents
from models.students import Students
from views import keyboards
from views.student_check import identify_student

REMOVE_REG = 1


def show_students_registrations(update, context):
    existing_student = identify_student(update)

    def find_lessons_dates(list_with_ids):
        list_with_dates = []

        for lesson_id in list_with_ids:
            existing_lesson = Lessons.objects(id=lesson_id)
            existing_lesson = existing_lesson.first() if existing_lesson else None
            if existing_lesson:
                list_with_dates.append(existing_lesson.date.strftime('%d.%m.%y (%a)'))

        return list_with_dates

    registrations_dates = find_lessons_dates(existing_student.registrations)
    awaiting_dates = find_lessons_dates(existing_student.awaiting)

    text = ''
    if registrations_dates:
        text += 'Вы записаны на следующие занятия:\n'
        text += ', '.join(registrations_dates)
    if awaiting_dates:
        text += '\nВы стоите в ожидании на эти занятия:\n'
        text += ', '.join(awaiting_dates)

    if not text:
        text = 'Здесь будет информация о ваших записях, чтобы записаться - нажмите "Свободные занятия"'
        update.message.reply_text(text, reply_markup=keyboards.main_kb)
        return ConversationHandler.END
    else:
        text += '\n\nЕсли вы хотите отменить какую-либо запись - нажмите дату на кнопке'
        update.message.reply_text(text, reply_markup=keyboards.lessons_dates_kb(registrations_dates))
        return REMOVE_REG


def remove_registration(update, context):
    received_text = update.effective_message.text

    if received_text == 'Отмена':
        text = 'Вы отменили запись на открытый урок'
        update.message.reply_text(text, reply_markup=keyboards.main_kb)
        return ConversationHandler.END

    existing_student = identify_student(update)

    wanted_date = datetime.strptime(received_text[:8], '%d.%m.%y').date()
    existing_lesson = Lessons.objects(date=wanted_date)
    existing_lesson = existing_lesson.first() if existing_lesson else None

    if existing_lesson:
        for student in existing_lesson.signed_up_students:
            if existing_student.id == student.student:
                existing_lesson.signed_up_students.remove(student)
                existing_lesson.save()
        for lessons_id in existing_student.registrations:
            if existing_lesson.id == lessons_id:
                existing_student.registrations.remove(lessons_id)
                existing_student.save()
        text = f'Вы успешно отменили запись на занятие {existing_lesson.date}'
    else:
        text = 'Произошла ошибка, занятие не найдено'

    # если ранее все места были заняты, а теперь одно освободилось 
    if len(existing_lesson.signed_up_students) + 1 == existing_lesson.slots:
        slot_opened(existing_lesson)
        
    update.message.reply_text(text, reply_markup=keyboards.main_kb)
    return ConversationHandler.END


def slot_opened(existing_lesson):
    if existing_lesson.awaiting_students:
        first_awaiting_student = existing_lesson.awaiting_students[0]
        existing_student = Students.objects(id=first_awaiting_student)

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
