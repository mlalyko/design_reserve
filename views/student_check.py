# models
from models.students import Students, Rating


def add_new_student(update):
    new_student = Students(chat_id=update.message.from_user.id, username=update.message.from_user.username,
                           first_name=update.message.from_user.first_name, last_name=update.message.from_user.last_name)

    students_rating = Rating()
    students_rating.registrations, students_rating.confirmations, students_rating.visits = 0, 0, 0
    new_student.rating = students_rating

    new_student.save()


def identify_student(update):
    existing_student = Students.objects(chat_id=update.message.from_user.id)

    if not existing_student:
        add_new_student(update)
        existing_student = Students.objects(chat_id=update.message.from_user.id)

    return existing_student.first()

