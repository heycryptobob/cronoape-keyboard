from telegram import *
from telegram.ext import *
from requests import *
from os import environ
from dotenv import load_dotenv
load_dotenv()

token = environ.get('TOKEN')
print("Token:", token)
updater = Updater(token=token)
dispatcher = updater.dispatcher

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
                with open(btn[1], "r") as file:
                    text = file.read()
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=text,
                        parse_mode=ParseMode.HTML
                    )
                    return
    
def newChatMember(update: Update, context: CallbackContext):
    keyboard = buildKeyboard()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to $CronoApe!", reply_markup=ReplyKeyboardMarkup(keyboard))

dispatcher.add_handler(CommandHandler("cronoape", startCommand))
dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))
dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, newChatMember))

updater.start_polling()
