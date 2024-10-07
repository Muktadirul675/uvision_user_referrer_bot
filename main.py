TOKEN = "7837368352:AAHvnJYCnGyCG5YQj5ColvXKKe4Fs_Zxjpc"
import telebot
from telebot.types import Message
from manage import *
import matplotlib.pyplot as plt
from flask import Flask, request

bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/',methods=['GET'])
def hello():
    return "Hello"

@app.route('/' + TOKEN, methods=['POST'])
def receive_update(request):
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the bot!")

@bot.message_handler(commands=['info'])
def info(message):
    user = User(message.from_user)
    reply_message = f"""
        Hello there. Your info: \nName: {user}
    """
    if user.obj.is_admin:
        reply_message += '\nYou are an admin.'
    bot.reply_to(message, reply_message)

@bot.message_handler(commands=['greet'])
def greet(message):
    bot.reply_to(message, f"Assalamualaikum, {message.from_user.first_name}")

@bot.message_handler(commands=['stats'])
def stats(message: Message):
    chat = message.chat
    if chat.type == 'supergroup':
        x,y = get_stats(f"{chat.id}")
        plt.bar(x, y)
        plt.title("User Referral Chart")
        plt.xlabel("Referrers")
        plt.ylabel("Referrals")

        # Display the chart
        plt.savefig("chart.png")
        caption = ""
        for i in range(len(x)):
            caption += f"{x[i]} added {y[i]} peoples\n"
        with open("chart.png","rb") as chart:
            bot.send_photo(chat.id, chart, caption=caption)
    else:
        bot.reply_to(message, "This command is only available in groups")

# Function to welcome new users
@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    referrer_user = User(message.from_user)
    # print(message.from_user)
    referrer_user.add_referrals(message)

if __name__ == "__main__":
    print("Server starting...")
    app.run()
