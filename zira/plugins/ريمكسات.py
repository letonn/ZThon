import asyncio
import os

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from . import zedub
from ..core.logger import logging

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply

plugin_category = "البحث"

@zedub.zed_cmd(
    pattern="ريماكس ([\s\S]*)",
    command=("ريماكس", plugin_category),
    info={
        "header": "ريمكسـات اغـانـي قصيـره",
        "الاستـخـدام": "{tr}ريماكس + كلمـة",
    },
)
async def remaxzedthon(zedrm):
    ok = zedrm.pattern_match.group(1)
    if not ok:
        if zedrm.is_reply:
            what = (await zedrm.get_reply_message()).message
        else:
            await zedrm.edit("`Sir please give some query to search and download it for you..!`")
            return
    sticcers = await bot.inline_query(
        "spotifybot", f"{(deEmojify(ok))}")
    await sticcers[0].click(zedrm.chat_id,
                            reply_to=zedrm.reply_to_msg_id,
                            silent=True if zedrm.is_reply else False,
                            hide_via=True)
    await zedrm.delete()
    

@zedub.zed_cmd(
    pattern="ريمكس ([\s\S]*)",
    command=("ريمكس", plugin_category),
    info={
        "header": "ريمكسـات اغـانـي قصيـره",
        "الاستـخـدام": "{tr}ريمكس + كلمـة",
    },
)
async def zed(event):
    if event.fwd_from:
        return
    zedr = event.pattern_match.group(1)
    zira = "@spotifybot"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(zira, zedr)
    await tap[0].click(event.chat_id)
    await event.delete()

