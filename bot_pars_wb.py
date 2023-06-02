import telebot
import requests
import csv
from model import Items
from API_keys import bot_token


# Initialize the Telegram bot
bot = telebot.TeleBot(bot_token)


# Wildberries parser function
#def parse_wb(url):
#    create_csv()
#    response = requests.get(url)
#    if response.status_code == 200:
#        items_info = Items.parse_obj(response.json()["data"])
#        save_csv(items_info)


# Wildberries parser function
def parse_wb(url):
    create_csv()
    page = 1
    limit = 300
    while True:
        response = requests.get(f"{url}&page={page}&limit={limit}")
        if response.status_code == 200:
            try:
                data = response.json()["data"]
                items_info = Items.parse_obj(data)

                if not items_info.products:
                    break
                save_csv(items_info)
                page += 1
            except (KeyError, ValueError) as e:
                print("Error parsing response:", e)
                print("Response content:", response.content)
                break
            else:
                print("Request failed with status code:", response.status_code)
                break


def create_csv():
    with open("wb_data.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'название', 'цена', 'бренд', 'продаж', 'рейтинг', 'в наличии'])


def save_csv(items):
    with open("wb_data.csv", mode="a", newline="", encoding='utf-8') as file:
        writer = csv.writer(file)
        for product in items.products:
            writer.writerow([product.id,
                            product.name,
                            product.salePriceU,
                            product.brand,
                            product.sale,
                            product.rating,
                            product.volume])


def send_file(user, file):
    doc = open(file, 'rb')
    bot.send_document(user, doc)


# Handle '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Wildberries parser bot!"
                          " Please enter the URL of the product you want to parse.")


# Handle incoming messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Get the URL from the user's message
    url = message.text.strip()
    # Check if the URL starts with "https://"
    if not url.startswith("https://"):
        bot.reply_to(message, "Please enter a valid URL starting with 'https://'")
        return
    # Parse Avito page
    product_data = parse_wb(url)
    bot.reply_to(message, 'Data has been parsed.')
    # send_file(message.from_user.id, "wb_data.csv")
    send_file(message.chat.id, 'wb_data.csv')


# Start the bot
bot.polling()
