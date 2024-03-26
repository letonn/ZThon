import requests
import asyncio
import random
import os
import sys
import html
import urllib.request
from datetime import datetime, timedelta
from time import sleep

try:
    import unicodedata
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    os.system("pip3 install unicodedata bs4")
    import unicodedata
    from bs4 import BeautifulSoup

from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import Channel, Chat, InputPhoto, User, InputMessagesFilterEmpty

from telethon import events
from telethon.errors import FloodWaitError
from telethon.tl.functions.messages import GetHistoryRequest, ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.tl.functions.messages import ImportChatInviteRequest as Get

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _zedutils, reply_id
from ..sql_helper.globals import gvarstatus
from . import ALIVE_NAME, BOTLOG, BOTLOG_CHATID, zedub, edit_delete, get_user_from_event

LOGS = logging.getLogger(__name__)
ANTHAL = gvarstatus("ANTHAL") or "(ايقاف الانتحال|اعادة|اعاده)"
# =========================================================== #
#                                                             𝙕𝙏𝙝𝙤𝙣
# =========================================================== #
WW_CHANGED = "**⎉╎جـارِ الانتحـال . . .**"
ZZ_CHANGED = "**⎉╎تم انتحـال الشخص .. بنجـاح 🥷**"
# =========================================================== #
#                                                             𝙕𝙏𝙝𝙤𝙣
# =========================================================== #

@zedub.zed_cmd(pattern="انتحال(?:\s|$)([\s\S]*)")
async def _(event):
    replied_user, error_i_a = await get_user_from_event(event)
    if replied_user is None:
        return
    zzz = await edit_or_reply(event, WW_CHANGED)
    user_id = replied_user.id
    profile_pic = await event.client.download_profile_photo(user_id, Config.TEMP_DIR)
    first_name = html.escape(replied_user.first_name)
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.last_name
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
        last_name = "⁪⁬⁮⁮⁮⁮ ‌‌‌‌"
    replied_user = (await event.client(GetFullUserRequest(replied_user.id))).full_user
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = replied_user.about
    await event.client(functions.account.UpdateProfileRequest(first_name=first_name))
    await event.client(functions.account.UpdateProfileRequest(last_name=last_name))
    await event.client(functions.account.UpdateProfileRequest(about=user_bio))
    try:
        pfile = await event.client.upload_file(profile_pic)
    except Exception as e:
        return await edit_delete(event, f"**اووبس خطـأ بالانتحـال:**\n__{e}__")
    if profile_pic.endswith((".mp4", ".MP4")):
        size = os.stat(profile_pic).st_size
        if size > 2097152:
            await zzz.edit("⎉╎يجب ان يكون الحجم اقل من 2 ميغا ✅")
            os.remove(profile_pic)
            return
        zpic = None
        zvideo = await event.client.upload_file(profile_pic)
    else:
        zpic = await event.client.upload_file(profile_pic)
        zvideo = None
    try:
        await event.client(
            functions.photos.UploadProfilePhotoRequest(
                file=zpic, video=zvideo, video_start_ts=0.01
            )
        )
    except Exception as e:
        await zzz.edit(f"**خطأ:**\n`{str(e)}`")
    await edit_or_reply(zzz, ZZ_CHANGED)
    try:
        os.remove(profile_pic)
    except Exception as e:
        LOGS.info(str(e))
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#الانتحـــال\n**⪼ تم انتحـال حسـاب الشخـص ↫** [{first_name}](tg://user?id={user_id }) **بنجاح ✅**\n**⪼ لـ الغـاء الانتحـال ارسـل** ( `.اعاده` )",
        )


@zedub.zed_cmd(pattern=f"{ANTHAL}$")
async def revert(event):
    firstname = gvarstatus("FIRST_NAME") or ALIVE_NAME
    lastname = gvarstatus("LAST_NAME") or ""
    bio = gvarstatus("DEFAULT_BIO") or "{وَتَوَكَّلْ عَلَى اللَّهِ ۚ وَكَفَىٰ بِاللَّهِ وَكِيلًا}"
    await event.client(
        functions.photos.DeletePhotosRequest(
            await event.client.get_profile_photos("me", limit=1)
        )
    )
    await event.client(functions.account.UpdateProfileRequest(about=bio))
    await event.client(functions.account.UpdateProfileRequest(first_name=firstname))
    await event.client(functions.account.UpdateProfileRequest(last_name=lastname))
    await edit_delete(event, "**⎉╎تمت اعادة الحساب لوضعـه الاصلـي \n⎉╎والغـاء الانتحـال .. بنجـاح ✅**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#الغـاء_الانتحـال\n**⪼ تم الغـاء الانتحـال .. بنجـاح ✅**\n**⪼ تم إعـاده معلـوماتك الى وضعـها الاصـلي**",
        )

# ================================================================================================ #
# =========================================الازعاج================================================= #
# ================================================================================================ #

@zedub.zed_cmd(pattern="مزاد(?: |$)(.*)")
async def _(event):
    reply = await event.get_reply_message()
    args = event.pattern_match.group(1)
    if not reply and not args:
        return
    if reply and not args:
        bot_token = reply.text
    else:
        bot_token = args
    if bot_token.startswith("@"):
        bot_token = bot_token.replace("@", "")
    chat = "@GetUsernameBot" #Code by T.me/zzzzl1l
    zed = await edit_or_reply(event, "**╮ جـارِ الكشـف عـن اليـوزر فـي المـزاد ...𓅫╰**")
    async with borg.conversation(chat) as conv: #Code by T.me/zzzzl1l
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(bot_token) #Code by T.me/zzzzl1l
            await asyncio.sleep(5)
            zedthon = await conv.get_response()
            await zed.delete()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=f"<b>⎉╎اليـوزر -->  @{bot_token}\n⎉╎رابـط اليـوزر ع المـزاد :  <a href = https://fragment.com/username/{bot_token}/1>اضغـط هنـا</a>\n⎉╎تم الكشف بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>",
                parse_mode="html",
            )
        except YouBlockedUserError: #Code by T.me/zzzzl1l
            await zedub(unblock("GetUsernameBot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(bot_token)
            await asyncio.sleep(5)
            zedthon = await conv.get_response()
            await zed.delete()
            await borg.send_file(
                event.chat_id,
                zedthon,
                caption=f"<b>⎉╎اليـوزر -->  @{bot_token}\n⎉╎رابـط اليـوزر ع المـزاد :  <a href = https://fragment.com/username/{bot_token}/1>اضغـط هنـا</a>\n⎉╎تم الكشف بواسطـة <a href = https://t.me/A1DIIU/1>𝐋𝐈𝐓𝐇𝐎𝐍</a> </b>",
                parse_mode="html",
            )



def get_tiktok_user_info(username):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
    r = requests.get(f"https://www.tiktok.com/@{username}", headers=headers)
    server_log = str(r.text)

    try:
        soup = BeautifulSoup(server_log, 'html.parser')
        script = soup.find(id='SIGI_STATE').contents
        data = str(script).split('},"UserModule":{"users":{')[1]
        
        user_info = {}
        user_info['user_id'] = data.split('"id":"')[1].split('",')[0]
        user_info['name'] = data.split(',"nickname":"')[1].split('",')[0]
        user_info['followers'] = data.split('"followerCount":')[1].split(',')[0]
        user_info['following'] = data.split('"followingCount":')[1].split(',')[0]
        user_info['user_create_time'] = user_create_time(int(user_info['user_id']))
        user_info['last_change_name'] = datetime.fromtimestamp(int(data.split('"nickNameModifyTime":')[1].split(',')[0]))
        user_info['account_region'] = data.split('"region":"')[1].split('"')[0]
        
        return user_info
    except IndexError:
        return None


def user_create_time(url_id):
    binary = "{0:b}".format(url_id)
    i = 0
    bits = ""
    while i < 31:
        bits += binary[i]
        i += 1
    timestamp = int(bits, 2)
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object


#Code by T.me/zzzzl1l
@zedub.zed_cmd(pattern="tt(?: |$)([\s\S]*)")
async def zelzal_gif(event):
    username = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not username and reply:
        username = reply.text
    if not username:
        return await edit_delete(event, "**- ارسـل (.tt) + يـوزر تيـك تـوك او بالـرد ع يـوزر تيـك تـوك**", 10)
    if username.startswith("@"):
        username = username.replace("@", "")
    zed = await edit_or_reply(event, "**⎉╎جـارِ جلب معلومـات TikTok .. انتظر قليلا ▬▭**")
    data = get_tiktok_user_info(username)
    if data:
        id = data['user_id']
        name = data['name']
        followers = data['followers']
        following = data['following']
        time = data['user_create_time']
        last = data['last_change_name']
        acc = data['account_region']
        country_emoji = unicodedata.lookup(f"REGIONAL INDICATOR SYMBOL LETTER {acc[0]}")
        country_emoji += unicodedata.lookup(f"REGIONAL INDICATOR SYMBOL LETTER {acc[1]}")
        zzz = f"𓆩 𝐋𝐈𝐓𝐇𝐎𝐍 𝗧𝗶𝗸𝗧𝗼𝗸 𝗜𝗻𝗳𝗼 - **معلومـات تيـك تـوك** 𓆪\n⋆─┄─┄─┄─┄─┄─┄─┄┄─┄─⋆\n**• الاسـم :** {name}\n**• اليـوزر :** {username}\n**• الايـدي :** {id}\n**• المتابعـين :** {followers}\n**• يتابـع :** {following}\n**• الدولـة :** {acc} {country_emoji}\n**• تاريـخ إنشـاء الحسـاب :** {time}"
        pic_z = f"https://graph.org/file/dd383bc88dc1ce1a1971c.jpg"
        try:
            await event.client.send_file(
                event.chat_id,
                pic_z,
                caption=zzz
            )
            await zed.delete()
        except ChatSendMediaForbiddenError as err:
            await edit_or_reply(zed, f"𓆩 𝐋𝐈𝐓𝐇𝐎𝐍 𝗧𝗶𝗸𝗧𝗼𝗸 𝗜𝗻𝗳𝗼 - **معلومـات تيـك تـوك** 𓆪\n⋆─┄─┄─┄─┄─┄─┄─┄┄─┄─⋆\n**• الاسـم :** {name}\n**• اليـوزر :** {username}\n**• الايـدي :** {id}\n**• المتابعـين :** {followers}\n**• يتابـع :** {following}\n**• الدولـة :** {acc} {country_emoji}\n**• تاريـخ إنشـاء الحسـاب :** {time}")
            await zed.delete()
    else:
        await zed.edit("**- لم استطـع الكشـف عـن الحسـاب او ان اليـوزر غيـر موجـود**")


@zedub.zed_cmd(pattern="nn(?: |$)(.*)")
async def zelzal_gif(event):
    zelzal = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not zelzal and reply:
        zelzal = reply.text
    if not zelzal:
        return await edit_delete(event, "**- ارسـل (.nn) + يـوزر انستـا او بالـرد ع يـوزر انستـا**", 10)
    if zelzal.startswith("@"):
        zelzal = zelzal.replace("@", "")
    zed = await edit_or_reply(event, "**⎉╎جـارِ جلب معلومـات الانستـا .. انتظر قليلا ▬▭**")
    chat = "@instagram_information_users_bot" # Code by T.me/zzzzl1l
    async with borg.conversation(chat) as conv: # Code by T.me/zzzzl1l
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(zelzal)
            await asyncio.sleep(3)
            zedthon = await conv.get_response()
            malath = zedthon.text
            if "Username : " in zedthon.text: # Code by T.me/zzzzl1l
                zzz = malath.replace("Username : `username`", f"**• اليـوزر :** `{zelzal}`").replace("Name : ", "**• الاسـم :** ").replace("ID : ", "**• الايـدي :** ").replace("Bio : ", "**• البايـو :** ").replace("Posts : ", "**• المنشـورات :** ").replace("Followers : ", "**• المتابعيـن :** ").replace("Following : ", "**• المتابعهـم :** ").replace("\n\n", "\n")
                zz = f"𓆩 𝐋𝐈𝐓𝐇𝐎𝐍 𝗜𝗻𝘀𝘁𝗮 𝗜𝗻𝗳𝗼 - **معلومـات انستـا** 𓆪\n⋆─┄─┄─┄─┄─┄─┄─┄┄─┄─⋆\n{zzz}"
                try:
                    await borg.send_file(
                        event.chat_id,
                        zedthon,
                        caption=zz,
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError as err:
                    await borg.send_message(event.chat_id, zz)
                    await zed.delete()
            else:
                await zed.edit("**- لم استطـع الكشـف عـن الحسـاب او ان اليـوزر غيـر موجـود**")
        except YouBlockedUserError: #Code by T.me/zzzzl1l
            await zedub(unblock("instagram_information_users_bot"))
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message(zelzal)
            await asyncio.sleep(3)
            zedthon = await conv.get_response()
            malath = zedthon.text
            if "Username : " in zedthon.text: # Code by T.me/zzzzl1l
                zzz = malath.replace("Username : `username`", f"**• اليـوزر :** `{zelzal}`").replace("Name : ", "**• الاسـم :** ").replace("ID : ", "**• الايـدي :** ").replace("Bio : ", "**• البايـو :** ").replace("Posts : ", "**• المنشـورات :** ").replace("Followers : ", "**• المتابعيـن :** ").replace("Following : ", "**• المتابعهـم :** ").replace("\n\n", "\n")
                zz = f"𓆩 𝐋𝐈𝐓𝐇𝐎𝐍 𝗜𝗻𝘀𝘁𝗮 𝗜𝗻𝗳𝗼 - **معلومـات انستـا** 𓆪\n⋆─┄─┄─┄─┄─┄─┄─┄┄─┄─⋆\n{zzz}"
                try:
                    await borg.send_file(
                        event.chat_id,
                        zedthon,
                        caption=zz,
                    )
                    await zed.delete()
                except ChatSendMediaForbiddenError as err:
                    await borg.send_message(event.chat_id, zz)
                    await zed.delete()
            else:
                await zed.edit("**- لم استطـع الكشـف عـن الحسـاب او ان اليـوزر غيـر موجـود**")
