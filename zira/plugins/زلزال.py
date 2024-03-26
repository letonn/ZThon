import requests
import asyncio
import os
import sys
import urllib.request
from datetime import timedelta
from telethon import events
from telethon.errors import FloodWaitError
from telethon.tl.functions.messages import GetHistoryRequest, ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from . import zedub
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id


@zedub.zed_cmd(pattern="اغنيه(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    d_link = event.pattern_match.group(1)
    if ".com" not in d_link:
        await event.edit("**╮ جـارِ البحث ؏ـن الاغنيـٓه... 🎧♥️╰**")
    else:
        await event.edit("**╮ جـارِ البحث ؏ـن الاغنيـٓه... 🎧♥️╰**")
    chat = "@Abm_MusicDownloader_Bot"
    async with borg.conversation(chat) as conv: # code by t.me/S_1_02
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(d_link)
            await conv.get_response()
            await asyncio.sleep(5)
            zira = await conv.get_response()
            if "⏳" not in zira.text:
                await zira.click(0)
                await asyncio.sleep(5)
                zira = await conv.get_response()
                await event.delete()
                await borg.send_file(
                    event.chat_id,
                    zira,
                    caption=f"**❈╎البحـث :** `{d_link}`",
                )

            else:
                await event.edit("**- لـم استطـع العثـور على نتائـج ؟!**\n**- حـاول مجـدداً في وقت لاحـق ...**")
        except YouBlockedUserError:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(d_link)
            await conv.get_response()
            await asyncio.sleep(5)
            zira = await conv.get_response()
            zira = await conv.get_response()
            if "⏳" not in zira.text:
                await zira.click(0)
                await asyncio.sleep(5)
                zira = await conv.get_response()
                await event.delete()
                await borg.send_file(
                    event.chat_id,
                    zira,
                    caption=f"**❈╎البحـث :** `{d_link}`",
                )

            else:
                await event.edit("**- لـم استطـع العثـور على نتائـج ؟!**\n**- حـاول مجـدداً في وقت لاحـق ...**")



#الملـف كتابـة زلـزال الهيبـه ⤶ @S_1_02 خاص بسـورس ⤶ 𝐋𝐈𝐓𝐇𝐎𝐍
#الملف متعوب عليه So تخمط وماتذكـر المصـدر == اهينـك
#ها خماط رمضان وتخمط hhhhhhh
@zedub.zed_cmd(pattern="تطبيق(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        d_link = reply.text
    else:
        return await event.edit("**⎉╎قم بكتـابة رابـط + اسـم التطبيـق اولاً ...**\n**⎉╎او ارسـل .تطبيق بالـرد ع رابـط التطبيـق ...**")
    if "preview" in d_link or "google" in d_link:
        await event.edit("**⎉╎جـارِ تحميـل التطبيق ...**")
    else:
        return
    chat = "@apkdl_bot"
    async with borg.conversation(chat) as conv: # code by t.me/S_1_02
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(d_link)
            await asyncio.sleep(3)
            zira = await conv.get_response()
            if "Version:" in zira.text:
                await zira.click(text='Download')
                await asyncio.sleep(5)
                zira = await conv.get_response()
                zilzal = zira.text
                if "above 50MB" in zira.text:
                    aa = zilzal.replace(".apk filesize is above 50MB so you can download only using link", "**- حجم التطبيق اكبر من 50MB ؟!\n- قم بتحميل التطبيق عبـر البوت\n- ادخل للبوت @uploadbot وارسل الرابـط بالاسفـل**\n\n") 
                    zz = aa.replace(" if you still want it as file copy the link and send to @UploadBot", "\n\n**- قنـاة السـورس : @A1DIIU**") 
                    await event.delete()
                    return await borg.send_message(event.chat_id, zz)
                await event.delete()
                await borg.send_file(
                    event.chat_id,
                    zira,
                    caption=f"**{zira.text}\nBy: @A1DIIU**",
                )

            else:
                await event.edit("**- لـم استطـع العثـور على نتائـج ؟!**\n**- حـاول مجـدداً في وقت لاحـق ...**")
        except YouBlockedUserError:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(d_link)
            await asyncio.sleep(3)
            zira = await conv.get_response()
            if "Version:" in zira.text:
                await zira.click(text='Download')
                await asyncio.sleep(5)
                zira = await conv.get_response()
                zilzal = zira.text
                if "above 50MB" in zira.text:
                    aa = zilzal.replace(".apk filesize is above 50MB so you can download only using link", "**- حجم التطبيق اكبر من 50MB ؟!\n- قم بتحميل التطبيق عبـر البوت\n- ادخل للبوت @uploadbot وارسل الرابـط بالاسفـل**\n\n") 
                    zz = aa.replace(" if you still want it as file copy the link and send to @UploadBot", "\n\n**- قنـاة السـورس : @A1DIIU**") 
                    await event.delete()
                    return await borg.send_message(event.chat_id, zz)
                await event.delete()
                await borg.send_file(
                    event.chat_id,
                    zira,
                    caption=f"**{zira.text}\nBy: @A1DIIU**",
                )

            else:
                await event.edit("**- لـم استطـع العثـور على نتائـج ؟!**\n**- حـاول مجـدداً في وقت لاحـق ...**")



@zedub.zed_cmd(pattern="رابط(?:\s|$)([\s\S]*)")
async def linkapk(event):
    input_str = event.pattern_match.group(1)
    if input_str == "الحذف":
        return
    chat = "@apkdl_bot" # code by t.me/S_1_02
    reply_id_ = await reply_id(event)
    zed = await edit_or_reply(event, "**⎉╎جـارِ البحث عن روابـط التطبيق ...**")
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message(input_str)
        except YouBlockedUserError:
            await zedub(unblock("apkdl_bot"))
            await conv.send_message(input_str)
        await asyncio.sleep(5)
        response = await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        await event.client.send_message(event.chat_id, f"**- قم بالضغـط ع اول رابـط يبـدأ ب /preview\n- ثم ارسـل .تطبيق بالـرد ع الرابـط**\n\n{response.message}")
        await zed.delete()



@zedub.zed_cmd(pattern="فلم ([\s\S]*)")
async def zed(event):
    if event.fwd_from:
        return
    zedr = event.pattern_match.group(1)
    zira = "@TGFilmBot"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(zira, zedr)
    await tap[0].click(event.chat_id)
    await event.delete()
