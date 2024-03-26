import asyncio
import math
import os
import sys
import re
import urllib.request
import requests
import urllib3
import random
import string
import time
import json
from datetime import datetime
from PIL import Image
from urlextract import URLExtract
from telegraph import Telegraph, exceptions, upload_file
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from telethon import events, types, functions
from telethon.utils import get_peer_id, get_display_name
from telethon.tl.types import MessageService, MessageEntityMentionName, MessageActionChannelMigrateFrom, MessageEntityMentionName, InputPhoneContact
from telethon.errors import FloodWaitError
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import GetHistoryRequest, ImportChatInviteRequest, DeleteHistoryRequest, ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest, GetAdminedPublicChannelsRequest
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from . import zedub
from ..Config import Config
from ..utils import Zed_Vip
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import delete_conv
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..helpers import media_type, progress, thumb_from_audio, sanga_seperator
from ..helpers.functions import convert_toimage, convert_tosticker, vid_to_gif
from ..helpers.utils import _zedtools, _zedutils, _format, parse_pre, reply_id
from . import BOTLOG_CHATID, mention

extractor = URLExtract()

plugin_category = "الادوات"
ZGIF = gvarstatus("Z_GIF") or "(لمتحركه|لمتحركة|متحركه|متحركة)"
if not os.path.isdir("./temp"):
    os.makedirs("./temp")
gpsbb = '@openmap_bot'
storyz = '@tgstories_dl_bot'
ppdf = '@Photo22pdfbot'
LOGS = logging.getLogger(__name__)
PATH = os.path.join("./temp", "temp_vid.mp4")
Zel_Uid = zedub.uid
thumb_loc = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")
cancel_process = False

extractor = URLExtract()
telegraph = Telegraph()
r = telegraph.create_account(short_name=Config.TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]

def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")

def get_random_cat():
    api_url = 'https://api.thecatapi.com/v1/images/search'
    try:
        response = requests.get(api_url)
        cat_url = response.json()[0]['url']
        return cat_url
    except:
        return None

def get_chatgpt_response(question):
    url = f"https://chatgpt.apinepdev.workers.dev/?question={question}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["answer"]
    else:
        return None

async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_object = await event.client.get_entity(previous_message.sender_id)
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await event.client.get_me()
            user = self_user.id
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        if isinstance(user, int) or user.startswith("@"):
            user_obj = await event.client.get_entity(user)
            return user_obj
        try:
            user_object = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return user_object

async def get_names(phone_number):
    try:
        contact = InputPhoneContact(client_id=0, phone=phone_number, first_name="", last_name="")
        contacts = await zedub(functions.contacts.ImportContactsRequest([contact]))
        user = contacts.to_dict()['users'][0]
        username = user['username']
        if not username:
            username = "لايوجد"
        user_id = user['id']
        return username, user_id
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

# Copyright (C) 2022 Zed-Thon . All Rights Reserved
@zedub.zed_cmd(pattern="اضف وسائط (الحماية|الحمايه|الفحص|فحص) ?(.*)")
async def _(malatha): # Write Code by T.me/S_1_02
    if malatha.fwd_from:
        return
    zed = await edit_or_reply(malatha, "**⎉╎جـاري اضـافة فـار الكليشـة الكاملـة الـى بـوتك ...**")
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
        #     if BOTLOG:
        await malatha.client.send_message(
            BOTLOG_CHATID,
            "**⎉╎تم إنشاء حساب Telegraph جديد {} للدورة الحالية‌‌** \n**⎉╎لا تعطي عنوان url هذا لأي شخص**".format(
                auth_url
            ),
        )
    optional_title = malatha.pattern_match.group(2)
    if malatha.reply_to_msg_id: # Write Code by T.me/S_1_02
        start = datetime.now()
        r_message = await malatha.get_reply_message()
        r_caption = r_message.text
        input_str = malatha.pattern_match.group(1)
        if input_str in ["الحماية", "الحمايه"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            if r_caption: # Write Code by T.me/S_1_02
                addgvar("pmpermit_txt", r_caption)
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await zed.edit("**⎉╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://graph.org{}".format(media_urls[0]))
                addgvar("pmpermit_pic", vinfo)
                await zed.edit("**⎉╎تم تعييـن الكليشـة الكاملـة لـ {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶ ميديـا + كليشـة**\n**⎉╎ارسـل الان الامـر : ↶** `.الحماية تفعيل`\n\n**⎉╎قنـاة السـورس : @A1DIIU**".format(input_str))
        elif input_str in ["الفحص", "فحص"]:
            downloaded_file_name = await malatha.client.download_media(
                r_message, Config.TEMP_DIR
            )
            if r_caption: # Write Code by T.me/S_1_02
                addgvar("ALIVE_TEMPLATE", r_caption)
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await zed.edit("**⎉╎خطا : **" + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                vinfo = ("https://graph.org{}".format(media_urls[0]))
                addgvar("ALIVE_PIC", vinfo)
                await zed.edit("**⎉╎تم تعييـن الكليشـة الكاملـة لـ {} .. بنجـاح ☑️**\n**⎉╎المتغيـر : ↶ ميديـا + كليشـة**\n**⎉╎ارسـل الان الامـر : ↶** `.فحص`\n\n**⎉╎قنـاة السـورس : @A1DIIU**".format(input_str))
    else:
        await zed.edit("**⎉╎بالـرد ع صـورة او ميديـا لتعييـن الفـار ...**")

@zedub.zed_cmd(pattern=r"حفظ (.+)")
async def save_post(event):
    post_link = event.pattern_match.group(1)
    if not post_link:
        return await edit_or_reply(event, "**- يرجـى إدخـال رابـط المنشـور المقيـد بعـد الامـر ؟!**")
    save_dir = "media"
    os.makedirs(save_dir, exist_ok=True)
    if post_link.startswith("https://t.me/c/"):
        try:
            post_id = post_link.split("/")
            if len(post_id) >= 2:
                channel_username_or_id = int(post_id[-2])
                message_id = int(post_id[-1])
            else:
                return
        except Exception as e:
            return await edit_or_reply(event, f"**- اووبـس .. حدث خطأ أثناء حفظ الرسالة\n- تفاصيل الخطأ :**\n {str(e)}\n\n**- استخـدم الامـر الآخـر لـ حفـظ الملفـات المقيـده 🔳:\n- ارسـل** ( .احفظ ) **+ رابـط او بالـرد ع رابـط مقيـد**")
    else:
        try:
            post_id = post_link.split("/")
            if len(post_id) >= 2:
                channel_username_or_id = post_id[-2]
                message_id = int(post_id[-1])
            else:
                return await edit_or_reply(event, "**- رابـط غيـر صالـح ؟!**")
        except Exception as e:
            return await edit_or_reply(event, f"**- اووبـس .. حدث خطأ أثناء حفظ الرسالة\n- تفاصيل الخطأ :**\n {str(e)}\n\n**- استخـدم الامـر الآخـر لـ حفـظ الملفـات المقيـده 🔳:\n- ارسـل** ( .احفظ ) **+ رابـط او بالـرد ع رابـط مقيـد**")
    try:
        message = await zedub.get_messages(channel_username_or_id, ids=message_id)
        if not message:
            return await edit_or_reply(event, "**- رابـط غيـر صالـح ؟!**")
        if message.media:
            file_ext = ""
            if message.photo:
                file_ext = ".jpg"
            elif message.video:
                file_ext = ".mp4"
            elif message.document:
                if hasattr(message.document, "file_name"):
                    file_ext = os.path.splitext(message.document.file_name)[1]
            file_path = os.path.join(save_dir, f"media_{message.id}{file_ext}")
            await zedub.download_media(message, file=file_path)
            if message.text:
                ahmed = await zedub.send_file(event.chat_id, file=file_path, caption=f"{message.text}")
                await zedub.send_message(event.chat_id, f"ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝐋𝐈𝐓𝐇𝐎𝐍 - حـفـظ المـحتـوى 🧧\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎ تـم جلب المنشـور المقيـد .. بنجـاح ☑️** ❝\n**⌔╎رابـط المنشـور** {post_link} .", reply_to=ahmed)
                os.remove(file_path)
                await event.delete()
            else:
                await zedub.send_file(event.chat_id, file=file_path, caption=f"[ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝐋𝐈𝐓𝐇𝐎𝐍 - حـفـظ المـحتـوى 🧧](t.me/A1DIIU) .\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎ تـم جلب المنشـور المقيـد .. بنجـاح ☑️** ❝\n**⌔╎رابـط المنشـور** {post_link} .")
                os.remove(file_path)
                await event.delete()
        else:
            if message.text:
                ali = await zedub.send_message(event.chat_id, f"{message.text}")
                await zedub.send_message(event.chat_id, f"ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝐋𝐈𝐓𝐇𝐎𝐍 - حـفـظ المـحتـوى 🧧\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**⌔╎ تـم جلب المنشـور المقيـد .. بنجـاح ☑️** ❝\n**⌔╎رابـط المنشـور** {post_link} .", reply_to=ali)
                await event.delete()
            else:
                await edit_or_reply(event, "**- الرابط لا يحتوي على ميديا أو نص ؟!**")
    except Exception as e:
        return await edit_or_reply(event, f"**- اووبـس .. حدث خطأ أثناء حفظ الرسالة\n- تفاصيل الخطأ :**\n {str(e)}\n\n**- استخـدم الامـر الآخـر لـ حفـظ الملفـات المقيـده 🔳:\n- ارسـل** ( .احفظ ) **+ رابـط او بالـرد ع رابـط مقيـد**")

@zedub.zed_cmd(
    pattern="(الغاء محتوى|الغاء المحتوى)$",
    command=("الغاء المحتوى", plugin_category),
    info={
        "header": "إلغاء عملية حفظ الميديا.",
        "description": "يقوم بإلغاء العملية الجارية لحفظ الميديا من القنوات.",
        "usage": "{tr}الغاء المحتوى",
    },
)
async def save_posts(event):
    "إلغاء عملية حفظ الميديا."
    global cancel_process
    cancel_process = True
    await event.edit("**- تم إلغـاء عمليـة حفـظ الميـديا .. بنجـاح✅**")

@zedub.on(events.NewMessage(incoming=True))
async def check_cancel(event):
    global cancel_process
    if isinstance(event.message, MessageService) and event.message.action and isinstance(event.message.action, MessageActionChannelMigrateFrom):
        cancel_process = True

@zedub.zed_cmd(
    pattern="محتوى(?: |$)(.*) (\d+)",
    command=("محتوى", plugin_category),
    info={
        "header": "حفظ الميديا من القنوات ذات تقييد المحتوى.",
        "description": "يقوم بحفظ الميديا (الصور والفيديوهات والملفات) من القنوات ذات تقييد المحتوى.",
        "usage": "{tr}محتوى + يـوزر القنـاة + عـدد الميديـا (الحـد)",
    },
)
async def save_posts(event):
    "حفظ الميديا من القنوات ذات تقييد المحتوى."
    global cancel_process
    channel_username = event.pattern_match.group(1)
    limit = int(event.pattern_match.group(2))
    if not channel_username:
        return await event.edit("**- يرجـى إدخـال يـوزر القنـاة بعـد الامـر ؟!**\n**- مثــال :**\n**. محتوى + يـوزر القنـاة + عـدد الميديـا التي تريـد جلبهـا (الحـد)**")
    if channel_username.startswith("@"):
        channel_username = channel_username.replace("@", "")
    save_dir = "media"
    os.makedirs(save_dir, exist_ok=True)
    try:
        channel_entity = await zedub.get_entity(channel_username)
        messages = await zedub.get_messages(channel_entity, limit=limit)
    except Exception as e:
        return await event.edit(f"**- اووبـس .. حدث خطأ أثناء جلب الرسـائل مـن القنـاة**\n**- تفاصيـل الخطـأ:**\n{str(e)}")
    for message in messages:
        try:
            if message.media:
                file_ext = ""
                if message.photo:
                    file_ext = ".jpg"
                elif message.video:
                    file_ext = ".mp4"
                elif message.document:
                    if hasattr(message.document, "file_name"):
                        file_ext = os.path.splitext(message.document.file_name)[1]
                    else:
                        # Handle documents without file_name attribute
                        file_ext = ""
                if not file_ext:
                    continue
                file_path = os.path.join(save_dir, f"media_{message.id}{file_ext}")
                await message.download_media(file=file_path)
                await zedub.send_file("me", file=file_path)
                os.remove(file_path)
            if cancel_process:
                await event.edit("**- تم إلغـاء عمليـة حفـظ الميـديا .. بنجـاح✅**")
                cancel_process = False
                return
        except Exception as e:
            print(f"حدث خطأ أثناء حفظ الرسالة {message.id}. الخطأ: {str(e)}")
            continue
    await event.edit(f"تم حفظ الميديا من القناة {channel_username} بنجاح.")

#A1DIIU 
@zedub.zed_cmd(pattern="متحركات ?(.*)")
async def gifs(ult):
    get = ult.pattern_match.group(1)
    xx = random.randint(0, 5)
    n = 0
    if not get:
        return await edit_or_reply(ult, "**-ارسـل** `.متحركات` **+ نـص لـ البحـث**\n**- او** `.متحركات عدد` **+ العـدد**")
    if "عدد" in get:
        try:
            n = int(get.split("عدد")[-1])
        except BaseException:
            pass
    m = await edit_or_reply(ult, "**╮ جـارِ ﮼ البحـث ؏ الـمتحـركھہ 𓅫🎆╰**")
    gifs = await ult.client.inline_query("gif", get)
    if not n:
        await gifs[xx].click(
            ult.chat.id, reply_to=ult.reply_to_msg_id, silent=True, hide_via=True
        )
    else:
        for x in range(n):
            await gifs[x].click(
                ult.chat.id, reply_to=ult.reply_to_msg_id, silent=True, hide_via=True
            )
    await m.delete()

@zedub.zed_cmd(
    pattern="متحركاات(?:\s|$)([\s\S]*)",
    command=("متحركاات", plugin_category),
    info={
        "header": "Sends random gifs",
        "usage": "Search and send your desire gif randomly and in bulk",
        "examples": [
            "{tr}gifs cat",
            "{tr}gifs cat ; <1-20>",
        ],
    },
)
async def some(event):
    """Sends random gifs of your query"""
    inpt = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if not inpt:
        return await edit_or_reply(event, "**-ارسـل** `.متحركات` **+ نـص لـ البحـث**\n**- او** `.متحركات عدد` **+ العـدد**")
    count = 1
    if "عدد" in inpt:
        inpt, count = inpt.split("عدد")
    if int(count) < 0 and int(count) > 20:
        await edit_delete(event, "`Give value in range 1-20`")
    zedevent = await edit_or_reply(event, "**╮ جـارِ ﮼ البحـث ؏ الـمتحـركھہ 𓅫🎆╰**")
    res = requests.get("https://giphy.com/")
    res = res.text.split("GIPHY_FE_WEB_API_KEY =")[1].split("\n")[0]
    api_key = res[2:-1]
    r = requests.get(
        f"https://api.giphy.com/v1/gifs/search?q={inpt}&api_key={api_key}&limit=50"
    ).json()
    list_id = [r["data"][i]["id"] for i in range(len(r["data"]))]
    rlist = random.sample(list_id, int(count))
    for items in rlist:
        nood = await event.client.send_file(
            event.chat_id,
            f"https://media.giphy.com/media/{items}/giphy.gif",
            reply_to=reply_to_id,
        )
        await _zedutils.unsavegif(event, nood)
    await zedevent.delete()

#Code by T.me/S_1_02
@zedub.zed_cmd(pattern="(لمتحركه|لمتحركة|متحركه|متحركة)$")
async def zelzal_gif(event):
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**╮ بالـرد ﮼؏ فيديـو للتحـويـل لمتحركـه ...𓅫╰**\n\n**-لـ البحث عن متحركـات :**\n**-ارسـل** `.متحركه` **+ نـص لـ البحـث**\n**- او** `.متحركه عدد` **+ العـدد**")
    chat = "@VideoToGifConverterBot" #Code by T.me/S_1_02
    zed = await edit_or_reply(event, "**╮ جـارِ تحويـل الفيديـو لـ متحركـه ...𓅫╰**")
    async with borg.conversation(chat) as conv: #Code by T.me/S_1_02
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_file(reply_message) #Code by T.me/S_1_02
            await conv.get_response()
            await asyncio.sleep(5)
            zedthon = await conv.get_response()
            await zed.delete()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=f"<b>⎉╎تم التحويل لمتحركه .. بنجاح 🎆</b>",
                parse_mode="html",
                reply_to=reply_message,
            )
            await zed.delete()
            await asyncio.sleep(3)
            await event.client(DeleteHistoryRequest(1125181695, max_id=0, just_clear=True))
        except YouBlockedUserError: #Code by T.me/S_1_02
            await zedub(unblock("VideoToGifConverterBot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_file(reply_message)
            await conv.get_response()
            await asyncio.sleep(5)
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=f"<b>⎉╎تم التحويل لمتحركه .. بنجاح 🎆</b>",
                parse_mode="html",
                reply_to=reply_message,
            )
            await zed.delete()
            await asyncio.sleep(3)
            await event.client(DeleteHistoryRequest(1125181695, max_id=0, just_clear=True))

#Code by T.me/S_1_02
@zedub.zed_cmd(pattern="(معالجه|تنقيه|تحسين|توضيح)$")
async def zelzal_ai(event):
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**- بالـرد ع صـوره .. لمعالجتهـا**")
    chat = "@PhotoFixerBot" #Code by T.me/S_1_02
    zzz = await edit_or_reply(event, "**- جـارِ معالجـة الصـورة بالذكـاء الاصطناعـي ...💡╰**\n**- الرجاء الانتظار دقيقـه كاملـه لـ التحسيـن ..... 🍧╰**")
    async with borg.conversation(chat) as conv: #Code by T.me/S_1_02
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message) #Code by T.me/S_1_02
        except YouBlockedUserError:
            await zedub(unblock("PhotoFixerBot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message) #Code by T.me/S_1_02
        await conv.get_response()
        await asyncio.sleep(3)
        zedthon1 = await conv.get_response()
        await borg.send_file(
            event.chat_id,
            zedthon1,
            caption=f"<b>⎉╎تم معالجـة الصـورة .. بنجـاح 🎆</b>",
            parse_mode="html",
            reply_to=reply_message,
        )
        await zzz.delete()
        await delete_conv(event, chat, purgeflag)
        await event.client(DeleteHistoryRequest(6314982389, max_id=0, just_clear=True))

#Code by T.me/S_1_02
@zedub.zed_cmd(pattern=f"s(?: |$)(.*)")
async def zelzal_ss(event):
    malath = event.pattern_match.group(1)
    if malath: #Write Code By T.me/S_1_02
        zelzal = malath
    elif event.is_reply:
        zelzal = await event.get_reply_message()
    else:
        return await edit_or_reply(event, "**⎉╎باضافة رابـط ستـوري لـ الامـر او بالـࢪد ؏ــلى رابـط الستـوري**")
    chat_url = "https://t.me/msaver_bot?start=1895219306"
    zzz = await edit_or_reply(event, f"**- جـارِ تحميـل الستـوري انتظـر ... 🍧╰\n- رابـط الستـوري :\n{zelzal.message}**")
    chat = "@msaver_bot"
    async with borg.conversation(chat) as conv: #Code by T.me/S_1_02
        try:
            purgeflag = await conv.send_message(zelzal)
        except YouBlockedUserError: #Code by T.me/S_1_02
            await zedub(unblock("msaver_bot"))
            purgeflag = await conv.send_message(zelzal)
        response = await conv.get_response()
        await asyncio.sleep(3)
        if response.media:
            zedthon1 = response.media
        else:
            zedthon1 = await conv.get_response()
        await borg.send_file(
            event.chat_id,
            zedthon1,
            caption=f"<b>⎉╎تم تحميـل الستـوري .. بنجـاح 🎆\n⎉╎الرابـط 🖇:  {zelzal.message}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>",
            parse_mode="html",
        )
        await zzz.delete()
        await delete_conv(event, chat, purgeflag)
        await event.client(DeleteHistoryRequest(6135950112, max_id=0, just_clear=True))

#Code by T.me/S_1_02
@zedub.zed_cmd(pattern="(انمي|كارتون)$")
async def zelzal_anime(event):
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**- بالـرد ع صـوره .. لتحويلهـا لـ انمـي**")
    chat = "@qq_neural_anime_bot" #Code by T.me/S_1_02
    zzz = await edit_or_reply(event, "**- جـارِ تحويـل الصـورة لـ انمـي (كارتـون) ...💡╰**\n**- الرجاء الانتظار دقيقـه كاملـه ..... 🍧╰**")
    async with borg.conversation(chat) as conv: #Code by T.me/S_1_02
        try:
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message) #Code by T.me/S_1_02
        except YouBlockedUserError:
            await zedub(unblock("qq_neural_anime_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message) #Code by T.me/S_1_02
        await conv.get_response()
        await asyncio.sleep(5)
        zedthon1 = await conv.get_response()
        await borg.send_file(
            event.chat_id,
            zedthon1,
            caption=f"<b>⎉╎تم تحويـل الصـورة .. بنجـاح 🍧🎆</b>",
            parse_mode="html",
            reply_to=reply_message,
        )
        await zzz.delete()
        await delete_conv(event, chat, purgeflag)
        await event.client(DeleteHistoryRequest(5894660331, max_id=0, just_clear=True))

#Code by T.me/S_1_02
@zedub.zed_cmd(pattern="سكانر$")
async def zelzal_scanner(event):
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**- بالـرد ع صـوره .. لاستخـراج النـص**")
    chat = "@BruhulBot" #Code by T.me/S_1_02
    zzz = await edit_or_reply(event, "**- جـارِ استخـراج النـص من الصـورة ...💡╰\n- يجب ان تكـون الصـورة بدقـه واضحـه ... 🎟╰\n- الرجاء الانتظار دقيقـه كاملـه ..... 🍧╰**")
    async with borg.conversation(chat) as conv: #Code by T.me/S_1_02
        try:
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message)
            await conv.send_message("/ocr", reply_to=purgeflag)  # إرسال /ocr بالرد على الصورة داخل البوت
        except YouBlockedUserError: #Code by T.me/S_1_02
            await zedub(unblock("BruhulBot"))
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message)
            await conv.send_message("/ocr", reply_to=purgeflag)  # إرسال /ocr بالرد على الصورة داخل البوت
        zedthon1 = await conv.get_response()
        replay_z = await borg.send_message(event.chat_id, zedthon1, reply_to=reply_message)
        await borg.send_message(event.chat_id, "**⎉╎تم استخـراج النـص من الصـورة .. بنجـاح 🍧🎆\n⎉╎بواسطـة @A1DIIU**", reply_to=replay_z)
        await zzz.delete()
        await asyncio.sleep(2)
        await event.client(DeleteHistoryRequest(1719108336, max_id=0, just_clear=True))

#Code by T.me/S_1_02
@zedub.zed_cmd(pattern="ازاله$")
async def zelzal_rr(event):
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**- بالـرد ع صـوره .. لـ ازالـة الخلفيـة**")
    chat = "@bgkillerbot" #Code by T.me/S_1_02
    zzz = await edit_or_reply(event, "**- جـارِ ازالـة الخلفيـة مـن الصـورة ...💡╰**\n**- الرجاء الانتظار دقيقـه كاملـه ..... 🍧╰**")
    async with borg.conversation(chat) as conv: #Code by T.me/S_1_02
        try:
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message) #Code by T.me/S_1_02
        except YouBlockedUserError: #Code by T.me/S_1_02
            await zedub(unblock("bgkillerbot"))
            await conv.send_message("/start")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message) #Code by T.me/S_1_02
        await conv.get_response()
        await asyncio.sleep(3)
        zedthon1 = await conv.get_response()
        if zedthon1.file:
            await borg.send_file(
                event.chat_id,
                zedthon1,
                caption=f"<b>⎉╎تم ازالـة الخلفيـة من الصـورة .. بنجـاح 🍧🎆\n⎉╎بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>",
                parse_mode="html",
                reply_to=reply_message,
            )
        else:
            zedthon1 = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon1,
                caption=f"<b>⎉╎تم ازالـة الخلفيـة من الصـورة .. بنجـاح 🍧🎆\n⎉╎بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>",
                parse_mode="html",
                reply_to=reply_message,
            )
        await zzz.delete()
        await delete_conv(event, chat, purgeflag)
        await event.client(DeleteHistoryRequest(1744388227, max_id=0, just_clear=True))

#Code by T.me/S_1_02
@zedub.on(events.NewMessage(outgoing=True, pattern='.موقع (.*)'))
async def _(event): #Code by T.me/S_1_02
    con = event.pattern_match.group(1) 
    sender = await event.get_sender()
    if sender.id != zedub.uid: #Code by T.me/S_1_02
        return
    if Zel_Uid not in Zed_Vip:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @S_1_02\n⎉╎او التواصـل مـع احـد المشرفيـن @S_1_02**")
    zzz = await event.edit("**⎉╎جـارِ البحث في خرائـط جـوجـل ...**")
    channel_entity = await zedub.get_entity(gpsbb)
    await zedub.send_message(gpsbb, '/start')
    await asyncio.sleep(0.5)
    msg0 = await zedub.get_messages(gpsbb, limit=1)
    await zedub.send_message(gpsbb, con)
    await asyncio.sleep(0.5)
    try:
        msg1 = await zedub.get_messages(gpsbb, limit=1)
        await msg1[0].click(2)
    except:
        await event.client(DeleteHistoryRequest(364791564, max_id=0, just_clear=True))
        return await zzz.edit("**⎉╎لم يتم العثـور ع الموقـع ...؟!**\n**⎉╎قم بادخـال الموقـع بشكـل صحيـح**")
    await asyncio.sleep(0.5)
    msg2 = await zedub.get_messages(gpsbb, limit=1)
    await msg2[0].click(2)
    await asyncio.sleep(0.5)
    msg3 = await zedub.get_messages(gpsbb, limit=1)
    await msg3[0].click(2)
    await asyncio.sleep(0.5)
    msg4 = await zedub.get_messages(gpsbb, limit=1)
    await zedub.send_file(
        event.chat_id,
        msg4[0],
        caption=f"<b>⎉╎تم جلب المـوقـع .. بنجـاح \n⎉╎</b><code>{con}</code>  🗺 \n<b>⎉╎بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>",
        parse_mode="html",
    )
    await msg4[0].click(3)
    await asyncio.sleep(0.5)
    msg5 = await zedub.get_messages(gpsbb, limit=1)
    await zedub.send_file(
        event.chat_id,
        msg5[0],
        caption=f"<b>⎉╎تم الجلب عبـر الاقمـار الصناعيـه .. بنجـاح 🛰\n⎉╎</b><code>{con}</code>  🗺 \n<b>⎉╎بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>",
        parse_mode="html",
    )
    await zzz.delete()
    await asyncio.sleep(2)
    await event.client(DeleteHistoryRequest(364791564, max_id=0, just_clear=True))

# Write code by T.me/S_1_02
@zedub.zed_cmd(pattern="(عدسه|عدسة)$")
async def _(event): # Write code by T.me/S_1_02
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**- بالـرد ع صـوره/ملصق/فيديـو ...\n- لـ البحث فـي عدسـة جـوجـل**")
    zellzall = '@reverse_image_search_bot' # Write code by T.me/S_1_02)
    channel_entity = await zedub.get_entity(zellzall)
    zzz = await event.edit("**⎉╎جـارِ البحث في عدسـة جـوجـل ...🔍**")
    channel_entity = await zedub.get_entity(zellzall)
    await zedub.send_message(zellzall, '/start')
    await asyncio.sleep(2)
    msga = await zedub.get_messages(zellzall, limit=1)
    await zedub.send_file(zellzall, reply_message)
    await asyncio.sleep(2)
    msg1 = await zedub.get_messages(zellzall, limit=1)
    msg2 = await zedub.get_messages(zellzall, limit=1)
    await asyncio.sleep(3)
    try: # Write code by T.me/S_1_02
        list = await zedub(GetHistoryRequest(peer=channel_entity, limit=1, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
        msgs = list.messages[0]
        url_pic = msgs.reply_markup.rows[1].buttons[0].url
        url_snao = msgs.reply_markup.rows[2].buttons[0].url
        url_google = msgs.reply_markup.rows[2].buttons[1].url
        url_trace = msgs.reply_markup.rows[3].buttons[0].url
        url_iqdb = msgs.reply_markup.rows[3].buttons[1].url
        url_3d = msgs.reply_markup.rows[4].buttons[0].url
        url_yandex = msgs.reply_markup.rows[4].buttons[1].url
        url_baidu = msgs.reply_markup.rows[5].buttons[0].url
        url_bing = msgs.reply_markup.rows[5].buttons[1].url
        url_tineye = msgs.reply_markup.rows[6].buttons[0].url
        url_sogou = msgs.reply_markup.rows[6].buttons[1].url
        url_ascii2d = msgs.reply_markup.rows[7].buttons[0].url
        await asyncio.sleep(0.5)
        await zedub.send_file(
            event.chat_id,
            url_pic,
            caption=f"<b>⎉╎تم البحث عبـر عدسـة جـوجـل .. بنجـاح ☑️\n⎉╎بواسطـة سـورس <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a>\n⎉╎اليـك روابـط بنتائـج البحث لـ عـدة محركـات بحث :</b>\n\n<b><a href = {url_pic}>- رابــط الصــورة</a> 🖇\n\n<a href = {url_google}>- عدسـة جوجـل Google</a> 🌐\n\n<a href = {url_yandex}>- ياندكس Yandex</a> 〽️\n\n<a href = {url_bing}>- بينـج Bing</a> 🅿️\n\n<a href = {url_baidu}>- بايـدو Baidu</a> 🛜\n\n<a href = {url_snao}>- سوسـناو SauceNAO</a> 🈯️\n\n<a href = {url_sogou}>- سوجـو Sogou</a> ❇️\n\n<a href = {url_tineye}>- تينـآي TinEye</a> 🚺\n\n<a href = {url_trace}>- تـراك Trace</a> 🚼\n\n<a href = {url_iqdb}>- آي كيو ديبي IQDB</a> 🚾\n\n<a href = {url_3d}>- ثـري دي ديبي 3D IQDB</a> Ⓜ️\n\n<a href = {url_ascii2d}>- آسكـي Ascii2d</a> 🔡</b>",
            parse_mode="html",
            reply_to=reply_message,
        )
        await zzz.delete()
        await event.client(DeleteHistoryRequest(812573486, max_id=0, just_clear=True))
    except: # Write code by T.me/S_1_02
        try:
            list = await zedub(GetHistoryRequest(peer=channel_entity, limit=2, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
            msgs = list.messages[1]
            url_pic = msgs.reply_markup.rows[1].buttons[0].url
            url_snao = msgs.reply_markup.rows[2].buttons[0].url
            url_google = msgs.reply_markup.rows[2].buttons[1].url
            url_trace = msgs.reply_markup.rows[3].buttons[0].url
            url_iqdb = msgs.reply_markup.rows[3].buttons[1].url
            url_3d = msgs.reply_markup.rows[4].buttons[0].url
            url_yandex = msgs.reply_markup.rows[4].buttons[1].url
            url_baidu = msgs.reply_markup.rows[5].buttons[0].url
            url_bing = msgs.reply_markup.rows[5].buttons[1].url
            url_tineye = msgs.reply_markup.rows[6].buttons[0].url
            url_sogou = msgs.reply_markup.rows[6].buttons[1].url
            url_ascii2d = msgs.reply_markup.rows[7].buttons[0].url
            await asyncio.sleep(0.5)
            await zedub.send_file(
                event.chat_id,
                url_pic,
                caption=f"<b>⎉╎تم البحث عبـر عدسـة جـوجـل .. بنجـاح ☑️\n⎉╎بواسطـة سـورس <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a>\n⎉╎اليـك روابـط بنتائـج البحث لـ عـدة محركـات بحث :</b>\n\n<b><a href = {url_pic}>- رابــط الصــورة</a> 🖇\n\n<a href = {url_google}>- عدسـة جوجـل Google</a> 🌐\n\n<a href = {url_yandex}>- ياندكس Yandex</a> 〽️\n\n<a href = {url_bing}>- بينـج Bing</a> 🅿️\n\n<a href = {url_baidu}>- بايـدو Baidu</a> 🛜\n\n<a href = {url_snao}>- سوسـناو SauceNAO</a> 🈯️\n\n<a href = {url_sogou}>- سوجـو Sogou</a> ❇️\n\n<a href = {url_tineye}>- تينـآي TinEye</a> 🚺\n\n<a href = {url_trace}>- تـراك Trace</a> 🚼\n\n<a href = {url_iqdb}>- آي كيو ديبي IQDB</a> 🚾\n\n<a href = {url_3d}>- ثـري دي ديبي 3D IQDB</a> Ⓜ️\n\n<a href = {url_ascii2d}>- آسكـي Ascii2d</a> 🔡</b>",
                parse_mode="html",
                reply_to=reply_message,
            )
            await zzz.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(812573486, max_id=0, just_clear=True))
        except: # Write code by T.me/S_1_02
            list = await zedub(GetHistoryRequest(peer=channel_entity, limit=3, offset_date=None, offset_id=0, max_id=0, min_id=0, add_offset=0, hash=0))
            msgs = list.messages[2]
            url_pic = msgs.reply_markup.rows[1].buttons[0].url
            url_snao = msgs.reply_markup.rows[2].buttons[0].url
            url_google = msgs.reply_markup.rows[2].buttons[1].url
            url_trace = msgs.reply_markup.rows[3].buttons[0].url
            url_iqdb = msgs.reply_markup.rows[3].buttons[1].url
            url_3d = msgs.reply_markup.rows[4].buttons[0].url
            url_yandex = msgs.reply_markup.rows[4].buttons[1].url
            url_baidu = msgs.reply_markup.rows[5].buttons[0].url
            url_bing = msgs.reply_markup.rows[5].buttons[1].url
            url_tineye = msgs.reply_markup.rows[6].buttons[0].url
            url_sogou = msgs.reply_markup.rows[6].buttons[1].url
            url_ascii2d = msgs.reply_markup.rows[7].buttons[0].url
            await asyncio.sleep(0.5)
            await zedub.send_file(
                event.chat_id,
                url_pic,
                caption=f"<b>⎉╎تم البحث عبـر عدسـة جـوجـل .. بنجـاح ☑️\n⎉╎بواسطـة سـورس <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a>\n⎉╎اليـك روابـط بنتائـج البحث لـ عـدة محركـات بحث :</b>\n\n<b><a href = {url_pic}>- رابــط الصــورة</a> 🖇\n\n<a href = {url_google}>- عدسـة جوجـل Google</a> 🌐\n\n<a href = {url_yandex}>- ياندكس Yandex</a> 〽️\n\n<a href = {url_bing}>- بينـج Bing</a> 🅿️\n\n<a href = {url_baidu}>- بايـدو Baidu</a> 🛜\n\n<a href = {url_snao}>- سوسـناو SauceNAO</a> 🈯️\n\n<a href = {url_sogou}>- سوجـو Sogou</a> ❇️\n\n<a href = {url_tineye}>- تينـآي TinEye</a> 🚺\n\n<a href = {url_trace}>- تـراك Trace</a> 🚼\n\n<a href = {url_iqdb}>- آي كيو ديبي IQDB</a> 🚾\n\n<a href = {url_3d}>- ثـري دي ديبي 3D IQDB</a> Ⓜ️\n\n<a href = {url_ascii2d}>- آسكـي Ascii2d</a> 🔡</b>",
                parse_mode="html",
                reply_to=reply_message,
            )
            await zzz.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(812573486, max_id=0, just_clear=True))

#Code by T.me/S_1_02
@zedub.zed_cmd(pattern="انستا(?: |$)([\s\S]*)")
async def zelzal_insta(event): #Code by T.me/S_1_02
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not link and reply: #Code by T.me/S_1_02
        link = reply.text
    if not link: #Code by T.me/S_1_02
        return await edit_delete(event, "**- ارسـل (.انستا) + رابـط او بالـرد ع رابـط**", 10)
    if "instagram.com" not in link:
        return await edit_delete(event, "**- احتـاج الـى رابــط من الانستـا .. للتحميــل ؟!**", 10)
    if link.startswith("https://instagram"):
        link = link.replace("https://instagram", "https://www.instagram")
    if link.startswith("http://instagram"):
        link = link.replace("http://instagram", "http://www.instagram")
    if "/reel/" in link: #Code by T.me/S_1_02
        cap_zzz = f"<b>⎉╎تم تحميـل مقطـع انستـا (ريلـز) .. بنجـاح ☑️\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>"
    elif "/tv/" in link: #Code by T.me/S_1_02
        cap_zzz = f"<b>⎉╎تم تحميـل بث انستـا (Tv) .. بنجـاح ☑️\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>"
    elif "/stories/" in link: #Code by T.me/S_1_02
        cap_zzz = f"<b>⎉╎تم تحميـل ستـوري انستـا .. بنجـاح ☑️\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>"
    else: #Code by T.me/S_1_02
        cap_zzz = f"<b>⎉╎تم تحميـل مقطـع انستـا .. بنجـاح ☑️\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>"
    chat = "@story_repost_bot" #Code by T.me/S_1_02
    zed = await edit_or_reply(event, "**⎉╎جـارِ التحميل من الانستـا .. انتظر قليلا ▬▭**")
    async with borg.conversation(chat) as conv: #Code by T.me/S_1_02
        try: #Code by T.me/S_1_02
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link) #Code by T.me/S_1_02
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(2036153627, max_id=0, just_clear=True))
        except YouBlockedUserError: #Code by T.me/S_1_02
            await zedub(unblock("story_repost_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link) #Code by T.me/S_1_02
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(2036153627, max_id=0, just_clear=True))

#Code by T.me/S_1_02
@zedub.zed_cmd(pattern="فيس(?: |$)([\s\S]*)")
async def zelzal_insta(event): #Code by T.me/S_1_02
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not link and reply: #Code by T.me/S_1_02
        link = reply.text
    if not link: #Code by T.me/S_1_02
        return await edit_delete(event, "**- ارسـل (.فيس) + رابـط او بالـرد ع رابـط**", 10)
    if "share/r" in link:
        return await edit_delete(event, "**- قم باستخـدام الامـر (.تيك + الرابط) لتحميل هذا النـوع من الفيديوهـات**", 10)
    if ("https://fb" not in link) and ("facebook.com" not in link):
        return await edit_delete(event, "**- احتـاج الـى رابــط من فيـس بـوك .. للتحميــل ؟!**", 10)
    if link.startswith("https://fb.watch"):
        link = link.replace("https://fb.watch", "https://www.facebook.com/watch")
    if link.startswith("http://fb.watch"):
        link = link.replace("http://fb.watch", "http://www.facebook.com/watch")
    cap_zzz = f"<b>⎉╎تم تحميـل مـن فيـس بـوك .. بنجـاح ☑️\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>"
    chat = "@FBDLBOT" #Code by T.me/S_1_02
    zed = await edit_or_reply(event, "**⎉╎جـارِ التحميل من فيـس بـوك .. انتظر قليلا ▬▭**")
    async with borg.conversation(chat) as conv: #Code by T.me/S_1_02
        try: #Code by T.me/S_1_02
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link) #Code by T.me/S_1_02
            await conv.get_response()
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(6361899360, max_id=0, just_clear=True))
        except YouBlockedUserError: #Code by T.me/S_1_02
            await zedub(unblock("FBDLBOT"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(link) #Code by T.me/S_1_02
            await conv.get_response()
            zedthon = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=cap_zzz,
                parse_mode="html",
            )
            await zed.delete()
            await asyncio.sleep(2)
            await event.client(DeleteHistoryRequest(6361899360, max_id=0, just_clear=True))

#Code by T.me/S_1_02
@zedub.zed_cmd(pattern="(النص|لنص)$")
async def zelzal_ai(event):
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**- بالـرد ع بصمـه (تسجيـل صـوتـي) .. لـ استخـراج النـص منهـا**")
    chat = "@Speechpro_ASR_bot" #Code by T.me/S_1_02
    zzz = await edit_or_reply(event, "**- جـارِ إستخـراج النـص مـن الصـوت . . .🎙╰\n- الرجـاء الانتظـار دقيـقـه . . .⏳╰**")
    async with borg.conversation(chat) as conv: #Code by T.me/S_1_02
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.get_response()
            await conv.send_message("/lang ara")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message) #Code by T.me/S_1_02
        except YouBlockedUserError:
            await zedub(unblock("Speechpro_ASR_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.get_response()
            await conv.send_message("/lang ara")
            await conv.get_response()
            purgeflag = await conv.send_file(reply_message) #Code by T.me/S_1_02
        zm = await conv.get_response()
        ztxt = zm.message
        await borg.send_message(
            event.chat_id,
            f"<b>{ztxt}\n\n<a href = https://t.me/A1DIIU/1>𓆩 𝐋𝐈𝐓𝐇𝐎𝐍 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𓆪</a> </b>",
            parse_mode="html",
            reply_to=reply_message,
        )
        await zzz.delete()
        await delete_conv(event, chat, purgeflag)
        await event.client(DeleteHistoryRequest(916427203, max_id=0, just_clear=True))

# Code by T.me/S_1_02
@zedub.zed_cmd(pattern="كتاب(?: |$)(.*)")
async def zelzal_gif(event):
    zelzal = str(event.pattern_match.group(1))
    if not zelzal:
        return await edit_or_reply(event, "**- ارسـل (.كتاب) + اسـم الكتـاب ...**")
    chat = "@GoogleBooksSearchBot" # Code by T.me/S_1_02
    zed = await edit_or_reply(event, "**⎉╎جـارِ البحث عن الكتـاب المحـدد ...**")
    async with borg.conversation(chat) as conv: # Code by T.me/S_1_02
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(zelzal)
        except YouBlockedUserError:
            await zedub(unblock("GoogleBooksSearchBot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(zelzal)
        try:
            zedthon1 = await conv.get_response()
            malath1 = zedthon1.text
            if "Find books with" in malath1: # Code by T.me/S_1_02
                zz1 = malath1.replace("Find books with @GoogleBooksSearchBot", "📕\n<b>- تم التحميـل بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>") 
                await zed.delete()
                await borg.send_file(
                    event.chat_id,
                    zedthon1,
                    caption=zz1,
                    parse_mode="html",
                )
        except:
            await zed.delete()
            await event.client(DeleteHistoryRequest(1986854339, max_id=0, just_clear=True))
        try:
            zedthon2 = await conv.get_response()
            malath2 = zedthon2.text
            if "Find books with" in malath2: # Code by T.me/S_1_02
                zz2 = malath2.replace("Find books with @GoogleBooksSearchBot", "📗\n<b>- تم التحميـل بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>") 
                await borg.send_file(
                    event.chat_id,
                    zedthon2,
                    caption=zz2,
                    parse_mode="html",
                )
        except:
            await zed.delete()
            await event.client(DeleteHistoryRequest(1986854339, max_id=0, just_clear=True))
        try:
            zedthon3 = await conv.get_response()
            malath3 = zedthon3.text
            if "Find books with" in malath3: # Code by T.me/S_1_02
                zz3 = malath3.replace("Find books with @GoogleBooksSearchBot", "📘\n<b>- تم التحميـل بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>") 
                await borg.send_file(
                    event.chat_id,
                    zedthon3,
                    caption=zz3,
                    parse_mode="html",
                )
        except:
            await zed.delete()
            await event.client(DeleteHistoryRequest(1986854339, max_id=0, just_clear=True))
        try:
            zedthon4 = await conv.get_response()
            malath4 = zedthon4.text
            if "Find books with" in malath4: # Code by T.me/S_1_02
                zz4 = malath3.replace("Find books with @GoogleBooksSearchBot", "📙\n<b>- تم التحميـل بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>") 
                await borg.send_file(
                    event.chat_id,
                    zedthon4,
                    caption=zz4,
                    parse_mode="html",
                )
        except:
            await zed.delete()
            await event.client(DeleteHistoryRequest(1986854339, max_id=0, just_clear=True))
        try:
            zedthon5 = await conv.get_response()
            malath5 = zedthon5.text
            if "Find books with" in malath5: # Code by T.me/S_1_02
                zz5 = malath5.replace("Find books with @GoogleBooksSearchBot", "📚\n<b>- تم التحميـل بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>") 
                await borg.send_file(
                    event.chat_id,
                    zedthon5,
                    caption=zz5,
                    parse_mode="html",
                )
        except:
            await zed.delete()
            await event.client(DeleteHistoryRequest(1986854339, max_id=0, just_clear=True))
        try:
            zedthon6 = await conv.get_response()
            malath6 = zedthon6.text
            if "Find books with" in malath6: # Code by T.me/S_1_02
                zz6 = malath6.replace("Find books with @GoogleBooksSearchBot", "📖\n<b>- تم التحميـل بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>") 
                await borg.send_file(
                    event.chat_id,
                    zedthon6,
                    caption=zz6,
                    parse_mode="html",
                )
        except:
            await zed.delete()
            await event.client(DeleteHistoryRequest(1986854339, max_id=0, just_clear=True))
        try:
            zedthon7 = await conv.get_response()
            malath7 = zedthon7.text
            if "Find books with" in malath7: # Code by T.me/S_1_02
                zz7 = malath7.replace("Find books with @GoogleBooksSearchBot", "📔\n<b>- تم التحميـل بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>") 
                await borg.send_file(
                    event.chat_id,
                    zedthon7,
                    caption=zz7,
                    parse_mode="html",
                )
        except:
            await zed.delete()
            await event.client(DeleteHistoryRequest(1986854339, max_id=0, just_clear=True))
        try:
            zedthon8 = await conv.get_response()
            malath8 = zedthon8.text
            if "Find books with" in malath8: # Code by T.me/S_1_02
                zz8 = malath8.replace("Find books with @GoogleBooksSearchBot", "📒\n<b>- تم التحميـل بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>") 
                await borg.send_file(
                    event.chat_id,
                    zedthon8,
                    caption=zz8,
                    parse_mode="html",
                )
        except:
            await zed.delete()
            await event.client(DeleteHistoryRequest(1986854339, max_id=0, just_clear=True))

# Code by T.me/S_1_02
@zedub.zed_cmd(pattern=f"ستوريات(?: |$)(.*)")
async def zelzal_ai(event):
    malath = event.pattern_match.group(1)
    if Zel_Uid not in Zed_Vip:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @S_1_02\n⎉╎او التواصـل مـع احـد المشرفيـن @S_1_02**")
    if malath: #Write Code By T.me/S_1_02
        zelzal = malath
    elif event.is_reply:
        zelzal = await event.get_reply_message()
    else:
        return await edit_or_reply(event, "**⎉╎باضافة يـوزر الشخـص لـ الامـر**")
    zzz = await event.edit("**⎉╎جـارِ تحميـل ستـوريـات الشخـص ...**")
    channel_entity = await zedub.get_entity(storyz)
    await zedub.send_message(storyz, '/start')
    await asyncio.sleep(0.5)
    await zedub.get_messages(storyz, limit=1)
    await zedub.send_message(storyz, f"/dlStories {zelzal}")
    await asyncio.sleep(2)
    await zedub.get_messages(storyz, limit=1)
    messages = await zedub.get_messages(storyz, limit=None)
    await asyncio.sleep(0.5)
    for message in messages:
        if "- ID" in message.text:
            entities = message.entities
            mentions = [entity for entity in entities if isinstance(entity, (types.MessageEntityTextUrl, types.MessageEntityUrl))]
            if mentions:
                for mention in mentions:
                    urs = str(mention)
                    urls = extractor.find_urls(urs)
                    for url in urls:
                        try:
                            await zedub.send_file(
                                event.chat_id,
                                url,
                                caption=f"**⎉╎تم جلب الستـوري .. بنجـاح ☑️\n⎉╎من الحسـاب {zelzal}\n⎉╎بواسطـة 𝐋𝐈𝐓𝐇𝐎𝐍**",
                            )
                            await asyncio.sleep(2)
                        except:
                            pass
        else:
            return await zzz.edit("**⎉╎تعـذر العثـور ع الستـوري ...؟!**\n**⎉╎حـال مجـدداً وقت لاحـق**")

@zedub.zed_cmd(pattern="قط$")
async def zelzal_ss(event):
    zzz = await edit_or_reply(event, "** 🐈 . . .**")
    cat_url = get_random_cat()
    await zzz.delete()
    await bot.send_file(
        event.chat_id,
        cat_url,
        caption=f"<b>⎉╎صـورة قـط عشـوائـي .. 🐈 🎆\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>",
        parse_mode="html",
    )

# code by t.me/S_1_02
@zedub.zed_cmd(pattern="زد(?: |$)(.*)")
async def zelzal_gpt(event):
    question = event.pattern_match.group(1)
    zzz = await event.get_reply_message()
    if not question and not event.reply_to_msg_id:
        return await edit_or_reply(event, "**⎉╎بالـرد ع سـؤال او باضـافة السـؤال للامـر**\n**⎉╎مثـــال :**\n`.زد من هو مكتشف الجاذبية الارضية`")
    if not question and event.reply_to_msg_id and zzz.text: #code by t.me/S_1_02
        question = zzz.text
    if not event.reply_to_msg_id: #code by t.me/S_1_02
        question = event.pattern_match.group(1)
    zed = await edit_or_reply(event, "**⎉╎جـارِ الاتصـال بـ الذكـاء الاصطناعي\n⎉╎الرجـاء الانتظـار .. لحظـات**")
    answer = get_chatgpt_response(question)
    await zed.edit(f"[ᯓ 𝐋𝐈𝐓𝐇𝐎𝐍 𝗖𝗵𝗮𝘁𝗚𝗽𝘁 -💡-](t.me/A1DIIU) **الذكاء الاصطناعي\n⋆──┄─┄─┄───┄─┄─┄──⋆**\n**• س/ {question}\n\n• {answer}**", link_preview=False)

# code by t.me/S_1_02
@zedub.zed_cmd(pattern="س(?: |$)(.*)")
async def zelzal_gpt(event):
    question = event.pattern_match.group(1)
    zzz = await event.get_reply_message()
    if not question and not event.reply_to_msg_id:
        return await edit_or_reply(event, "**⎉╎بالـرد ع سـؤال او باضـافة السـؤال للامـر**\n**⎉╎مثـــال :**\n`.زد من هو مكتشف الجاذبية الارضية`")
    if not question and event.reply_to_msg_id and zzz.text: #code by t.me/S_1_02
        question = zzz.text
    if not event.reply_to_msg_id: #code by t.me/S_1_02
        question = event.pattern_match.group(1)
    zed = await edit_or_reply(event, "**⎉╎جـارِ الاتصـال بـ الذكـاء الاصطناعي\n⎉╎الرجـاء الانتظـار .. لحظـات**")
    answer = get_chatgpt_response(question)
    await zed.edit(f"[ᯓ 𝐋𝐈𝐓𝐇𝐎𝐍 𝗖𝗵𝗮𝘁𝗚𝗽𝘁 -💡-](t.me/A1DIIU) **الذكاء الاصطناعي\n⋆──┄─┄─┄───┄─┄─┄──⋆**\n**• س/ {question}\n\n• {answer}**", link_preview=False)

@zedub.zed_cmd(pattern="(pdf|نص pdf)$")
async def zelzal_ai(event):
    reply_message = await event.get_reply_message()
    if not reply_message:
        return await edit_or_reply(event, "**- بالـرد ع رسالـة (نص) .. لـ طباعتهـا لـ  مـلف PDF**")
    chat = "@pdfbot" #Code by T.me/S_1_02
    zzz = await edit_or_reply(event, "**- جـارِ طباعـة النـص الـى ملـف PDF . . .📕╰\n- الرجـاء الانتظـار ثوانـي . . .⏳╰**")
    async with borg.conversation(chat) as conv: #Code by T.me/S_1_02
        try:
            purgeflag = await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/text")
            await conv.get_response()
            await conv.send_message(reply_message) #Code by T.me/S_1_02
            await conv.get_response()
            await conv.send_message("Noto Naskh Arabic")
        except YouBlockedUserError:
            await zedub(unblock("pdfbot"))
            purgeflag = await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("/text")
            await conv.get_response()
            await conv.send_message(reply_message) #Code by T.me/S_1_02
            await conv.get_response()
            await conv.send_message("Noto Naskh Arabic")
        zedthon1 = await conv.get_response()
        if zedthon1.file:
            await borg.send_file(
                event.chat_id,
                zedthon1,
                caption=f"<b>⎉╎تم تحويـل النص الى PDF .. بنجـاح 🍧📕\n⎉╎بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>",
                parse_mode="html",
                reply_to=reply_message,
            )
        else:
            zedthon1 = await conv.get_response()
            await borg.send_file(
                event.chat_id,
                zedthon1,
                caption=f"<b>⎉╎تم تحويـل النص الى PDF .. بنجـاح 🍧📕\n⎉╎بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>",
                parse_mode="html",
                reply_to=reply_message,
            )
        await zzz.delete()
        await delete_conv(event, chat, purgeflag)
        await event.client(DeleteHistoryRequest(381839844, max_id=0, just_clear=True))

#Code by T.me/S_1_02
@zedub.on(events.NewMessage(outgoing=True, pattern='.صورة pdf$'))
async def _(event): #Code by T.me/S_1_02
    reply_message = await event.get_reply_message()
    zzz = await edit_or_reply(event, "**- جـارِ طباعـة الصـورة الـى ملـف PDF . . .📕╰\n- الرجـاء الانتظـار ثوانـي . . .⏳╰**")
    channel_entity = await zedub.get_entity(ppdf)
    await zedub.send_message(ppdf, '/start')
    await asyncio.sleep(0.5)
    msg0 = await zedub.get_messages(ppdf, limit=1)
    await zedub.send_file(ppdf, reply_message)
    await asyncio.sleep(0.5)
    try:
        msg1 = await zedub.get_messages(ppdf, limit=1)
        await msg1[0].click(0)
    except:
        await event.client(DeleteHistoryRequest(1549375781, max_id=0, just_clear=True))
        return await zzz.edit("**⎉╎اووبـس حـدث خطـأ ...؟!**\n**⎉╎حـاول مجـدداً في وقت لاحـق**")
    await asyncio.sleep(0.5)
    msg2 = await zedub.get_messages(ppdf, limit=1)
    await msg2[0].click(0)
    await asyncio.sleep(0.5)
    msg3 = await zedub.get_messages(ppdf, limit=1)
    await asyncio.sleep(0.5)
    msg4 = await zedub.get_messages(ppdf, limit=1)
    await zedub.send_file(
        event.chat_id,
        msg4[0],
        caption=f"<b>⎉╎تم تحويـل الصـورة الى PDF .. بنجـاح 🍧📕\n⎉╎بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>",
        parse_mode="html",
    )
    await zzz.delete()
    await event.client(DeleteHistoryRequest(1549375781, max_id=0, just_clear=True))


# Code by T.me/S_1_02
@zedub.zed_cmd(pattern="كشف(?: |$)(.*)")
async def zelzal_gif(event):
    input_str = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        await edit_or_reply(event, "**- بالـرد ع الشخص او باضافة معـرف/ايـدي الشخـص للامـر**")
    if input_str and not reply_message:
        if input_str.isnumeric():
            uid = input_str
        if input_str.startswith("@"):
            user = await event.client.get_entity(input_str)
            uid = user.id
    if input_str and reply_message:
        if input_str.isnumeric():
            uid = input_str
        if input_str.startswith("@"):
            user = await event.client.get_entity(input_str)
            uid = user.id
    if not input_str and reply_message:
        user = await event.client.get_entity(reply_message.sender_id)
        uid = user.id
    #user = await get_user_from_event(event)
    #if not user:
        #return
    #uid = user.id
    chat = "@SangMata_beta_bot" # Code by T.me/S_1_02
    zed = await edit_or_reply(event, "**⎉╎جـارِ الكشـف ...**")
    async with borg.conversation(chat) as conv: # Code by T.me/S_1_02
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(f"{uid}")
        except YouBlockedUserError:
            await zedub(unblock("SangMata_beta_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(f"{uid}")
        zlz = await conv.get_response()
        mallath = zlz.text
        if "No data available" in mallath: # Code by T.me/S_1_02
            zzl = "<b>⎉╎المستخدم ليس لديه أي سجل اسمـاء بعـد ...</b>"
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        if "Sorry, you have used up your quota for today" in zlz.text:
            zzl = "<b>⎉╎عـذراً .. لقد استنفدت محاولاتك لهذا اليوم.\n⎉╎لديـك 5 محاولات فقط كل يوم\n⎉╎يتم تحديث محاولاتك في الساعة 03:00 بتوقيت مكة كل يوم</b>"
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        if "👤 History for" in mallath:
            zzl = mallath.replace("👤 History for", "ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝐋𝐈𝐓𝐇𝐎𝐍 - <b>سجـل الحسـاب 🪪\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n⌔ تم جلب السجـلات .. بنجـاح ☑️</b> ❝") 
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        await zed.delete()
        return await borg.send_message(event.chat_id, zlz, parse_mode="html")

# Code by T.me/S_1_02
@zedub.zed_cmd(pattern="الاسماء(?: |$)(.*)")
async def zelzal_gif(event):
    input_str = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        await edit_or_reply(event, "**- بالـرد ع الشخص او باضافة معـرف/ايـدي الشخـص للامـر**")
    if input_str and not reply_message:
        if input_str.isnumeric():
            uid = input_str
        if input_str.startswith("@"):
            user = await event.client.get_entity(input_str)
            uid = user.id
    if input_str and reply_message:
        if input_str.isnumeric():
            uid = input_str
        if input_str.startswith("@"):
            user = await event.client.get_entity(input_str)
            uid = user.id
    if not input_str and reply_message:
        user = await event.client.get_entity(reply_message.sender_id)
        uid = user.id
    #user = await get_user_from_event(event)
    #if not user:
        #return
    #uid = user.id
    chat = "@SangMata_beta_bot" # Code by T.me/S_1_02
    zed = await edit_or_reply(event, "**⎉╎جـارِ الكشـف ...**")
    async with borg.conversation(chat) as conv: # Code by T.me/S_1_02
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(f"{uid}")
        except YouBlockedUserError:
            await zedub(unblock("SangMata_beta_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(f"{uid}")
        zlz = await conv.get_response()
        mallath = zlz.text
        if "No data available" in mallath: # Code by T.me/S_1_02
            zzl = "<b>⎉╎المستخدم ليس لديه أي سجل اسمـاء بعـد ...</b>"
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        if "Sorry, you have used up your quota for today" in zlz.text:
            zzl = "<b>⎉╎عـذراً .. لقد استنفدت محاولاتك لهذا اليوم.\n⎉╎لديـك 5 محاولات فقط كل يوم\n⎉╎يتم تحديث محاولاتك في الساعة 03:00 بتوقيت مكة كل يوم</b>"
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        if "👤 History for" in mallath:
            zzl = mallath.replace("👤 History for", "ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝐋𝐈𝐓𝐇𝐎𝐍 - <b>سجـل الحسـاب 🪪\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n⌔ تم جلب السجـلات .. بنجـاح ☑️</b> ❝") 
            await zed.delete()
            return await borg.send_message(event.chat_id, zzl, parse_mode="html")
        await zed.delete()
        return await borg.send_message(event.chat_id, zlz, parse_mode="html")

# Code by T.me/S_1_02
@zedub.zed_cmd(pattern="تحقق ?(.*)")
async def check_user(event):
    input_str = event.pattern_match.group(1)
    if input_str.startswith("+"):
        phone_number = event.pattern_match.group(1)
    else:
        return await edit_or_reply(event, "**• ارسـل الامـر كالتالـي ...𓅫 :**\n`.تحقق` **+ ࢪقـم الهاتـف مـع ࢪمـز الدولـة\n• مثــال :**\n.تحقق +967777118223")
    try:
        username, user_id = await get_names(phone_number)
        if user_id:
            await edit_or_reply(event, f"ᯓ 𝐋𝐈𝐓𝐇𝐎𝐍 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗗𝗮𝘁𝗮 📟\n**⋆─┄─┄─┄─┄─┄─┄─⋆**\n**• معلومـات حسـاب تيليجـرام 📑 :**\n**- اليـوزر :** @{username}\n**- الايـدي :** `{user_id}`")
        else:
            await edit_or_reply(event, "**- الرقـم ليس مسجـل بعـد على تيليجـرام !!**")
    except Exception as e:
        print(f"An error occurred: {e}")

#Code by T.me/S_1_02
@zedub.zed_cmd(pattern="احفظ(?: |$)([\s\S]*)")
async def zelzal_ss(event):
    link = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not link and reply: #Code by T.me/S_1_02
        link = reply.text
    if not link: #Code by T.me/S_1_02
        return await edit_or_reply(event, "**⎉╎باضافة رابـط منشـور لـ الامـر او بالـࢪد ؏ــلى رابـط المنشـور المقيـد**")
    if not link.startswith("https://t.me/"):
        return await edit_or_reply(event, "**⎉╎باضافة رابـط منشـور لـ الامـر او بالـࢪد ؏ــلى رابـط المنشـور المقيـد**")
    if "?single" in link:
        link = link.replace("?single", "")
    zzz = await edit_or_reply(event, f"**- جـارِ تحميـل المنشـور المقيـد انتظـر ... 🍧╰\n- رابـط المنشـور المقيـد :\n{link}**")
    chat = "@Save_restricted_robot"
    await zedub(JoinChannelRequest(channel="@logicxupdates"))
    async with borg.conversation(chat) as conv: #Code by T.me/S_1_02
        try:
            purgeflag = await conv.send_message(link)
        except YouBlockedUserError: #Code by T.me/S_1_02
            await zedub(unblock("Save_restricted_robot"))
            purgeflag = await conv.send_message(link)
        response = await conv.get_response()
        await asyncio.sleep(3)
        try:
            if response.media:
                zedthon1 = response.media
                await borg.send_file(
                    event.chat_id,
                    zedthon1,
                    caption=f"<b>⎉╎تم تحميـل المنشـور المقيـد .. بنجـاح 🎆\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>",
                    parse_mode="html",
                )
            else:
                zedthon1 = await conv.get_response()
                await borg.send_message(
                    event.chat_id,
                    f"{zedthon1}\n\n<b>⎉╎تم تحميـل المنشـور المقيـد .. بنجـاح 🎆\n⎉╎الرابـط 🖇:  {link}\n⎉╎تم التحميـل بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>",
                    parse_mode="html",
                    link_preview=False,
                )
        except:
            pass
        await zzz.delete()
        await delete_conv(event, chat, purgeflag)
        await event.client(DeleteHistoryRequest(6109696397, max_id=0, just_clear=True))


@zedub.zed_cmd(pattern="(معرفاتي|يوزراتي)$")
async def _(event):
    zzz = await edit_or_reply(event, "**⎉╎جـارِ جلب يـوزرات حسابـك ⅏ . . .**")
    result = await event.client(GetAdminedPublicChannelsRequest())
    output_str = "ᯓ 𝐋𝐈𝐓𝐇𝐎𝐍 𝗨𝘀𝗲𝗿𝗯𝗼𝘁 **- 🝢 - يوزراتـك العامـة** \n**⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆**\n"
    for channel_obj in result.chats:
        output_str += f"•┊{channel_obj.title} - @{channel_obj.username} \n"
    await zzz.delete()
    await zedub.send_message(event.chat_id, output_str)


# Function to split Arabic words into individual letters
def split_arabic(input_text): #Write Code By T.me/S_1_02
    letters = []
    for char in input_text:
        if char.isalpha():
            letters.append(char)
    return ' '.join(letters)

@zedub.zed_cmd(pattern=f"تفكيك(?: |$)(.*)")
async def handle_event(event): #Write Code By T.me/S_1_02
    malath = event.pattern_match.group(1)
    if malath:
        zelzal = malath
    elif event.is_reply:
        zelzal = await event.get_reply_message()
    else:
        return await edit_or_reply(event, "**⎉╎باضافة كلمة لـ الامـر او بالـࢪد ؏ــلى كلمة لتفكيكها**")
    split_message = split_arabic(zelzal)
    await zedub.send_message(event.chat_id, split_message)
    await event.delete()

@zedub.zed_cmd(pattern=f"ت(?: |$)(.*)")
async def handle_event(event): #Write Code By T.me/S_1_02
    malath = event.pattern_match.group(1)
    if malath:
        zelzal = malath
    elif event.is_reply:
        zelzal = await event.get_reply_message()
    else:
        return await edit_or_reply(event, "**⎉╎باضافة كلمة لـ الامـر او بالـࢪد ؏ــلى كلمة لتفكيكها**")
    split_message = split_arabic(zelzal)
    await zedub.send_message(event.chat_id, split_message)
    await event.delete()
