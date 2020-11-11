from models.students import Students
from views import keyboards
from views.student_check import identify_student


def start_command(update, context):
    identify_student(update)

    text = 'Тут приветственный текст, информация о курсе и о том как осуществлять запись через этого бота.'
    update.message.reply_text(text, reply_markup=keyboards.main_kb)

