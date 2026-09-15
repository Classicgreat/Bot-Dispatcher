import telebot
from alchemy import *
import os
import settings

token = settings.token

bot = telebot.TeleBot(token)

def registration(message,msg):
    db.register(str(message.from_user.id),str(message.chat.id))
    if db.get(message.from_user.id).admin==1:
        main(msg)
    else:
        bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id,text="User added")

def main(message,text="Enter message to send"):
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,text=text)
    bot.register_next_step_handler(message, sending_request, message)

def sending_request(message,msg):
    bot.delete_message(chat_id=message.chat.id,message_id=message.id)
    bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id,text="Message sending...")
    data=db.get_all()
    print(message.content_type)
    if message.content_type=="text":
        sending(message,msg,data,text)
    elif message.content_type=="photo":
        sending(message,msg,data,img)
    elif message.content_type=="document":
        sending(message,msg,data,doc)
    elif message.content_type=="video":
        sending(message,msg,data,video)
    elif message.content_type=="poll":
        sending(message,msg,data,poll)
    else:
        main(msg,text="Error: type not found")

def sending(message,msg,data,func):
    for i in range(len(data)):
        #if data[i].id!=str(message.from_user.id):
        func(message,data[i].chat_id)
    #bot.send_message("-1001924995428", message.text)
    main(msg)

def text(message,chat_id):
    bot.send_message(chat_id,message.text)
def img(message,chat_id):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f"{message.photo[-1].file_name}.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_photo(chat_id, downloaded_file, caption=message.caption)
    os.remove(f"{message.photo[-1].file_name}.jpg")
def doc(message,chat_id):
    fileID = message.document.file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f"{message.document.file_name}.doc", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_document(chat_id, downloaded_file, caption=message.caption)
    os.remove(f"{message.document.file_name}.doc")
def video(message,chat_id):
    fileID = message.video.file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f"{message.video.file_name}.mp4", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_video(chat_id, downloaded_file, caption=message.caption)
    os.remove(f"{message.video.file_name}.mp4")
def poll(message,chat_id):
    bot.send_poll(chat_id,message.poll.question,message.poll.options)


@bot.message_handler(commands=["start"])
def start(message):
    #bot.delete_message(chat_id=message.chat.id,message_id=message.id)
    msg=bot.send_message(message.chat.id, "Starting...")
    if not(db.get(message.from_user.id)):
        registration(message,msg)
    else:
        if db.get(message.from_user.id).admin==1:
            main(msg)
        else:
            bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id,text="User already in system")


if __name__=="__main__":
    db=Database("databaze")
    bot.polling(none_stop=True)
