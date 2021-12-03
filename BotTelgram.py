import random
import telebot 
from datetime import date , datetime
from khayyam import JalaliDatetime
from gtts import gTTS

bot = telebot.TeleBot("5047922019:AAF3x9idQ_O7dLJTQt6tI8KK-jR8w7qvjcI")

@bot.message_handler(commands='start')
def start(message):
    payamstart = "سلام خوش آمديد" + message.from_user.first_name
    bot.reply_to(message , payamstart )

@bot.message_handler(commands=['help'])
def help(message):
    show = """/game بازی حدس اعداد \n
/max بزرگ ترین عدد در یک آرایه\n
/argmax ایندکس بزرگترین عدد در یک آرایه\n
/age محاسبه سن\n
/voice تبديل متن به صدا"""
    bot.reply_to(message , show)

@bot.message_handler(commands='game')
def bazi(message):
    user = bot.reply_to(message," يك عدد بين يك تا 10 رو حدس بزن ")
    global adad
    adad = random.randint(1,10)
    bot.register_next_step_handler(user , bazi2)

def bazi2(user):
    
    if int(user.text) == adad:
        bot.reply_to(user, "درست حدس زدي")

    elif int(user.text) > adad:
        user = bot.reply_to(user, "كوچيكتر")
        bot.register_next_step_handler(user , bazi2)

    else :        
        user = bot.reply_to(user, "بزرگتر")
        bot.register_next_step_handler(user , bazi2)

@bot.message_handler(commands='age')
def age(message):
    user = bot.reply_to(message , 'تاريخ تولد خود را وارد كنيد  (مثال : 1400/9/10)')
    bot.register_next_step_handler(user , age2)

def age2(user):
    tarikh = user.text.split("/")
    sen = JalaliDatetime.now() - JalaliDatetime(tarikh[0] , tarikh[1] , tarikh[2] )
    Sen = sen.days//365
    bot.send_message(user.chat.id ,Sen)

@bot.message_handler(commands=['voice'])
def Voice(message):
    txt = bot.reply_to(message , 'متن به زبات انگليسي را وارد كنيد')
    bot.register_next_step_handler(txt , Voice2)

def Voice2(txt):
    v = gTTS(text = txt.text , lang = 'en' , slow = False)
    v.save('v.mp3')
    v = open('v.mp3' , 'rb')
    bot.send_voice(txt.chat.id , v )

@bot.message_handler(commands='max')
def Max(message):
    a = bot.reply_to(message , "يك آرايه از اعداد وارد كنيد به صورتي كه هر عدد با , جدا شده باشند")
    bot.register_next_step_handler(a ,  Max2 )

def Max2(a) :
    arr = a.text.split(',')
    num = max(arr)
    bot.send_message(a.chat.id ,  num)

@bot.message_handler(commands='argmax')
def argmax(message):
    a = bot.reply_to(message , "يك آرايه از اعداد وارد كنيد به صورتي كه هر عدد با , جدا شده باشند")
    bot.register_next_step_handler(a , argmax2 )

def argmax2(a) :
    arr = a.text.split(',')
    index = arr.index(max(arr))
    bot.send_message(a.chat.id ,  index)
    
bot.infinity_polling()