# Originally By @DeletedUser420
# Ported - @StarkxD
import asyncio
import html
import os
import re
import shlex
import subprocess
import time
from datetime import datetime
from os.path import basename
from typing import List
from typing import Optional
from typing import Tuple

from telegraph import exceptions
from telegraph import Telegraph
from telegraph import upload_file

from fridaybot.Configs import Config
from fridaybot.utils import friday_on_cmd
from fridaybot.utils import sudo_cmd

telegraph = Telegraph()
tgnoob = telegraph.create_account(short_name="Friday 🇮🇳")


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """ run command in terminal """
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


@friday.on(friday_on_cmd(pattern="mediainfo$"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    if reply_message is None:
        await event.edit("Reply To a Media.")
    await event.edit("`Processing...`")
    file_path = await borg.download_media(reply_message, Config.TMP_DOWNLOAD_DIRECTORY)
    out, err, ret, pid = await runcmd(f"mediainfo '{file_path}'")
    media_info = f"""
    <code>
    {out}
    </code>"""
    title_of_page = "Media Info 🎬"
    response = telegraph.create_page(title_of_page, html_content=media_info)
    km = response["path"]
    await event.edit(f"`This MediaInfo Can Be Found` [Here](https://telegra.ph/{km})")
    if os.path.exists(file_path):
        os.remove(file_path)
