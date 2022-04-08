from telegram import *
from telegram.ext import *
from requests import *
from os import environ
from dotenv import load_dotenv

load_dotenv()

buttons = [
    [
        ["👓 Vision", "vision.txt" ],
        ["🛒 Buy $CronoApe", "buy.txt"],
        ["💹 Chart", "chart.txt"],
        ["🚀 Roadmap", "roadmap.txt" ],
    ],
    [
        ["🏛 Tax System", "tax.txt" ],
        ["💰 View $CRO Rewards", "rewards.txt"],
        ["🔀 Bridge To Cronos", "bridge.txt"],
    ],
    [
        ["📢 Marketing", "marketing.txt"],
        ["🛠 Utility", "utility.txt"],
        ["📱 Socials", "socials.txt"],
    ]
]

def buildKeyboard():
    keyboard = []
    for row in buttons:
        keyRow = []
        for btn in row:
            keyRow.append(KeyboardButton(btn[0]))
        keyboard.append(keyRow)
    return keyboard

def startCommand(update: Update, context: CallbackContext):
    keyboard = buildKeyboard()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Loading CronoApe Keyboard 🔥", reply_markup=ReplyKeyboardMarkup(keyboard))

def messageHandler(update: Update, context: CallbackContext):    
    for row in buttons:
        for btn in row:
            if btn[0] == update.message.text:
                print("Button pressed: ", update.message.text)
                with open(btn[1], "r") as file:
                    text = file.read()
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=text,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True
                    )
                    return
    
def newChatMember(update: Update, context: CallbackContext):
    keyboard = buildKeyboard()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to $CronoApe!", reply_markup=ReplyKeyboardMarkup(keyboard))


if __name__ == "__main__":
    print("Starting up the keyboard...")
    
    TOKEN = environ.get('TOKEN')
    NAME = environ.get('HEROKU_APP_NAME')
    PORT = environ.get('PORT')
    ENV = environ.get('PYTHON_ENV')

    print("TOKEN: ", TOKEN)
    print("HEROKU_APP_NAME: ", HEROKU_APP_NAME)
    print("PORT: ", PORT)
    print("ENV: ", PYTHON_ENV)

    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("cronoape", startCommand))
    dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, newChatMember))

    if ENV == "production":
        URL = f"https://{NAME}.herokuapp.com/{TOKEN}"
        print("URL: ", URL)
        
        updater.start_webhook(
            listen="0.0.0.0",
            port=int(PORT),
            url_path=TOKEN,
            webhook_url=URL
        )
        updater.idle()
    else:
        updater.start_polling()

    print("Keyboard is operational.")