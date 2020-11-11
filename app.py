# telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackQueryHandler

# config
from data.config import TG_TOKEN

# other
from datetime import datetime
from loguru import logger

from views import main
from views.admin import add_new_lessons
from views.cancel_action import cancel_action
from views.start_command import start_command
from views.lessons_schedule import show_lessons, LESSONS_DATE, CRAFT_THING, sign_up, thing_to_craft
from views.students_registrations import show_students_registrations, REMOVE_REG, remove_registration

logger.add("data/logs/main.log", format="{time} {level} {message}", level="DEBUG")


def app():
    print('Start ' + str(datetime.today()))

    updater = Updater(token=TG_TOKEN, use_context=True)
    dp = updater.dispatcher.add_handler

    dp(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Свободные занятия'), show_lessons)],
        states={
            LESSONS_DATE: [MessageHandler(Filters.text, sign_up, pass_user_data=True)],
            CRAFT_THING: [MessageHandler(Filters.text, thing_to_craft, pass_user_data=True)]},
        fallbacks=[CommandHandler('cancel', cancel_action)]
    ))
    dp(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Мои записи'), show_students_registrations)],
        states={
            REMOVE_REG: [MessageHandler(Filters.text, remove_registration, pass_user_data=True)]},
        fallbacks=[CommandHandler('cancel', cancel_action)]
    ))

    dp(MessageHandler(Filters.regex('Мои записи'), show_students_registrations))
    # dp(MessageHandler(Filters.regex(r'Отписаться'), subscriptions.unsubscribe))
    # button_one = Selections.objects(number=1).first().name
    # button_two = Selections.objects(number=2).first().name
    # dp(MessageHandler(Filters.regex(f'^({button_one}|{button_two}|🔪 Chaky рекомендует)$'), selections.selections))
    # dp(MessageHandler(Filters.regex('^(За день|За неделю|За месяц|За год)$'), graph.graph))
    #
    # # query-обработчик
    # def query_data_handler(update, context):
    #     query = update.callback_query
    #     query.answer()
    #
    #     if query.data in ['backward_op_h', 'forward_op_h']:
    #         operations_history.operation_history_arrows(query)
    #     elif query.data in ['backward_news', 'forward_news']:
    #         news.news_arrows(query)
    #     elif query.data in ['sectors_back', 'sectors_fwd']:
    #         sectors_arrows(query)
    #     elif query.data in ['bid_back', 'bid_forward']:
    #         bidding.bid_arrows(query)
    #     elif query.data in ['selections_back', 'selections_forward']:
    #         selections.selections_arrows(context, query)
    #     elif query.data in ['portfolio_back', 'portfolio_forward']:
    #         portfolio_info.portfolio_arrows(query)
    #
    # dp(CallbackQueryHandler(query_data_handler))

    # Add new lessons
    dp(ConversationHandler(
        entry_points=[CommandHandler('add_new_lessons', add_new_lessons.lessons_dates_request)],
        states={
            add_new_lessons.DATE_OF_LESSONS: [MessageHandler(Filters.text, add_new_lessons.new_lessons_handler,
                                                             pass_user_data=True)]},
        fallbacks=[CommandHandler('cancel', cancel_action)]
    ))

    dp(CommandHandler('start', start_command))

    dp(MessageHandler(Filters.text, start_command))

    updater.start_polling()
    updater.idle()

    print('Finish')


if __name__ == '__main__':
    app()
# except Exception as e:
#     logger.error(f'{e} in app.py')
