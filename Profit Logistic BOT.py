#модули
import telebot
from telebot import types


bot = telebot.TeleBot('6067890505:AAHV00C1-80IEkmw4iAnFh4BPR1OvIZ39EU')
CHAT_ID = '-1001501911197'

#переменные константы______________________________________________________________________________________________
course_rub = 13


#настройка клавиатуры______________________________________________________________________________________________
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_price = types.KeyboardButton(text="Рассчитать стоимость📱💸")
    button_course = types.KeyboardButton(text="Актуальный Курс💹")
    button_reviews = types.KeyboardButton(text="Отзывы📨")
    button_add_reviews = types.KeyboardButton(text="Оставить отзыв")
    markup.add(button_reviews, button_course, button_price, button_add_reviews)
    bot.send_message(message.chat.id, "Привет! Чем я могу помочь?", reply_markup=markup)



#блок кнопки отзывы______________________________________________________________________________________________
@bot.message_handler(func=lambda message: message.text == "Отзывы📨")
def send_reviews(message):
    markup = types.InlineKeyboardMarkup()
    button_channel = types.InlineKeyboardButton(text="Перейти к отзывам", url="https://t.me/pl_reviews")
    markup.add(button_channel)
    bot.send_message(message.chat.id, "Отзывы от наших реальных покупателей👇🏿", reply_markup=markup)


#блок кнопки оставить отзыв______________________________________________________________________________________________

@bot.message_handler(func=lambda message: message.text == "Оставить отзыв")
def send_feedback(message):
    bot.send_message(message.chat.id, 'Пишите отзыв в сообщении ниже.')
def echo_all(message):
    # Пересылаем сообщение в указанный чат
    bot.forward_message(CHAT_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, 'Спасибо за обратную связь!')    # Отправляем сообщение с благодарностью


#блок кнопки курса______________________________________________________________________________________________
@bot.message_handler(func=lambda message: message.text == "Актуальный Курс💹")
def send_course(message):
    bot.send_message(message.chat.id, f"Текущий курс💱\n1 CN¥ = {course_rub} ₽UB")

#блок кнопки расчитать стоимость______________________________________________________________________________________________
@bot.message_handler(func=lambda message: message.text == "Рассчитать стоимость📱💸")
def ask_amount(message):
    bot.send_message(message.chat.id, "💸Введите стоимость вещи в юанях💸")

@bot.message_handler(func=lambda message: True)
def handle_amount(message):
    global amount
    amount = message.text
    if not amount.isdigit():
        bot.send_message(message.chat.id, "Вы ввели не число. Пожалуйста, введите число.")
        return

    ask_category(message.chat.id, int(amount))



def ask_category(chat_id, amount):
    markup = types.InlineKeyboardMarkup()
    button_obuv = types.InlineKeyboardButton(text="Обувь", callback_data="category_shoes")
    button_other = types.InlineKeyboardButton(text="Другое", callback_data="category_other")
    markup.add(button_obuv, button_other)
    bot.send_message(chat_id, "Выберите категорию товара👇🏿", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_category(call):
    if call.data == "category_shoes":
        total_amount = (int(amount) * course_rub) * 1.10 + 1500
        bot.send_message(call.message.chat.id, f"Сумма: {int(total_amount)}")
    elif call.data == "category_other":
        total_amount = (int(amount) * course_rub) * 1.10 + 1000
        bot.send_message(call.message.chat.id, f"Сумма: {int(total_amount)}")
    markup = types.InlineKeyboardMarkup()
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)



# ---------



bot.polling()
