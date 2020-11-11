def cancel_action(update, context):
    text = 'Вы отменили действие.'
    update.message.reply_text(text)