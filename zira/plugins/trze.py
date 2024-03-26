from googletrans import LANGUAGES, Translator
from telethon import events, functions, types
from zira import zedub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions.functions import getTranslate
from ..sql_helper.globals import addgvar, gvarstatus
from ..sql_helper.tede_chatbot_sql import is_tede, rem_tede, set_tede
from . import BOTLOG, BOTLOG_CHATID, deEmojify

ZzTRT_cmd = (
"[ᯓ 𝗦𝗼𝘂𝗿𝗰𝗲 𝐋𝐈𝐓𝐇𝐎𝐍 🌐 اوامـر الترجمــه](t.me/A1DIIU) .\n"
"**⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆**\n"
"**✾╎قـائمـة اوامــر الترجمــة الخاصـه بسـورس ليثون :** \n\n"
" `.عربي`\n"
" `.انكلش`\n"
" `.روسي`\n"
" `.فرنسي`\n"
" `.اسباني`\n"
" `.ايطالي`\n"
" `.تركي`\n"
" `.الماني`\n"
" `.برتغالي`\n"
" `.سويدي`\n"
" `.اوكراني`\n"
" `.صيني`\n"
" `.ياباني`\n"
" `.كوري`\n"
" `.افريقي`\n"
" `.فارسي`\n"
" `.عبري`\n"
" `.اوزبكي`\n"
" `.هندي`\n"
" `.اندنوسي`\n"
" `.صومالي`\n"
" `.صربي`\n"
" `.لاتيني`\n"
" `.اوردي`\n"
"**⪼ لـ الترجمـه مـن اي لغـه الـى اللغـه المحـدده بالـرد ع نـص بالامـر**\n\n\n"
"**✾╎قـائمـة اوامــر الترجمــة التلقائيــة الذكيــة الخاصـه بسـورس ليثون :** \n\n"
" `.تفعيل الترجمه عربي`\n"
" `.تفعيل الترجمه انكلش`\n"
" `.تفعيل الترجمه روسي`\n"
" `.تفعيل الترجمه فرنسي`\n"
" `.تفعيل الترجمه اسباني`\n"
" `.تفعيل الترجمه ايطالي`\n"
" `.تفعيل الترجمه تركي`\n"
" `.تفعيل الترجمه الماني`\n"
" `.تفعيل الترجمه برتغالي`\n"
" `.تفعيل الترجمه سويدي`\n"
" `.تفعيل الترجمه اوكراني`\n"
" `.تفعيل الترجمه صيني`\n"
" `.تفعيل الترجمه ياباني`\n"
" `.تفعيل الترجمه كوري`\n"
" `.تفعيل الترجمه افريقي`\n"
" `.تفعيل الترجمه فارسي`\n"
" `.تفعيل الترجمه عبري`\n"
" `.تفعيل الترجمه اوزبكي`\n"
" `.تفعيل الترجمه هندي`\n"
" `.تفعيل الترجمه اندنوسي`\n"
" `.تفعيل الترجمه صومالي`\n"
" `.تفعيل الترجمه صربي`\n"
" `.تفعيل الترجمه لاتيني`\n"
" `.تفعيل الترجمه اوردي`\n"
"**⪼ لـ تفعيـل الترجمـه التلقـائيـه الذكيـه لـ دردشـه معينـه ✔️**\n\n"
" `.تعطيل الترجمه`\n"
"**⪼ لـ تعطيـل الترجمـه التلقـائيـه الذكيـه وايقافهـا ✖️**\n"
)

@zedub.zed_cmd(pattern="(ترجمه|الترجمه)")
async def trt(zelzallll):
    await edit_or_reply(zelzallll, ZzTRT_cmd)

# Write Code By T.me/zzzzl1l
@zedub.zed_cmd(pattern="(عربي|انكلش|فرنسي|الماني|روسي|اسباني|مكسيكي|ارجنتيني|تركي|برتغالي|برازيلي|افريقي|فارسي|ايراني|عبري|هندي|اندنوسي|ايطالي|ياباني|كوري|صيني|صومالي|صربي|لاتيني|سويدي|اوكراني|اوردي|اوزبكي)$")
async def _(event):
    input_str = event.pattern_match.group(1)
    if input_str == "عربي":
        lan = "ar"
    elif input_str == "انكلش":
        lan = "en"
    elif input_str == "فرنسي":
        lan = "fr"
    elif input_str == "تركي":
        lan = "tr"
    elif input_str == "روسي":
        lan = "ru"
    elif input_str == "اسباني" or input_str == "مكسيكي" or input_str == "ارجنتيني":
        lan = "es"
    elif input_str == "برتغالي" or input_str == "برازيلي":
        lan = "pt"
    elif input_str == "افريقي":
        lan = "af"
    elif input_str == "الماني":
        lan = "de"
    elif input_str == "فارسي":
        lan = "fa"
    elif input_str == "عبري":
        lan = "he"
    elif input_str == "هندي":
        lan = "hi"
    elif input_str == "اندنوسي":
        lan = "id"
    elif input_str == "ايطالي":
        lan = "it"
    elif input_str == "ياباني":
        lan = "ja"
    elif input_str == "صيني":
        lan = "zh-cn"
    elif input_str == "كوري":
        lan = "ko"
    elif input_str == "صومالي":
        lan = "so"
    elif input_str == "صربي":
        lan = "sr"
    elif input_str == "لاتيني":
        lan = "la"
    elif input_str == "سويدي":
        lan = "sv"
    elif input_str == "اوكراني":
        lan = "uk"
    elif input_str == "اوردي":
        lan = "ur"
    elif input_str == "اوزبكي":
        lan = "uz"
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
    else:
        return await edit_delete(event, "**- قم بالـرد ع كلمـة او نـص لكي اقـوم بترجمتهـا**", time=5)
    text = text.strip()
    translator = Translator()
    try:
        translated = translator.translate(text, dest=lan)
        after_tr_text = translated.text
        output_str = f"**- تمت الترجمـه مـن {LANGUAGES[translated.src].title()} الـى {LANGUAGES[lan].title()}**\
                \n\n`{after_tr_text}`"
        await edit_or_reply(event, output_str)
    except Exception as exc:
        await edit_delete(event, f"**- خطـأ :**\n`{exc}`", time=5)


@zedub.zed_cmd(pattern="تفعيل الترجمه(?: |$)(.*)")
async def trt_on(event):
    input_str = event.pattern_match.group(1)
    chat_id = event.chat_id
    variable = "TRT"
    zed = await edit_or_reply(event, "**⎉╎جـارِ إعـداد الترجمـه التلقائيـه ...**")
    if input_str == "انكلش" or input_str == "انجلش" or input_str == "انقلش" or input_str == "انكليزي" or input_str == "انجليزي" or input_str == "امريكا" or input_str == "كندي":
        vinfo = "en"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "فرنسي":
        vinfo = "fr"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "تركي":
        vinfo = "tr"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "روسي":
        vinfo = "ru"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "اسباني" or input_str == "مكسيكي" or input_str == "ارجنتيني":
        vinfo = "es"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "البرتغال" or input_str == "البرازيل" or input_str == "برتغالي" or input_str == "برازيلي":
        vinfo = "pt"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "افريقي" or input_str == "افريقيه" or input_str == "افريقيا":
        vinfo = "af"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "الماني" or input_str == "الالمانيه" or input_str == "المانيا":
        vinfo = "de"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "الفارسية" or input_str == "الفارسيه" or input_str == "فارسي" or input_str == "ايران":
        vinfo = "fa"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "العبرية" or input_str == "العبريه" or input_str == "عبري":
        vinfo = "he"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "هندي" or input_str == "الهنديه" or input_str == "الهند":
        vinfo = "hi"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "اندنوسي" or input_str == "الاندنوسيه" or input_str == "اندنوسيا":
        vinfo = "id"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "ايطالي" or input_str == "الايطالية" or input_str == "ايطاليا":
        vinfo = "it"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "ياباني" or input_str == "اليابانيه" or input_str == "اليابان":
        vinfo = "ja"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "صيني" or input_str == "الصينيه" or input_str == "الصين":
        vinfo = "zh-cn"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "كوري" or input_str == "الكوريه" or input_str == "كوريا":
        vinfo = "ko"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "صومالي" or input_str == "الصوماليه" or input_str == "الصومال":
        vinfo = "so"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "صربي" or input_str == "الصربيه" or input_str == "صربيا":
        vinfo = "sr"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "لاتيني" or input_str == "اللاتينيه" or input_str == "لاتينيه":
        vinfo = "la"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "السويديه" or input_str == "سويدي" or input_str == "السويد":
        vinfo = "sv"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "اوكراني" or input_str == "الاوكرانيه" or input_str == "اوكرانيا":
        vinfo = "uk"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "اوردو":
        vinfo = "ur"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)
    elif input_str == "اوزبكي" or input_str == "اوزبكيه" or input_str == "اوزبكية":
        vinfo = "uz"
        addgvar(variable, vinfo)
        await zed.edit("**⎉╎تم تفعيـل الترجمـة التلقائيـة هنـا .. بنجـاح ☑️**\n**⎉╎اللغـه {} 🌐**\n**⎉╎قم بالتحدث بالعربيـه وسـوف اقـوم بالترجمـه التلقائيـه عنـك**".format(input_str))
        set_tede(chat_id)


@zedub.zed_cmd(pattern="تعطيل الترجمه$")
async def trt_off(event):
    chat_id = event.chat_id
    if is_tede(chat_id):
        rem_tede(chat_id)
        return await edit_or_reply(event, "**⎉╎تم تعطيـل الترجمـة التلقائيـة .. بنجـاح ☑️**")
    await edit_or_reply(event, "**⎉╎الترجمـة التلقائيـة .. معطلـه بالفعـل هنـا ☑️**")


@zedub.on(events.NewMessage(outgoing=True))
async def ai_trt(event):
    sender_id = event.sender_id
    malath = zedub.uid
    zzt = event.message.text
    if sender_id != malath:
        return
    if not is_tede(event.chat_id):
        return
    if event.fwd_from or event.edit_hide:
        return
    if event.message.fwd_from:
        return
    if event.message.media or zzt.startswith(".") or zzt.startswith("⎉") or zzt.startswith("@") or zzt.startswith("https") or zzt.startswith("t.me"):
        return
    lan = gvarstatus("TRT") 
    text = zzt.strip()
    translator = Translator()
    try:
        translated = translator.translate(text, dest=lan)
        after_tr_text = translated.text
        await event.edit(after_tr_text)
    except Exception as exc:
        return
