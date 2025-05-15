import telebot 
from telebot import types
import requests


bot = telebot.TeleBot('7761604165:AAF86f2zHBidKdurquVWFNMyKzCz8JyKQEo')
@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "Привет"):
        bot.send_message(message.chat.id, text="Привет! Я бот, который поможет распознать тип и качество кожи лица по фотографии. Для удобства напиши 'Задать вопрос' и ты увидишь весь функционал бота!)")
    elif(message.text == "Задать вопрос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Что может бот?")
        btn2 = types.KeyboardButton("Кожа")
        btn3 = types.KeyboardButton("Распознать тип кожи ")
        btn4 = types.KeyboardButton("Помощь")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, btn3, btn4, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)
    
    elif(message.text == "Что может бот?"):
        bot.send_message(message.chat.id, "Я ваш личный помощник по вашему здоровью!")                                                                                  
    
    elif message.text == "Кожа":
        bot.send_message(message.chat.id, text="типы кожи: fsdfd")

    elif message.text == "Распознать тип кожи":
        bot.send_message(message.chat.id, text="Идет анализ... ⌛️")
    elif message.text == "Помощь":
            bot.send_message(message.chat.id, text="Чем могу помочь?")

    
    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Помощь")
        button2 = types.KeyboardButton("Задать вопрос")
        button3 = types.KeyboardButton("Привет")
        markup.add(button1, button2, button3)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован.. Напиши мне 'Привет'")
    
    @bot.message_handler(content_types=['photo'])
    def handle_photo(message):
        bot.send_message(message.chat.id, "Фото получено, начинаю анализ... ⌛️")

        # Получаем файл
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Сохраняем локально
        with open("temp_image.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)

        # Отправляем файл на сервер FastAPI
        try:
            files = {'file': open('temp_image.jpg', 'rb')}
            response = requests.post("http://localhost:8000/predict", files=files)
            if response.status_code == 200:
                result = response.json()['result']
                bot.send_message(message.chat.id, result)
            else:
                bot.send_message(message.chat.id, "Ошибка при анализе изображения. Попробуйте позже.")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {e}")  



bot.polling(none_stop=True)