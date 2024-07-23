from typing import Final
from telegram import Update
from telegram.ext import Application, Updater, CommandHandler, MessageHandler, filters, ContextTypes
import requests
# import ollama
# response = ollama.chat(model='llama3', messages=[
#     {
#         'role': 'user',
#         'content': 'Xin chao, Tôi là yamakun',
#     },
# ])
# print(response['message']['content'])

TOKEN: Final = "7488319479:AAFKQrrvc8LWQoo7e1wV7HA4IL1mlY4t0AA"
BOT_USERNAME: Final = "@yyamakun_bot"

history = []
# context = {
#     "role": "user",
#     "content": "Bạn là AI được tạo bởi chàng trai Yamakun, vì Yamakun và cống hiến cho Yamakun. Ngôn ngữ chính của bạn là tiếng Việt, ngôn ngữ phụ là tiếng anh. Tôi sẽ cho bạn một số ngữ cảnh: Dũng và Long là bạn cùng giường với nhau mỗi tối. "
# }
# history.append(context)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, I am yamakun")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yes, how can i help you")

async def custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("What do you want to say?")
# Define chatbot initialization

def handle_response(text:str) -> str:
     
    question = {
    "role": "user",
    "content": text
}
    history.append(question)
    json_payload = {
    "model": "Yamakun",
    "messages": history,
    "stream": False
}
    output = requests.post("http://localhost:11434/api/chat", json=json_payload).json()
    answer = output["message"]
    history.append(answer)
    print(history)
    return output["message"]["content"]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  message_type: str = update.message.chat.type
  text = update.message.text
  print(f"User: {update.message.chat.id} in {message_type} says: {text}")
  if message_type =="group":
    if BOT_USERNAME in text:
      new_text = text.replace(BOT_USERNAME)
      response = handle_response(new_text)
    else:
      return
  else:
    response = handle_response(text)
  print(f"Bot says: {response}")
  await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
    
if __name__=="__main__":
  print("Bot started")
  app = Application.builder().token(TOKEN).build()
    
  app.add_handler(CommandHandler("start", start))
  app.add_handler(CommandHandler("help", help))
  app.add_handler(CommandHandler("custom", custom))

  app.add_handler(MessageHandler(filters.TEXT, handle_message))
  app.add_error_handler(error)
    
  print("Bot is polling")
  app.run_polling(poll_interval=5)
  

  