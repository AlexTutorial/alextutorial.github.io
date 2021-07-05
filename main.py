import telebot
import config
import random
import threading
import sqlite3 as sl
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
print('Runned test bot')

qesqty = len(config.QUESTIONS)

check = False
allballs = 0
continuevar = ["Начнём!" , "Почти готово!" , "Последний вопрос!" , "Продолжим!" , "Далее!"]


def errorMSG(message, ERRCODE) :
    bot.send_message(message.chat.id , 'Похоже, что-то сломалось. Подождите, мы всё починим! Код ошибки: ' + ERRCODE + '🧑‍🔧')

def ask(message) :
    answer = 0
    check = False

    def true(message) :
        bot.send_message(message.chat.id , 'Правильно!')

    def false(message) :
        bot.send_message(message.chat.id , 'Нет!')

    def answvar(message , answers , var1 , var2 , var3 , var4) :
        answers = answers.replace("{" , '')
        answers = answers.replace("}" , '')
        answers = answers.replace("'" , '')
        answers = answers.replace("," , '\n')
        str1 = 'Варианты ответов: \n' + answers
        markup = types.ReplyKeyboardMarkup(row_width = 2 , resize_keyboard = True)
        item1 = types.KeyboardButton("1")
        item2 = types.KeyboardButton("2")
        item3 = types.KeyboardButton("3")
        item4 = types.KeyboardButton("4")
        markup.add(item1 , item2 , item3 , item4)
        bot.send_message(message.chat.id , str1.format(message.from_user , bot.get_me( )) , parse_mode = 'html' ,
                         reply_markup = markup)

    @bot.message_handler(content_types = ['text'])
    def lalala(message):
        nonlocal answer
        nonlocal check
        answer = 0
        if message.chat.type == 'private':
            if message.text == 'LOL!':
                bot.send_message(message.chat.id, 'LOOL')
            elif message.text == '1':
                check = True
                bot.send_message(message.chat.id, 'Вы выбрали вариант 1')
                answer = 1
            elif message.text == '2':
                check = True
                bot.send_message(message.chat.id, 'Вы выбрали вариант 2')
                answer = 2
            elif message.text == '3':
                check = True
                bot.send_message(message.chat.id, 'Вы выбрали вариант 3')
                answer = 3
            elif message.text == '4':
                check = True
                bot.send_message(message.chat.id, 'Вы выбрали вариант 4')
                answer = 4
            else :
                bot.send_message(message.chat.id, 'Сорян, я незнаю что ответить 😕')
        else:
            errorMSG(message, 'VAR_ERR')
            answer = 0
    def asking():
        nonlocal answer
        con = sl.connect('my-test.db')
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS results(name TEXT, score INTEGER)""")
        con.commit()
        nonlocal check

        global allballs
        currq = 1
        nextq = 2
        score = 0
        allballs = 0
        for i in range(qesqty):
            while answer != 0 or nextq == currq + 1:
                answer = 0
                if (currq == 1):
                    bot.send_message(message.chat.id,
                                     str(continuevar[0]) + ' ' + str(currq) + ' вопрос: ' + config.QUESTIONS.get(currq))
                elif (currq == qesqty - 1):
                    bot.send_message(message.chat.id,
                                     str(continuevar[1]) + ' ' + str(currq) + ' вопрос: ' + config.QUESTIONS.get(currq))
                elif (currq == qesqty):
                    bot.send_message(message.chat.id,
                                     str(continuevar[2]) + ' ' + str(currq) + ' вопрос: ' + config.QUESTIONS.get(currq))
                else :
                    bot.send_message(message.chat.id, str(continuevar[random.randint(3, 4)]) + ' ' + str(
                        currq) + ' вопрос: ' + config.QUESTIONS.get(currq))
                answers = str(config.VARIANTS.get(currq))
                threading.Thread(target = answvar, args = (message, answers, '1', '2', '3', '4')).start()
                # answvar(message, answers, '1', '2', '3', '4')
                nextq += 1
            while answer == 0 or nextq != currq + 1:
                if check == True:
                    ans = config.ANSWERS
                    balls = config.BALLS
                    # print(config.BALLS.get(currq))
                    print(currq , end = ' ')
                    print(answer)
                    allballs += int(config.BALLS.get(currq))
                    if int(answer) == int(ans.get(currq)) and int(answer) != 0:
                        bot.send_message(message.chat.id, 'Правильно!')
                        score += int(balls.get(currq))
                    else :
                        bot.send_message(message.chat.id , 'Нет!')
                    if (currq < len(config.QUESTIONS)) : currq += 1
                    check = False
        # nextq = 2

        userdata = [str(message.from_user.first_name) , int(score)]
        cur.execute("INSERT INTO results VALUES(?, ?);" , userdata)
        con.commit( )

        bot.send_message(message.chat.id , 'Тест пройден! Ваш результат: ' + str(score) + ' из ' + str(
            allballs) + '. Процент выполнения: ' + str(score / allballs * 100) + ' %')

    asking()


@bot.message_handler(commands = ['game'])
def startgame(message) :
    x = threading.Thread(target = ask, args = (message,))
    x.start( )

    bot.send_message(message.chat.id ,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, предлагаю вам пройти один тест. Начнём!".format(
                         message.from_user , bot.get_me( )),
                     parse_mode = 'html')


@bot.message_handler(commands = ['start'])
def welcome(message) :
    bot.send_message(message.chat.id , 'Добро пожаловать! Напишите /commands, и узнаете что я умею.')


@bot.message_handler(commands = ['commands'])
def welcome(message) :
    bot.send_message(message.chat.id , 'Запустить тест: /game \nКалькулятор: /calc')







@bot.callback_query_handler(func = lambda call : True)
def callback_inline(call) :
    try :

        # remove inline buttons
        # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Как дела?",
        # 	reply_markup=None)

        # show alert
        bot.answer_callback_query(callback_query_id = call.id , show_alert = False ,
                                  text = "")

    except Exception as e :
        print(repr(e))


# RUN
bot.polling(none_stop = True)
