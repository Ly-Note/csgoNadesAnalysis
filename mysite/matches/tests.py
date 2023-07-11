from django.test import TestCase
import datetime,time
from django.utils import timezone
# Create your tests here.
class DateFormatCorrect(TestCase):

    def dateFormatCorrect(self):
   
        # 将格式字符串转换为时间戳
        a = "2023-04-18T07:00:16.2312175+08:00"
       # print time.mktime(time.strptime(a,"%a %b %d %H:%M:%S %Y"))
       # time = timezone.now() + datetime.timedelta(days=30)
        #future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)