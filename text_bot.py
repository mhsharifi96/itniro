#!/usr/bin/python
# -*- coding: latin-1 -*-
Hired_text="""#آگهی_استخدام
{0}
#{1}

#{2}
#عنوان_شغلی:{3}
#نوع استخدام


✍توضیحات:

{4}

ارسال رزومه از طریق:
📩 ایمیل:{5}
📥 تلگرام:{6}

💠 #کانال_IT_نیرو : 
@itniro
 استخدام های معتبر و خاص it👇
https://telegram.me/joinchat/AAAAAEEzBkS44DoLP2bQeQ"""

class text_Bot(object):
    def __init__(self):
        self.Hired_Text=Hired_text


    def hired_text(self):
        print "I am in text bot "
        return self.Hired_Text

