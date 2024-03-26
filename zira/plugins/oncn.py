import asyncio
from telethon import events
from telethon.tl import types, functions
from telethon.tl.types import UserStatusOnline as onn
from telethon.utils import get_display_name

from zira import zedub
from ..Config import Config
from ..utils import Zed_Vip
from ..sql_helper.globals import addgvar, gvarstatus
from ..core.managers import edit_delete, edit_or_reply
from . import BOTLOG, BOTLOG_CHATID

Zel_Uid = zedub.uid

async def get_private_chat_ids(limit=50):
    ids = []
    try:
        dialogs = await zedub.get_dialogs(limit=limit)
        for dialog in dialogs:
            if isinstance(dialog.entity, types.User):
                ids.append(dialog.entity.id)
    except Exception as e:
        async for dialog in zedub.iter_dialogs(limit=limit):
            if dialog.is_user:
                ids.append(dialog.entity.id)
    return ids

@zedub.zed_cmd(pattern="(تفعيل الكاشف الذكي|تفعيل اشعارات الحالة)")
async def start_zelzali(event):
    #if Zel_Uid not in Zed_Vip:
        #return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @S_1_02\n⎉╎او التواصـل مـع احـد المشرفيـن @S_1_02**")
    ZAZ = not gvarstatus("ZAZ") or gvarstatus("ZAZ") != "false"
    if ZAZ:
        privacy_settings = types.InputPrivacyValueAllowAll()
        privacy_key = types.InputPrivacyKeyStatusTimestamp()
        await zedub(functions.account.SetPrivacyRequest(key=privacy_key, rules=[privacy_settings]))
        await asyncio.sleep(2)
        await edit_or_reply(event, "**⎉╎إشعـارات الحالـة (متصـل) .. مفعـله مسبقـاً ☑️**")
    else:
        privacy_settings = types.InputPrivacyValueAllowAll()
        privacy_key = types.InputPrivacyKeyStatusTimestamp()
        await zedub(functions.account.SetPrivacyRequest(key=privacy_key, rules=[privacy_settings]))
        await asyncio.sleep(2)
        addgvar("ZAZ", True)
        await edit_or_reply(event, "**⎉╎تم تفعيـل إشعـارات الحالـة (متصـل) .. بنجـاح ☑️**")

@zedub.zed_cmd(pattern="(تعطيل الكاشف الذكي|تعطيل اشعارات الحالة)")
async def stop_zelzali(event):
    #if Zel_Uid not in Zed_Vip:
        #return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @S_1_02\n⎉╎او التواصـل مـع احـد المشرفيـن @S_1_02**")
    ZAZ = not gvarstatus("ZAZ") or gvarstatus("ZAZ") != "false"
    if ZAZ:
        addgvar("ZAZ", False)
        await edit_or_reply(event, "**⎉╎تم تعطيـل إشعـارات الحالـة (متصـل) .. بنجـاح ☑️**")
    else:
        await edit_or_reply(event, "**⎉╎إشعـارات الحالـة (متصـل) .. معطلـه مسبقـاً ☑️**")

@zedub.on(events.UserUpdate)
async def zelzal_online_ai(event):
    #if Zel_Uid not in Zed_Vip:
        #return
    if gvarstatus("ZAZ") and gvarstatus("ZAZ") == "false":
        return
    if gvarstatus("ZAZ") is None:
        return
    private_chat_ids = await get_private_chat_ids(limit=50)
    if event.user_id in private_chat_ids and event.user_id != zedub.uid:
        if event.online:
            user = await event.get_user()
            first_name = user.first_name
            last_name = user.last_name
            full_name = f"{user.first_name}{user.last_name}"
            full_name = full_name if last_name else first_name
            if BOTLOG:
                zaz = f"<b>⌔┊الحسـاب : </b>" 
                zaz += f'<a href="tg://user?id={user.id}">{full_name}</a>'
                zaz += f"\n<b>⌔┊اصبـح متصـل الان ⦿</b>"
                await zedub.send_message(Config.PM_LOGGER_GROUP_ID, zaz, parse_mode="html")
                    #f"<b>⌔┊الحسـاب :</b> <a href='tg://user?id={user.id}'>{full_name}</a>\n<b>⌔┊اصبـح متصـل الان ⦿</b>",
                #)


@zedub.zed_cmd(pattern="المتصليين?(.*)")
async def _(e):
    if e.is_private:
        return await edit_or_reply(e, "**- عـذراً ... هـذه ليـست مجمـوعـة ؟!**")
    if Zel_Uid not in Zed_Vip:
        return await edit_or_reply(e, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @S_1_02\n⎉╎او التواصـل مـع احـد المشرفيـن @S_1_02**")
    chat = await e.get_chat()
    if not chat.admin_rights and not chat.creator:
        await edit_or_reply(e, "**- عـذراً ... يجب ان تكـون مشرفـاً هنـا ؟!**")
        return False
    zel = await edit_or_reply(e, "**- جـارِ الكشـف اونـلايـن ...**")
    zzz = e.pattern_match.group(1)
    o = 0
    zilzali = "𓆩 [𝗦𝗼𝘂𝗿𝗰𝗲 𝐋𝐈𝐓𝐇𝐎𝐍 - 🝢 - الڪـٓاشـف الذڪـٓي](t.me/A1DIIU) 𓆪\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n**- تـم انتهـاء الكشـف .. بنجـاح ✅**\n**- قائمـة بعـدد الاعضـاء المتصليـن واسمائـهـم :**\n"
    xx = f"{zzz}" if zzz else zilzali
    zed = await e.client.get_participants(e.chat_id, limit=99)
    for users, bb in enumerate(zed):
        x = bb.status
        y = bb.participant
        if isinstance(x, onn):
            o += 1
            xx += f"\n- [{get_display_name(bb)}](tg://user?id={bb.id})"
    await e.client.send_message(e.chat_id, xx)
    await zel.delete()


ZelzalVip_Orders = (
"[ᯓ 𝐋𝐈𝐓𝐇𝐎𝐍 𝗩𝗶𝗽 🌟 الاوامــر المـدفـوعـة](t.me/A1DIIU) .\n"
"⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
"**✾╎قـائمـة الاوامـر المـدفـوعـة الخاصـة بسـورس ليثون :** \n\n"
"`.هاك`\n"
"**⪼ لـ عـرض اوامـر الاختـراق عبـر كـود تيرمكـس ☠**\n"
"**⪼ الاختـراق يدعـم كود تليثـون او بايروجـرام معـاً 🏌‍♂**\n\n\n"
"`.تفعيل الكاشف الذكي`\n"
"**⪼ لـ تفعيـل إشعـارات كشـف المتصليـن الموجـوديـن خـاص لـديـك 🛜**\n\n\n"
"`.تعطيل الكاشف الذكي`\n"
"**⪼ لـ تعطيـل إشعـارات كشـف المتصليـن الموجـوديـن خـاص لـديـك 🛃**\n\n\n"
"`.موقع`\n"
"**⪼ ارسـل الامـر (.موقع + الدولة + المحافظة/المدينة + اسم محل خدمي او تجاري)**\n"
"**⪼ مثــال (.موقع العراق بغداد المنصور مطعم الساعة)**\n"
"**⪼ لـ جـلب صـورة مباشـرة لـ الموقـع عبـر الاقمـار الصنـاعيـة 🗺🛰**\n\n\n"
"`.اتصل`\n"
"**⪼ ارسـل الامـر (.اتصل + رقـم الهاتـف)**\n"
"**⪼ لـ عمـل سبـام اتصـال لـ اي هاتـف مـن رقـم اجنبـي 📲**\n\n\n"
"**⪼ ملاحظــه هامــه 💡:**\n"
"راح يتـم اضافـة المزيـد مـن الاوامـر المدفوعـة بالتحديثـات القادمـه كـل فتـره\n"
"مـع زدثــون راح تجربـون اوامـر مو موجـودة عنـد حـدا 🏌‍♂\n"
"حتى الاجـانب يحلمـون يوصلـون لهـا ⛹🏻‍♀\n\n"
"𓆩 [𝐋𝐈𝐓𝐇𝐎𝐍 𝗩𝗶𝗽 🌟](t.me/A1DIIU) 𓆪"
)

@zedub.zed_cmd(pattern="المميز$")
async def sbyshal(zzzvip):
    if Zel_Uid not in Zed_Vip:
        return await edit_or_reply(event, "**⎉╎عـذࢪاً .. ؏ـزيـزي\n⎉╎هـذا الامـر ليـس مجـانـي📵\n⎉╎للاشتـراك في الاوامـر المدفوعـة\n⎉╎تواصـل مطـور السـورس @S_1_02\n⎉╎او التواصـل مـع احـد المشرفيـن @S_1_02**")
    return await edit_or_reply(zzzvip, ZelzalVip_Orders)


ZelzalViip_Orders = (
"[ᯓ 𝐋𝐈𝐓𝐇𝐎𝐍 𝗩𝗶𝗽 🌟 الاوامــر المميـزة](t.me/A1DIIU) .\n"
"⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n"
"**✾╎قـائمـة اثنين من الاوامـر المميـزة الخاصـة بسـورس ليثون :** \n\n"
"`.تفعيل الكاشف الذكي`\n"
"**⪼ لـ تفعيـل إشعـارات كشـف المتصليـن الموجـوديـن خـاص لـديـك 🛜**\n\n\n"
"`.تعطيل الكاشف الذكي`\n"
"**⪼ لـ تعطيـل إشعـارات كشـف المتصليـن الموجـوديـن خـاص لـديـك 🛃**\n\n\n"
"`.اتصل`\n"
"**⪼ ارسـل الامـر (.اتصل + رقـم الهاتـف)**\n"
"**⪼ لـ عمـل سبـام اتصـال لـ اي هاتـف مـن رقـم اجنبـي 📲**\n\n\n"
"**⪼ ملاحظــه هامــه 💡:**\n"
"هذه اثنين اوامر مدفوعة من اصل 5 اوامر\n"
"تم فتحها للجميع لمدة محدودة فقط (شهر) وسوف تصبح مدفوعة مرة اخرى بعد انتهاء المدة المحددة\n\n"
"𓆩 [𝐋𝐈𝐓𝐇𝐎𝐍 𝗩𝗶𝗽 🌟](t.me/A1DIIU) 𓆪"
)

@zedub.zed_cmd(pattern="vip$")
async def sbyshaal(zzzviip):
    return await edit_or_reply(zzzviip, ZelzalViip_Orders)
