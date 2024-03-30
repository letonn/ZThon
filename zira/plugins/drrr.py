import os
import random
import asyncio
import base64
import contextlib
import shutil
import requests
from datetime import datetime
from telethon import events, types
from telethon.utils import get_peer_id, get_display_name
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl import functions
from telethon.tl.types import Channel, Chat, InputPhoto, User, InputMessagesFilterEmpty
from telethon.tl.functions.channels import GetParticipantRequest, GetFullChannelRequest
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.users import GetFullUserRequest
from telethon.errors.rpcerrorlist import ForbiddenError
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetStickerSetRequest, ExportChatInviteRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from . import zedub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type, unsavegif, progress
from ..helpers.utils import _zedtools, _zedutils, _format, parse_pre, reply_id
from ..sql_helper.autopost_sql import add_post, get_all_post, is_post, remove_post
from ..sql_helper.echo_sql import addecho, get_all_echos, get_echos, is_echo, remove_all_echos, remove_echo, remove_echos
from ..core.data import blacklist_chats_list
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper import global_collectionjson as sql
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import *

plugin_category = "الادوات"
LOGS = logging.getLogger(__name__)

NASHR = gvarstatus("Z_NASHR") or "(نشر عام|سوبر)"
SPRS = gvarstatus("Z_SPRS") or "(نشر_تلقائي|نشر|تلقائي)"
OFSPRS = gvarstatus("Z_OFSPRS") or "(ايقاف_النشر|ايقاف النشر|ستوب)"

ZelzalNSH_cmd = (
    "𓆩 [𝗦𝗼𝘂𝗿𝗰𝗲 𝐋𝐈𝐓𝐇𝐎𝐍 - اوامـر النشـر التلقـائي](t.me/A1DIIU) 𓆪\n\n"
    "**- اضغـط ع الامـر للنسـخ** \n\n\n"
    "**⪼** `.تلقائي` \n"
    "**- الامـر + (معـرف/ايـدي/رابـط) القنـاة المـراد النشـر التلقـائي منهـا** \n"
    "**- استخـدم الامـر بقنـاتـك \n\n\n"
    "**⪼** `.ايقاف النشر` \n"
    "**- الامـر + (معـرف/ايـدي/رابـط) القنـاة المـراد ايقـاف النشـر التلقـائي منهـا** \n"
    "**- استخـدم الامـر بقنـاتـك \n\n\n"
    "**- ملاحظـه :**\n"
    "**- الاوامـر صـارت تدعـم المعـرفات والروابـط الى جـانب الايـدي 🏂🎗**\n"
    "**🛃 سيتـم اضـافة المزيـد من اوامــر النشـر التلقـائي بالتحديثـات الجـايه**\n"
)

ZelzalSuper_cmd = (
    "[ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝐋𝐈𝐓𝐇𝐎𝐍 🎡 النشـࢪ التڪࢪاࢪي العـام](t.me/A1DIIU) .\n"
    "**⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆**\n"
    "**⎉╎قـائمـة اوامـر السـوبـر (النشـر العـام) الخاصـه بـ سـورس ليثون ♾ :**\n\n"
    "`.سوبر`\n"
    "**⪼ الامـر + عـدد الثـوانـي + عـدد مـرات التكـرار (بالـرد ع رسـالة او ميديـا)**\n"
    "**⪼ لـ النشـر التكـراري العـام بكـل مجموعـات قائمـة السـوبـر ( خـاص بجماعـة بالسـوبـرات ) ...✓**\n\n"
    "ٴ┄─┄─┄─┄┄─┄─┄─┄─┄┄\n\n"
    "`.اضف سوبر`\n"
    "**⪼ استخـدم الامـر داخـل المجموعـة المحـدده ...**\n"
    "**⪼ او استخـدم (الامـر + ايديـات السوبـرات) لـ اضافـة عـدة سـوبـرات الـى القائمـة ...**\n"
    "**⪼ مثــال (.اضف سوبر 244324554 4654454555 1345563234) ...**\n"
    "**⪼ لـ اضافة مجموعـة محـددة او عـدة مجمـوعـات لـ قائمـة السوبـر ...✓**\n\n"
    "ٴ┄─┄─┄─┄┄─┄─┄─┄─┄┄\n\n"
    "`.حذف سوبر`\n"
    "**⪼ استخـدم الامـر داخـل المجموعـة المحـدده ...**\n"
    "**⪼ او استخـدم (الامـر + ايديـات السوبـرات) لـ حـذف السـوبـرات مـن القائمـة ...**\n"
    "**⪼ مثــال (.حذف سوبر 244324554 4654454555 1345563234) ...**\n"
    "**⪼ لـ حـذف مجموعـة محـددة او عـدة مجمـوعـات مـن قائمـة السوبـر ...✓**\n\n"
    "ٴ┄─┄─┄─┄┄─┄─┄─┄─┄┄\n\n"
    "`.السوبرات`\n"
    "**⪼ لـ جلب قائمـة مجموعـات السوبـر الخاصـه بك ...✓**\n\n"
    "ٴ┄─┄─┄─┄┄─┄─┄─┄─┄┄\n\n"
    "`.ايقاف سوبر`\n"
    "**⪼ استخـدم الامـر داخـل المجموعـة المحـدده ...**\n"
    "**⪼ لـ إيقـاف النشـر العـام عـن مجموعـة معينـه ...✓**\n\n"
    "ٴ┄─┄─┄─┄┄─┄─┄─┄─┄┄\n\n"
    "`.ايقاف السوبرات`\n"
    "**⪼ لـ إيقـاف النشـر التكـراري العـام عـن جميـع المجموعـات ...✓**\n\n"
    "ٴ┄─┄─┄─┄┄─┄─┄─┄─┄┄\n\n"
    "**⪼ مـلاحظــات هـامــه :**\n"
    "- اوامـر السوبـرات إضـافة جديـدة خاصـه وحصريـه بسـورس ليثون¹ فقـط ...\n"
    "- تحديثات السوبـر متواصـلة لـ إضـافة كـل ماهـو جديـد بالتحديثـات الجايـه ...\n"
    "- نسعـى جاهـدين لـ جعـل اوامـر السوبـر سهـله وسلسـه لـكي توفـر لكـم الجهـد والتعب ...\n"
    "- شكـر خـاص لـ منصبيـن السـورس علـى افكـارهم الرائعـه والمفيـده ...\n"
    "\n𓆩 [𝐋𝐈𝐓𝐇𝐎𝐍 𝗨𝘀𝗲𝗿𝗯𝗼𝘁](t.me/A1DIIU) 𓆪"
)

# Write Code By T.me/zzzzl1l
ZED_BLACKLIST = [
    -1002137527137,
    -1002137527137,
    ]

ss = []

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


# Write Code By T.me/zzzzl1l
# Copyright (C) 20223 T.me/A1DIIU . All Rights Reserved
async def super_function(event, zelzal, zed, sleeptimet, er, done):
    # sourcery no-metrics
    counter = int(zed[0])
    num = 0
    blkchats = blacklist_chats_list()
    for k, i in enumerate(blkchats, start=1):
        num += 1
    if event.reply_to_msg_id:
        for _ in range(counter):
            if gvarstatus("nashrwork") is None:
                return
            for chat_id in blkchats:
                chat = await event.client.get_entity(chat_id)
                chat = chat.id
                if chat not in ZED_BLACKLIST and chat not in ss:
                    try:
                        if zelzal.text: #Write Code By T.me/zzzzl1l
                            try:
                                await event.client.send_message(chat, zelzal)
                                done += 1
                                await asyncio.sleep(sleeptimet)
                            except BaseException:
                                er += 1
                                await asyncio.sleep(sleeptimet)
                        else:
                            try: #Write Code By T.me/zzzzl1l
                                await event.client.send_file(
                                    chat,
                                    zelzal,
                                    caption=zelzal.caption,
                                )
                                done += 1
                                await _zedutils.unsavegif(event, zelzal)
                                await asyncio.sleep(sleeptimet)
                            except BaseException:
                                er += 1
                                await asyncio.sleep(sleeptimet)
                    except BaseException:
                        er += 1
                    except BaseException:
                        return
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝐋𝐈𝐓𝐇𝐎𝐍 🎡 **النشــࢪ التڪـࢪاࢪي العـام**\n**⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆**\n"
                + f"**- تم الانتهـاء من النشـࢪ .. بنجـاح ✅**\n**- تم النشـࢪ فـي ** {num} **ڪـࢪوب**\n**- عـدد النشـࢪ** {counter} **مـࢪات**\n**- لـ الࢪسالة أدناه بـ تأخيـࢪ** {sleeptimet} **ثانيـه**",
            )
            if zelzal.text:
                zelzal = await event.client.send_message(BOTLOG_CHATID, zelzal)
            else:
                zelzal = await event.client.send_file(BOTLOG_CHATID, zelzal)
                await _zedutils.unsavegif(event, zelzal)
        return

# Write Code By T.me/zzzzl1l
# Copyright (C) 20223 T.me/A1DIIU . All Rights Reserved
@zedub.zed_cmd(pattern=f"{NASHR} ([\s\S]*)")
async def gcast(event):
    reply = await event.get_reply_message()
    input_str = "".join(event.text.split(maxsplit=1)[1:]).split(" ", 2)
    er = 0
    done = 0
    blkchats = blacklist_chats_list()
    if len(blkchats) == 0:
        return await edit_or_reply(event, "**⎉╎لا يوجد مجموعات في قائمة مجموعات السـوبر ؟!**\n**⎉╎لـ تصفـح اوامـر السـوبرات ارسـل الامـر** ( `.اوامر السوبر` )")
    if event.reply_to_msg_id: #Write Code By T.me/zzzzl1l
        zelzal = await event.get_reply_message()
    else:
        await edit_or_reply(event, "**⎉╎بالـࢪد ؏ــلى ࢪسـالة او وسائـط**")
        return
    try:
        sleeptimet = int(input_str[0])
    except Exception:
        return await edit_or_reply(event, "**- ارسـل الامـر بالشكـل الآتي**\n\n`.سوبر` **+ عدد الثواني + عدد المرات بالـرد ع الرسالة**\n**- مثـال : .سوبر 12 12 بالـرد ع رسالـه**")
    zzz = await edit_or_reply(event, "**⎉╎جـاري بـدء النشـر في المجموعـات ...الرجـاء الانتظـار**")
    zed = input_str[1:]
    zaz = int(zed[0])
    await zzz.edit(
        f"**- النشــر التڪـراري العـام ♽**\nٴ**•────‌‌‏─‌‌‏✯ 𝐋𝐈𝐓𝐇𝐎𝐍 ✯──‌‌‏─‌‌‏─‌‌‏─•**\n**⎉╎تمت بـدء النشـر .. بنجـاح ✅ **\n\n**⎉╎عـدد المـرات** {zaz}\n**⎉╎بـ تأخيـر** {sleeptimet} **ثانيـه ⏳**\n\n**⎉╎لـ ايقافـه في مجموعة محدده ارسـل** ( `.ايقاف سوبر` ) **داخل المجموعة**\n**⎉╎لـ ايقافـه عـام ارسـل** ( `.ايقاف السوبرات` )"
    )
    addgvar("nashrwork", True)
    if BOTLOG:
        rss = "ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝐋𝐈𝐓𝐇𝐎𝐍 🎡 <b>النشــࢪ التڪـࢪاࢪي العـام</b>\n<b>⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆</b>"
        rss += f"\n<b>• تمت بـدء النشـر .. بنجـاح ✅ </b>"
        if reply.text:
            rss += f"\n<b>• الرسـالة المنشـورة :</b>\n<code>{reply.text}</code>"
        rss += f"\n<b>• عـدد المـرات</b> {zaz}"
        rss += f"\n<b>• بـ تأخيـر</b> {sleeptimet} <b>ثانيـه ⏳</b>"
        rss += f"\n\n<b>• لـ ايقافـه في مجموعة محدده ارسـل</b> ( <code>.ايقاف سوبر</code> ) <b>داخل المجموعة</b>"
        rss += f"\n<b>• لـ ايقافـه عـام ارسـل</b> ( <code>.ايقاف السوبرات</code> )"
        await event.client.send_message(
            BOTLOG_CHATID,
            rss,
            parse_mode="html",
            link_preview=False,
        )
    await super_function(event, reply, zed, sleeptimet, er, done)

# Write Code By T.me/zzzzl1l
# Copyright (C) 20223 T.me/A1DIIU . All Rights Reserved
@zedub.zed_cmd(pattern="ايقاف السوبرات$")
async def stopspamrz(event):
    if gvarstatus("nashrwork") is not None and gvarstatus("nashrwork") == "true":
        delgvar("nashrwork")
        return await edit_or_reply(event, "**- تم ايقـاف النشـر التڪـراري العـام للكروبـات .. بنجـاح ✅**")
    return await edit_or_reply(event, "**- لايوجـد نشـر تڪراري عـام لـ إيقافه ؟!**")

# Write Code By T.me/zzzzl1l
# Copyright (C) 20223 T.me/A1DIIU . All Rights Reserved
@zedub.zed_cmd(pattern="ايقاف سوبر$")
async def stopspamrz(event):
    if not event.is_group:
        return await edit_or_reply(event, "**✾╎عـذراً .. اوامـر السوبـر خـاصه بالمجموعـات فقـط**")
    if gvarstatus("nashrwork") is not None and gvarstatus("nashrwork") == "true":
        ss.append(event.chat_id)
        return await edit_or_reply(event, "**- تم ايقـاف النشـر التڪـراري هنـا .. بنجـاح ✅**")
    return await edit_or_reply(event, "**- لايوجـد هنـا نشـر تڪراري عـام لـ إيقافه ؟!**")

# Write Code By T.me/zzzzl1l
# Copyright (C) 20223 T.me/A1DIIU . All Rights Reserved
@zedub.zed_cmd(
    pattern="اضف سوبر?(?:\s|$)([\s\S]*)",
    command=("addblkchat", plugin_category),
    info={
        "header": "To add chats to blacklist.",
        "description": "to add the chats to database so your bot doesn't work in\
         thoose chats. Either give chatids as input or do this cmd in the chat\
         which you want to add to db.",
        "usage": [
            "{tr}addblkchat <chat ids>",
            "{tr}addblkchat in the chat which you want to add",
        ],
    },
)
async def add_blacklist_chat(event):
    "To add chats to blacklist."
    input_str = event.pattern_match.group(1)
    errors = ""
    result = ""
    blkchats = blacklist_chats_list()
    if not event.is_group:
        return await edit_or_reply(event, "**✾╎عـذراً .. اوامـر السوبـر خـاصه بالمجموعـات فقـط**")
    try:
        blacklistchats = sql.get_collection("blacklist_chats_list").json
    except AttributeError:
        blacklistchats = {}
    if input_str:
        input_str = input_str.split(" ")
        for chatid in input_str:
            try:
                chatid = int(chatid.strip())
                if chatid in blkchats:
                    return await edit_or_reply(event, "**✾╎عـذراً .. هـذه المجموعـة مضافة مسبقـاً لقائمـة مجموعـات السوبـر**")
                chat = await event.client.get_entity(chatid)
                date = str(datetime.now().strftime("%B %d, %Y"))
                chatdata = {
                    "chat_id": chat.id,
                    "chat_name": get_display_name(chat),
                    "chat_username": chat.username,
                    "date": date,
                }
                blacklistchats[str(chat.id)] = chatdata
                result += (
                    f"**• تم اضافـة المجموعـة**  {get_display_name(chat)} **.. بنجـاح ☑️**\n**• لـ ڪـروبـات السـوبـر 🎡**\n"
                )
            except Exception as e:
                errors += f"**حدث خطـأ عنـد محاولة اضافة المجموعة {chatid}** - __{e}__\n"
    else:
        chat = await event.get_chat()
        try:
            chatid = chat.id
            if chat.id in blkchats:
                return await edit_or_reply(event, "**✾╎عـذراً .. هـذه المجموعـة مضافة مسبقـاً لقائمـة مجموعـات السوبـر**")
            else:
                date = str(datetime.now().strftime("%B %d, %Y"))
                chatdata = {
                    "chat_id": chat.id,
                    "chat_name": get_display_name(chat),
                    "chat_username": chat.username,
                    "date": date,
                }
                blacklistchats[str(chat.id)] = chatdata
                result += (
                    f"**• تم اضافـة المجموعـة**  {get_display_name(chat)} **.. بنجـاح ☑️**\n**• لـ ڪـروبـات السـوبـر 🎡**\n"
                )
        except Exception as e:
            errors += f"**حدث خطـأ عنـد محاولة اضافة المجموعة {chatid}** - __{e}__\n"
    sql.del_collection("blacklist_chats_list")
    sql.add_collection("blacklist_chats_list", blacklistchats, {})
    output = ""
    if result != "":
        output += f"ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝐋𝐈𝐓𝐇𝐎𝐍 🎡 **ڪـࢪوبـات السوبـࢪ**\n**⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆**\n{result}\n"
    if errors != "":
        output += f"**• الاخطـاء :**\n{errors}\n"
    if result != "":
        output += "**• يتـم الان اعـادة تشغيـل بـوت ليثون**\n"
        output += "**• قـد يستغـرق الامـر 2-1 دقائـق ▬▭ ...**"
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            output,
        )
    msg = await edit_or_reply(event, output)
    await event.client.reload(msg)

# Write Code By T.me/zzzzl1l
# Copyright (C) 20223 T.me/A1DIIU . All Rights Reserved
@zedub.zed_cmd(
    pattern="حذف سوبر?(?:\s|$)([\s\S]*)",
    command=("rmblkchat", plugin_category),
    info={
        "header": "To remove chats to blacklist.",
        "description": "to remove the chats from database so your bot will work in\
         those chats. Either give chatids as input or do this cmd in the chat\
         which you want to remove from db.",
        "usage": [
            "{tr}rmblkchat <chat ids>",
            "{tr}rmblkchat in the chat which you want to add",
        ],
    },
)
async def add_blacklist_chat(event):
    "To remove chats from blacklisted chats."
    input_str = event.pattern_match.group(1)
    errors = ""
    result = ""
    blkchats = blacklist_chats_list()
    try:
        blacklistchats = sql.get_collection("blacklist_chats_list").json
    except AttributeError:
        blacklistchats = {}
    if input_str:
        input_str = input_str.split(" ")
        for chatid in input_str:
            try:
                chatid = int(chatid.strip())
                if chatid in blkchats:
                    chatname = blacklistchats[str(chatid)]["chat_name"]
                    del blacklistchats[str(chatid)]
                    result += (
                        f"**• تم ازالـة المجموعـة**  {chatname} **.. بنجـاح ☑️**\n**• مـن ڪـروبـات السـوبـر 🎡**\n"
                    )
                else:
                    return await edit_or_reply(event, f"**✾╎عـذراً .. المجموعـة** {chatid} **ليست مضافة اصـلاً لقائمـة مجموعـات السوبـر**")
            except Exception as e:
                errors += f"**حدث خطـأ عنـد محاولة ازالة المجموعة {chatid}** - __{e}__\n"
    else:
        chat = await event.get_chat()
        try:
            chatid = chat.id
            if chatid in blkchats:
                chatname = blacklistchats[str(chatid)]["chat_name"]
                del blacklistchats[str(chatid)]
                result += f"**• تم ازالـة المجموعـة**  {chatname} **.. بنجـاح ☑️**\n**• مـن ڪـروبـات السـوبـر 🎡**\n"
            else:
                return await edit_or_reply(event, f"**✾╎عـذراً .. المجموعـة** {chatid} **ليست مضافة اصـلاً لقائمـة مجموعـات السوبـر**")
        except Exception as e:
            errors += f"**حدث خطـأ عنـد محاولة ازالة المجموعة {chatid}** - __{e}__\n"
    sql.del_collection("blacklist_chats_list")
    sql.add_collection("blacklist_chats_list", blacklistchats, {})
    output = ""
    if result != "":
        output += f"ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝐋𝐈𝐓𝐇𝐎𝐍 🎡 **ڪـࢪوبـات السوبـࢪ**\n**⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆**\n{result}\n"
    if errors != "":
        output += f"**• الاخطـاء :**\n{errors}\n"
    if result != "":
        output += "**• يتـم الان اعـادة تشغيـل بـوت ليثون**\n"
        output += "**• قـد يستغـرق الامـر 2-1 دقائـق ▬▭ ...**"
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            output,
        )
    msg = await edit_or_reply(event, output)
    await event.client.reload(msg)

# Write Code By T.me/zzzzl1l
# Copyright (C) 20223 T.me/A1DIIU . All Rights Reserved
@zedub.zed_cmd(pattern="السوبرات$")
async def add_blacklist_chat(event):
    blkchats = blacklist_chats_list()
    try:
        blacklistchats = sql.get_collection("blacklist_chats_list").json
    except AttributeError:
        blacklistchats = {}
    if len(blkchats) == 0:
        return await edit_delete(
            event, "**- لا يوجـد كروبـات بعـد فـي قائمـة السوبـرات ؟؟**"
        )
    result = "ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝐋𝐈𝐓𝐇𝐎𝐍 🎡 **ڪـࢪوبـات السوبـࢪ**\n**⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆**\n"
    for chat in blkchats:
        result += f"**• المجموعة :** {blacklistchats[str(chat)]['chat_name']}\n"
        result += f"**• الايدي :** `{chat}`\n"
        username = blacklistchats[str(chat)]["chat_username"] or "لا يوجـد"
        result += f"**• اليوزࢪ :** {username}\n"
        result += f"**• تم اضافتها بتاࢪيخ :** {blacklistchats[str(chat)]['date']}\n\n"
    await edit_or_reply(event, result)


# Write Code By T.me/zzzzl1l
# Copyright (C) 20223 T.me/A1DIIU . All Rights Reserved
@zedub.zed_cmd(pattern="(اوامر السوبرات|اوامر السوبر)")
async def cmd_super(zelzallll):
    await edit_or_reply(zelzallll, ZelzalSuper_cmd)

# Copyright (C) 2022 LltHoN . All Rights Reserved
@zedub.zed_cmd(pattern="(النشر|اوامر النشر)")
async def cmd_nasher(zilzallll):
    await edit_or_reply(zilzallll, ZelzalNSH_cmd)

# Copyright (C) 2022 LltHoN . All Rights Reserved
@zedub.zed_cmd(pattern="(نشر تلقائي|تلقائي)(?:\s|$)([\s\S]*)")
async def _(event):
    if event.is_private:
        return await edit_or_reply(event, "**⎉╎عـذراً .. النشر التلقائي خـاص بالقنـوات/المجموعات فقـط\n⎉╎قم باستخـدام الامـر داخـل القنـاة/المجموعة الهـدف**")
    if input_str := event.pattern_match.group(2):
        try:
            zch = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_or_reply(event, "**⎉╎عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**⎉╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")
        try:
            if is_post(zch.id , event.chat_id):
                return await edit_or_reply(event, "**⎉╎النشـر التلقـائي مفعـل مسبقـاً ✓**")
            if zch.first_name:
                await asyncio.sleep(1.5)
                add_post(zch.id, event.chat_id)
                await edit_or_reply(event, "**⎉╎تم تفعيـل النشـر التلقـائي من القنـاة .. بنجـاح ✓**")
        except Exception:
            try:
                if is_post(zch.id , event.chat_id):
                    return await edit_or_reply(event, "**⎉╎النشـر التلقـائي مفعـل مسبقـاً ✓**")
                if zch.title:
                    await asyncio.sleep(1.5)
                    add_post(zch.id, event.chat_id)
                    return await edit_or_reply(event, "**⎉╎تم تفعيـل النشـر التلقـائي من القنـاة .. بنجـاح ✓**")
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "**⎉╎عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**⎉╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")

# Copyright (C) 2022 LltHoN . All Rights Reserved
@zedub.zed_cmd(pattern="(ايقاف النشر|ستوب)(?:\s|$)([\s\S]*)")
async def _(event):
    if event.is_private:
        return await edit_or_reply(event, "**⎉╎عـذراً .. النشر التلقائي خـاص بالقنـوات/المجموعات فقـط\n⎉╎قم باستخـدام الامـر داخـل القنـاة/المجموعة الهـدف**")
    if input_str := event.pattern_match.group(2):
        try:
            zch = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_or_reply(event, "**⎉╎عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**⎉╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")
        try:
            if not is_post(zch.id, event.chat_id):
                return await edit_or_reply(event, "**⎉╎عـذراً .. النشـر التلقـائي غير مفعـل اسـاسـاً ؟!**")
            if zch.first_name:
                await asyncio.sleep(1.5)
                remove_post(zch.id, event.chat_id)
                await edit_or_reply(event, "**⎉╎تم تعطيـل النشر التلقـائي هنـا .. بنجـاح ✓**")
        except Exception:
            try:
                if not is_post(zch.id, event.chat_id):
                    return await edit_or_reply(event, "**⎉╎عـذراً .. النشـر التلقـائي غير مفعـل اسـاسـاً ؟!**")
                if zch.title:
                    await asyncio.sleep(1.5)
                    remove_post(zch.id, event.chat_id)
                    return await edit_or_reply(event, "**⎉╎تم تعطيـل النشر التلقـائي هنـا .. بنجـاح ✓**")
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "**⎉╎عـذراً .. معـرف/ايـدي القنـاة غيـر صـالح**\n**⎉╎الرجـاء التـأكـد مـن المعـرف/الايـدي**")


# =========================================================== #
#                                                             𝙕𝙏𝙝𝙤𝙣
# =========================================================== #
#                                           الملف كتابتي من الصفر ومتعوب عليه                            #
#                                  مامسموحلك تخمـط So تخمـط = اهينك وافضحك                   #
# =========================================================== #
#                                                             𝙕𝙏𝙝𝙤𝙣
# =========================================================== #
blocked_word = ["sex", "سكس", "نيك", "نيج", "كحاب", "سحاق", "porn"]
blocked_channels = ["ZlZZll7", "M_iaar_M", "RS_F_Z", "LL_7L", "OoO15", "JO6JJ", "ZlZZl771", "zzzzl1l1", "ZedThon1", "EARCXb", "zzzzl1lj", "Dakson_SDR12", "w352xd", "AAffoopp12", "Slomsfr", "BT224"]

# Copyright (C) 2023 LltHoN . All Rights Reserved
@zedub.zed_cmd(pattern="تلي (.*)")
async def _(event): # Code by t.me/zzzzl1l
    search = event.pattern_match.group(1)
    if "sex" in search or "porn" in search or "سكس" in search or "نيك" in search or "نيج" in search or "سحاق" in search or "كحاب" in search or "تبياته" in search:
        return await edit_delete(event, "**- البحث عـن قنـوات غيـر اخلاقيـه محظـور 🔞؟!**", 5)
    l = 'qwertyuiopasdfghjklxcvbnmz'
    result = await zedub(functions.contacts.SearchRequest(
        q=search,
        limit=20
    ))
    json = result.to_dict()
    i = str(''.join(random.choice(l) for i in range(3))) + '.txt'
    counter = 0
    for item in json['chats']:
        channel_id = item["username"]
        if channel_id not in blocked_channels:
            links = f'https://t.me/{channel_id}'
            counter += 1
            open(i, 'a').write(f"{counter}• {links}\n")
    link = open(i, 'r').read()
    if not link:
        await event.edit("**- لا توجد نتائج في البحث**")
    else:
        await event.edit(f'''
ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝐋𝐈𝐓𝐇𝐎𝐍 - **بـحـث تيليـجـࢪام**
⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆
l {search} l  **🔎 نتائـج البحث عـن -**
l قنوات + مجموعات l **يشمـل -**

{link}
        ''')

# =========================================================== #
#                                                             𝙕𝙏𝙝𝙤𝙣
# =========================================================== #
#                                           الملف كتابتي من الصفر ومتعوب عليه                            #
#                                  مامسموحلك تخمـط So تخمـط = اهينك وافضحك                   #
# =========================================================== #
#                                                             𝙕𝙏𝙝𝙤𝙣
# =========================================================== #
# Copyright (C) 2023 LltHoN . All Rights Reserved
@zedub.zed_cmd(pattern="كلمه (.*)")
async def _(event):
    search_word = event.pattern_match.group(1)
    chat = await event.get_chat()
    chat_name = chat.title
    l = 'qwertyuiopasdfghjklxcvbnmz'
    messages = await zedub.get_messages(chat, filter=InputMessagesFilterEmpty(), limit=100)
    i = str(''.join(random.choice(l) for i in range(3))) + '.txt'
    counter = 0
    for message in messages:
        if message.message and search_word in message.message:
            links = f'https://t.me/c/{chat.id}/{message.id}'
            counter += 1
            open(i, 'a').write(f"{counter}• {links}\n")
    link = open(i, 'r').read()
    if not link:
        await event.edit("**- لا توجد نتائج في البحث**")
    else:
         await event.edit(f"**ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝐋𝐈𝐓𝐇𝐎𝐍 - بـحـث تيليـجـࢪام \n ⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆ \n l {search_word} l  نتائـج البحث عـن - \n l {chat_name} l  فـي المجموعـة - \n {link}**")

Z = (
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⣾⣿⠁⢸⣿⣧⠀⣿⣿⠉⠹⣿⣆⠉⠉⠉⠉⣿⣿⠟⠀⠀⠀\n"
    "⣿⣿⠀⠘⠛⠛⠀⣿⣿⠀⠀⣿⣿⠀⠀⠀⣼⣿⡟⠀⠀⠀⠀\n"
    "⣿⣿⠀⠀⠀⠀⠀⣿⣿⣤⣾⡿⠃⠀⠀⣼⣿⡟⠀⠀⠀⠀⠀\n"
    "⣿⣿⠀⠀⠀⠀⠀⣿⣿⢻⣿⣇⠀⠀⠀⣿⣿⠁⠀⠀⠀⠀⠀\n"
    "⣿⣿⠀⢸⣿⣷⠀⣿⣿⠀⣿⣿⡄⠀⠀⣿⣿⠀⠀⠀⠀⠀⠀\n"
    "⢻⣿⣦⣼⣿⠏⠀⣿⣿⠀⢸⣿⣧⠀⢀⣿⣿⠀⠀⠀⠀⠀⠀\n"
    "⠈⠛⠛⠛⠋⠀⠀⠛⠛⠀⠀⠛⠛⠀⠸⠛⠛⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⣴⣿⢿⣷⠒⠲⣾⣾⣿⣿⠀⠀⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⣴⣿⠟⠁⠀⢿⣿⠁⣿⣿⣿⠻⣿⣄⠀⠀⠀⠀⠀\n"
    "⠀⠀⣠⡾⠟⠁⠀⠀⠀⢸⣿⣸⣿⣿⣿⣆⠙⢿⣷⡀⠀⠀⠀\n"
    "⣰⡿⠋⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⠀⠀⠉⠻⣿⡀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣆⠂⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⡿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⠿⠟⠀⠀⠻⣿⣿⡇⠀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⠀⢀⣾⡿⠃⠀⠀⠀⠀⠀⠘⢿⣿⡀⠀⠀⠀⠀\n"
    "⠀⠀⠀⠀⠀⣰⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣷⡀⠀⠀⠀\n"
    "⠀⠀⠀⠀⢠⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣧⠀⠀⠀\n"
    "⠀⠀⠀⢀⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣆⠀⠀\n"
    "⠀⠀⠠⢾⠇⠀⠀⠀⠀  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣷⡤.\n"
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀sɪɪɪɪᴜᴜᴜᴜ⠀⠀ ⠀⠀⠀⠀⠀⠀\n"
)




@zedub.zed_cmd(pattern="كريس")
async def cr7(crr): # Code by t.me/zzzzl1l
    await crr.edit(Z)
    


@zedub.zed_cmd(pattern="ماريو")
async def mario(mario):
    await mario.edit(f'''
➖➖➖🟥🟥🟥🟥🟥🟥
➖➖🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥
➖➖🟫🟫🟫🟨🟨🟨⬛🟨
➖🟫🟨🟫🟨🟨🟨🟨⬛🟨🟨🟨
➖🟫🟨🟫🟫🟨🟨🟨🟨⬛🟨🟨
➖🟫🟫🟨🟨🟨🟨🟨⬛⬛⬛⬛
➖➖➖🟨🟨🟨🟨🟨🟨🟨🟨
➖➖🟥🟥🟦🟥🟥🟥🟥
➖🟥🟥🟥🟦🟥🟥🟦🟥🟥🟥
🟥🟥🟥🟥🟦🟦🟦🟦🟥🟥🟥🟥
🟨🟨🟥🟦🟨🟦🟦🟨🟦🟥🟨🟨
🟨🟨🟨🟦🟦🟦🟦🟦🟦🟨🟨🟨
🟨🟨🟦🟦🟦🟦🟦🟦🟦🟦🟨🟨
➖➖🟦🟦🟦➖➖🟦🟦🟦
➖🟫🟫🟫➖➖➖➖🟫🟫🟫
🟫🟫🟫🟫➖➖➖➖🟫🟫🟫🟫
    ''')



@zedub.zed_cmd(pattern="ضفدع")
async def frog(frog):
    await frog.edit(f'''
⬜️⬜️🟩🟩⬜️🟩🟩
⬜️🟩🟩🟩⬜️🟩🟩🟩
🟩🟩🟩🟩🟩🟩🟩🟩🟩
🟩⬜️⬛️⬜️🟩⬜️⬛️⬜️🟩
🟩🟩🟩🟩🟩🟩🟩🟩
🟩🟩🟥🟥🟥🟥🟥🟥🟥
🟩??🟥🟥🟥🟥🟥🟥🟥
🟩🟩🟩🟩🟩🟩🟩🟩
    ''')


@zedub.zed_cmd(pattern="اجري$")
async def _(kst):
    chars = (
        "🏃                        🦖",
        "🏃                       🦖",
        "🏃                      🦖",
        "🏃                     🦖",
        "🏃                    🦖",
        "🏃                   🦖",
        "🏃                  🦖",
        "🏃                 🦖",
        "🏃                🦖",
        "🏃               🦖",
        "🏃              🦖",
        "🏃             🦖",
        "🏃            🦖",
        "🏃           🦖",
        "🏃          🦖",
        "🏃           🦖",
        "🏃            🦖",
        "🏃             🦖",
        "🏃              🦖",
        "🏃               🦖",
        "🏃                🦖",
        "🏃                 🦖",
        "🏃                  🦖",
        "🏃                   🦖",
        "🏃                    🦖",
        "🏃                     🦖",
        "🏃                    🦖",
        "🏃                   🦖",
        "🏃                  🦖",
        "🏃                 🦖",
        "🏃                🦖",
        "🏃               🦖",
        "🏃              🦖",
        "🏃             🦖",
        "🏃            🦖",
        "🏃           🦖",
        "🏃          🦖",
        "🏃         🦖",
        "🏃        🦖",
        "🏃       🦖",
        "🏃      🦖",
        "🏃     🦖",
        "🏃    🦖",
        "🏃   🦖",
        "🏃  🦖",
        "🏃 🦖",
        "🧎🦖",
    )
    for char in chars:
        await asyncio.sleep(0.3)
        await edit_or_reply(kst, char)


@zedub.zed_cmd(pattern="(كلبي|فكيو|ورده|سوفيت|كلوك|تحبني)$")
async def _(kst):
    cmd = kst.pattern_match.group(1)
    if cmd == "كلبي":
        art = r"""
ㅤ
┈┈┈┈╱▏┈┈┈┈┈╱▔▔▔▔╲┈┈┈┈
┈┈┈┈▏▏┈┈┈┈┈▏╲▕▋▕▋▏┈┈┈
┈┈┈┈╲╲┈┈┈┈┈▏┈▏┈▔▔▔▆┈┈
┈┈┈┈┈╲▔▔▔▔▔╲╱┈╰┳┳┳╯┈┈
┈┈╱╲╱╲▏┈┈┈┈┈┈▕▔╰━╯┈┈┈
┈┈▔╲╲╱╱▔╱▔▔╲╲╲╲┈┈┈┈┈┈
┈┈┈┈╲╱╲╱┈┈┈┈╲╲▂╲▂┈┈┈┈
┈┈┈┈┈┈┈┈┈┈┈┈┈╲╱╲╱┈┈┈┈
ㅤ
"""
    elif cmd == "فكيو":
        art = """
ㅤ
⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⣴⠏⠁⠙ ⡄
⠀⠀⠀⠀⠀⠀⠀⠀   ⡾     ⠀⠀ ⢷
⠀⠀⠀⠀⠀⠀   ⠀⠀⣾  ⠀  ⠀  ⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿  ⠀⠀⠀ ⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿  ⠀⠀ ⠀⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿  ⠀⠀⠀ ⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿      ⠀⠀⣿
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⠀⠀⠀⠀⣿⡇
⠀⠀⠀⠀⠀⠀⠀⣾⠏⣿⠀⠀⠀⠀⣿⣷⣦⣄⡀
⠀⠀⠀⠀⠀⠀⣼⡿⠀⣿⠀⠀⠀⠀⣿⠇⠀⠉⢷⡀
⠀⠀⠀⠀⣠⡾⢿⠇⠀⣿⠀⠀⠀⠀⣿⡇⠀⠀⠸⡷⠤⣄⡀
⠀⠀⢠⡾⠋⣾⠀⠀⠀⣿⠀⠀⠀⠀⣿⡇⠀⠀⠀⣧⠀⠀⠹⡄
⠀⣰⠏⠀⠀⣿⠀⠀⠀⠉⠀⠀⠀⠀⠈⠁⠀⠀⠀⢹⡄⠀⠀⢹⡄
⡾⡏⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠇⠀⠀⠀⢻⡄
⡾⣿⡀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣷
⠀⠙⢿⣦⡀⠀⠀⠀⠀⠀⠀  ⠀فكيو⠀⠀⠀⠀           ⠀⢠⣿
⠀⠀⠀⠹⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟
⠀⠀⠀⠀⠈⠻⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠟
⠀⠀⠀⠀⠀⠀⠈⠻⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡿⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠏
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏
ㅤ
"""
    elif cmd == "ورده":
        art = """
ㅤ
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀
⠀⠀⠀⠀⠀⠀⠀⡠⠖⠋⠉⠉⠳⡴⠒⠒⠒⠲⠤⢤⣀
⠀⠀⠀⠀⠀⣠⠊⠀⠀⡴⠚⡩⠟⠓⠒⡖⠲⡄⠀⠀⠈⡆
⠀⠀⠀⢀⡞⠁⢠⠒⠾⢥⣀⣇⣚⣹⡤⡟⠀⡇⢠⠀⢠⠇
⠀⠀⠀⢸⣄⣀⠀⡇⠀⠀⠀⠀⠀⢀⡜⠁⣸⢠⠎⣰⣃
⠀⠀⠸⡍⠀⠉⠉⠛⠦⣄⠀⢀⡴⣫⠴⠋⢹⡏⡼⠁⠈⠙⢦⡀
⠀⠀⣀⡽⣄⠀⠀⠀⠀⠈⠙⠻⣎⡁⠀⠀⣸⡾⠀⠀⠀⠀⣀⡹⠂
⢀⡞⠁⠀⠈⢣⡀⠀⠀⠀⠀⠀⠀⠉⠓⠶⢟⠀⢀⡤⠖⠋⠁
⠀⠉⠙⠒⠦⡀⠙⠦⣀⠀⠀⠀⠀⠀⠀⢀⣴⡷⠋
⠀⠀⠀⠀⠀⠘⢦⣀⠈⠓⣦⣤⣤⣤⢶⡟⠁
⢤⣤⣤⡤⠤⠤⠤⠤⣌⡉⠉⠁⠀⢸⢸⠁⡠⠖⠒⠒⢒⣒⡶⣶⠤
⠉⠲⣍⠓⠦⣄⠀⠀⠙⣆⠀⠀⠀⡞⡼⡼⢀⣠⠴⠊⢉⡤⠚⠁
⠀⠀⠈⠳⣄⠈⠙⢦⡀⢸⡀⠀⢰⢣⡧⠷⣯⣤⠤⠚⠉
⠀⠀⠀⠀⠈⠑⣲⠤⠬⠿⠧⣠⢏⡞
⠀⠀⢀⡴⠚⠉⠉⢉⣳⣄⣠⠏⡞
⣠⣴⣟⣒⣋⣉⣉⡭⠟⢡⠏⡼
⠉⠀⠀⠀⠀⠀⠀⠀⢀⠏⣸⠁
⠀⠀⠀⠀⠀⠀⠀⠀⡞⢠⠇
⠀⠀⠀⠀⠀⠀⠀⠘⠓⠚
ㅤ
"""
    elif cmd == "سوفيت":
        art = """
ㅤ
⠀⠀⠀⠀⠀⠀⢀⣤⣀⣀⣀⠀⠻⣷⣄
⠀⠀⠀⠀⢀⣴⣿⣿⣿⡿⠋⠀⠀⠀⠹⣿⣦⡀
⠀⠀⢀⣴⣿⣿⣿⣿⣏⠀⠀⠀⠀⠀⠀⢹⣿⣧
⠀⠀⠙⢿⣿⡿⠋⠻⣿⣿⣦⡀⠀⠀⠀⢸⣿⣿⡆
⠀⠀⠀⠀⠉⠀⠀⠀⠈⠻⣿⣿⣦⡀⠀⢸⣿⣿⡇
⠀⠀⠀⠀⢀⣀⣄⡀⠀⠀⠈⠻⣿⣿⣶⣿⣿⣿⠁
⠀⠀⠀⣠⣿⣿⢿⣿⣶⣶⣶⣶⣾⣿⣿⣿⣿⡁
⢠⣶⣿⣿⠋⠀⠀⠉⠛⠿⠿⠿⠿⠿⠛⠻⣿⣿⣦⡀
⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⡿
ㅤ
"""
    elif cmd == "كلوك":
        art = """
ㅤ
⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⢀⣀⣀⣀⣀⣀⣤⣤
⠀⢶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠛⠛⠛⠛⠋⠉
⠀⠀⢹⣿⣿⣿⣿⣿⠏    ⣿   ⠀ ⢹⡟
⠀⢠⣿⣿⣿⣿⣿⣿⣦⣀⣀⣙⣂⣠⠼⠃
⠀⣾⣿⣿⣿⣿⣿⠁
⢠⣿⣿⣿⣿⣿⡟
⢸⣿⣿⣿⣿⣿⡅
⠀⠛⠛⠛⠛⠛⠃
ㅤ
"""
    elif cmd == "تحبني":
        art = """
ㅤ
⠀⠀⠀⠀⣠⣶⡾⠏⠉⠙⠳⢦⡀⠀⠀⠀⢠⠞⠉⠙⠲⡀
⠀⠀⠀⣴⠿⠏⠀⠀⠀⠀⠀⠀⢳⡀⠀⡏⠀⠀⠀⠀ ⠀⢷
⠀⠀⢠⣟⣋⡀⢀⣀⣀⡀⠀⣀⡀⣧⠀⢸⠀⠀⠀⠀ ⠀ ⡇
⠀⠀⢸⣯⡭⠁⠸⣛⣟⠆⡴⣻⡲⣿⠀⣸⠀تحبني؟   ⡇
⠀⠀⣟⣿⡭⠀⠀⠀⠀⠀⢱⠀⠀⣿⠀⢹⠀⠀⠀ ⠀⠀ ⡇
⠀⠀⠙⢿⣯⠄⠀⠀⠀⢀⡀⠀⠀⡿⠀⠀⡇⠀⠀⠀⠀⡼
⠀⠀⠀⠀⠹⣶⠆⠀⠀⠀⠀⠀⡴⠃⠀⠀⠘⠤⣄⣠⠞
⠀⠀⠀⠀⠀⢸⣷⡦⢤⡤⢤⣞⣁
⠀⠀⢀⣤⣴⣿⣏⠁⠀⠀⠸⣏⢯⣷⣖⣦⡀
⢀⣾⣽⣿⣿⣿⣿⠛⢲⣶⣾⢉⡷⣿⣿⠵⣿
⣼⣿⠍⠉⣿⡭⠉⠙⢺⣇⣼⡏⠀⠀⠀⣄⢸
⣿⣿⣧⣀⣿.........⣀⣰⣏⣘⣆⣀
ㅤ
"""
    await kst.edit(art, parse_mode=parse_pre)


@zedub.zed_cmd(pattern="(شبح|دعبل)$")
async def _(kst):
    cmd = kst.pattern_match.group(1)
    if cmd == "شبح":
        expr = """
┻┳|
┳┻| _
┻┳| •.•)  **lشبحl**
┳┻|⊂ﾉ
┻┳|
"""
    elif cmd == "دعبل":
        expr = """
○
く|)へ
    〉
 ￣￣┗┓             __lدعبل مناl__
 　 　   ┗┓　     ヾ○ｼ
  　　        ┗┓   ヘ/
 　                 ┗┓ノ
　 　 　 　 　   ┗┓
"""
    await kst.edit(expr)

