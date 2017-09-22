#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import imgkit
#from bottle import route, run, static_file
import thread
import time 
from store import TinyDBStore
from text_bot import text_Bot

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters,CommandHandler, CallbackQueryHandler

import time

FIELDS = [
    {
        'name': 'company_name',
        'message': 'نام شرکت/استارپ خود را وارد کنید '
    },
    {
        'name': 'sharp_word',
        'message': """ کلمات کلیدی خود را وارد کنید 
        به عنوان مثال:
        #gitiserver #backend #python #django #flask""",
    },
    {
        'name': 'job_title',
        'message': 'عنوان شغلی به عنوان مثال :برنامه نویس ارشد پایتون',
    },
    {
        'name': 'place',
        'message': 'لطفا محل شرکت خود را وارد کنید ',
        #'required': False
    },
    {
        'name': 'Description',
        'message': 'توضیحات مد نظر خود را وارد کنید',
    },
    {
        'name': 'email',
        'message': 'ایمیل خود /شرکت  ',
        #'required': False
    },
    {
        'name':'finish',
        'message':"برای پایان یافتن و مشاهده پیش نمایش آگهی عبارت داخل پرانتز را تایپ فرمایید (/finish)",
    },
]

def parse_fields(field, value):
    if field == 'date':
        cal = parsedatetime.Calendar()
        time_struct, parse_status = cal.parse(value)
        timestamp = time.mktime(datetime(*time_struct[:6]).timetuple())
        return str(int(timestamp))
    return value
def user_ID(bot,update):
    user_id = update.message.from_user.id
    print user_id
    return user_id

def split_text(description):
    description=description.split(".")
    li_text=[]
    for i in description:
        if i:
            li_text.append("<li>"+i+"</li>")
    return ''.join(li_text)

class CommandsModule(object):
    def __init__(self):
       
        self.Text_bot=text_Bot()
        self.store = TinyDBStore()
        self.handlers=[
            CommandHandler('start',self.welcome_bot),
            CommandHandler('help',self.welcome_bot),
            CallbackQueryHandler(self.button),
            MessageHandler([Filters.text], self.message),
            CommandHandler('finish',self.bot.send_photo(chat_id=user_id1,caption="salam",photo=open(img_file, 'rb')))]
        

    def get_handlers(self):
        return self.handlers
    
    def welcome_bot(self,bot,update):
          #  print'update:',update
            user_id = update.message.from_user.id
            self.store.new_draft(user_id)
            bot.sendMessage(update.message.chat_id,
                        text=""" به آی-تی نیرو خوش آمدید لطفا برای اینکه چون که زیر شود شما باید  زیر باید متن الیکی """)
            #keyboard = [[InlineKeyboardButton(text='ساخت تبلیغ', switch_inline_query=":)")], []]
            keyboard = [[InlineKeyboardButton("درج آگهی استخدادم", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2')]]
            user_id=update.message.chat_id
            bot.sendMessage(
            update.message.chat_id,
            text="Event created!",
            reply_markup=InlineKeyboardMarkup(keyboard))
            
    def message(self, bot, update):
        user_id=update.message.from_user.id
        text = update.message.text
     #   print "store  : " ,self.store
        draft= self.store.get_draft(user_id)
        # print "draft : ",draft
        if draft:
            event = draft['event']
            #print "event : ",event 
            current_field = draft["current_field"]
            field = FIELDS[current_field]
            # print "field : ",field
            event[field['name']] = parse_fields(field['name'], text)
            # print "event[field['name']] : ",event[field['name']]
            current_field=current_field+1
            print "current_field: ",current_field
            self.update_draft(bot, event, user_id, update, current_field)
    
    def update_draft(self, bot, event, user_id, update, current_field):
        self.store.update_draft(user_id, event, current_field)

        if current_field <= len(FIELDS) - 1:
            bot.sendMessage(
                update.message.chat_id,
                text=FIELDS[current_field]['message']
            )
        else:
            event['user_id'] = user_id
            self.create_event(bot, update, event)

    
    def finish(self,bot,update):
        print " i am in finish"
        user_id1=update.message.from_user.id
        # print " : ",user_id1 

        draft= self.store.get_draft(user_id1)
        # print "final text : ",draft
        company_name=draft['event']['company_name']
        place=draft['event']['place']
        email=draft['event']['email']
        Description=split_text(Description)
        key_word=draft['event']['sharp_word']
        job_title=draft['event']['job_title']
        final_text=self.Text_bot.hired_text()
        final_text=final_text.format(company_name,place,key_word,job_title,Description,email,"telegram")
        print "last final test :",final_text
#######################################
        main_file="/home/fox/Documents/telegram_bot/itniro/page/index.html"
        file=open(main_file,"r+")
        text=file.read()
        dic={"IOS":job_title,"email":email,"company":company_name,"<li></li>":Description}
        text=self.replace_all(text,dic)
        file.close()
        second_file="/home/fox/Documents/telegram_bot/itniro/page/index2.html"
        file2=open(second_file,"w")
        file2.write(text)
        file2.close()
        img_file="/home/fox/Documents/telegram_bot/itniro/img/{}.png".format(user_id1)
        OUTPUT="/home/fox/Documents/telegram_bot/itniro/img/index.png"
        imgkit.from_file(second_file,img_file)
        self.send_photos(user_id1,img_file)
        #bot.send_photo(chat_id=user_id1,caption="salam",photo=open(img_file, 'rb'))



	
    def replace_all(self,text, dic):
        for i, j in dic.iteritems():
            text = text.replace(i, j)
        return text
    def send_photos(chat_id,img_file):
        bot.send_photo(chat_id=user_id1,caption="salam",photo=open(img_file, 'rb'))
        


    def button(self,bot,update):
         #chat_id = bot.get_updates()[-1].message.chat_id
         query = update.callback_query
         #print("qury ::::::::::::::::::::::::::::::::::::::::: ",query.message.id)
         print "update.message ::::: :::::  ",update.message
          
         if query.data=="1":
                print "man in jaaaaaaaaaaaaaaa a hassssssstam :)"
                print("qury ::::::::::::::::::::::::::::::::::::::::: ",query.message.chat_id) 
                chat_id=query.message.chat_id

                keyboard = [[InlineKeyboardButton("درج آگهی استخدادم ", callback_data='o1'),
                   InlineKeyboardButton("ساخت رزومه", callback_data='o2')],

                  [InlineKeyboardButton("درباره ما", callback_data='o3')]]


                reply_markup = InlineKeyboardMarkup(keyboard)
                #bot.edit_message_text(user_id,'لطفا یکی از گزینه های زیر را انتحاب فرمایید', reply_markup=reply_markup)
            

                bot.edit_message_text(text="Selected option: %s" % query.data,
                       chat_id=query.message.chat_id,
                       message_id=query.message.message_id)
                bot.sendMessage(
                    chat_id=query.message.chat_id,
                    text="Event created!",
                    reply_markup=InlineKeyboardMarkup(keyboard))
         if query.data=="o1":
            chat_id=query.message.chat_id
            
            bot.edit_message_text(text="لطفا به آگهی زیر دقت کنید",chat_id=query.message.chat_id,message_id=query.message.message_id)

           
            text_info="""#آگهی_79
#تهران 
#shatel
 
 گروه شرکت های شاتل " کارشناس تولید محتوای وب " در واحد شاتل لند استخدام می‌کند:

مهارت‌های موردنیاز:

•  مدرک کارشناسی (فارغ التحصیلان مهندسی کامپیوتر، علوم کامپیوتر و آی تی در اولویت خواهند بود) 


 متقاضیان رزومه خود را به ایمیل زیر ارسال نمایند:

email:  career@shatelland.com 


💠 #کانال_IT_نیرو : 
@itniro
 استخدام های معتبر و خاص it👇
https://telegram.me/joinchat/AAAAAEEzBkS44DoLP2bQeQ"""
            bot.sendMessage(
                    chat_id=query.message.chat_id,
                    text=text_info,
                    reply_markup=None)
            bot.sendMessage(
                    chat_id=query.message.chat_id,
                    text="نام شرکت خود را وارد کنید",
                    reply_markup=None)
            #bot.get_updates(timeout=10)
            

                    


