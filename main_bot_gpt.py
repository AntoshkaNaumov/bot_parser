import openai
import telebot
from API_keys import api_key, bot_token


openai.api_key = api_key
bot = telebot.TeleBot(bot_token)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=message.text,
    temperature=0.5,
    max_tokens=1000,
    top_p=1.0,
    frequency_penalty=0.5,
    presence_penalty=0.0,
  )
  bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])


bot.polling()
