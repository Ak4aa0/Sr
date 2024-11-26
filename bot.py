import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice

API_KEY = "7074630284:AAHQwTnbqLsR0i3nOklLUD39XOj_UXqWacc"
bot = telebot.TeleBot(API_KEY)
admin_id = "5379744467"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()

    donate_buttons = [
        InlineKeyboardButton("10 Stars ⭐", callback_data="pay_10_stars"),
        InlineKeyboardButton("50 Stars ⭐", callback_data="pay_50_stars"),
        InlineKeyboardButton("100 Stars ⭐", callback_data="pay_100_stars"),
        InlineKeyboardButton("250 Stars ⭐", callback_data="pay_250_stars"),
        InlineKeyboardButton("500 Stars ⭐", callback_data="pay_500_stars"),
        InlineKeyboardButton("999 Stars ⭐", callback_data="pay_999_stars")
    ]

    # Adjusting buttons as a single column
    markup.add(donate_buttons[0])
    markup.add(donate_buttons[1])
    markup.add(donate_buttons[2])
    markup.add(donate_buttons[3])
    markup.add(donate_buttons[4])
    markup.add(donate_buttons[5])

    bot.send_message(
        message.chat.id,
        f"Hello {message.from_user.first_name}!\n\n"
        "You can support the bot owner with stars by choosing one of the options below:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("pay_"))
def process_donation(call):
    star_amount = int(call.data.split("_")[1].split("_")[0])
    prices = [LabeledPrice(label=f"{star_amount} Stars", amount=star_amount)]

    bot.send_invoice(
        chat_id=call.message.chat.id,
        title="Support the Bot Owner",
        description=f"Donate {star_amount} Stars to support the bot owner",
        provider_token="",
        currency="XTR",
        prices=prices,
        start_parameter=f"donation_{star_amount}_stars", 
        invoice_payload=f"donation_{star_amount}_stars"
    )

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    star_amount = int(message.successful_payment.invoice_payload.split("_")[1].split("_")[0])
    bot.send_message(message.chat.id, f"Thank you for your donation of {star_amount} Stars ⭐!")
    bot.send_message(admin_id, f"Successful donation from user: {message.from_user.first_name} "
                               f"(@{message.from_user.username})\nAmount: {star_amount} Stars")

bot.polling()
