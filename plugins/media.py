import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from web.video_play import MEDIA_DB, register_media

logger = logging.getLogger(__name__)

# ── replace with your Telegram user ID ──
ADMIN_IDS = [5733685945]

# temporary state while admin is registering media
_pending: dict = {}


@Client.on_message(filters.command("fileid") & filters.reply)
async def get_file_id(client: Client, message: Message):
    replied = message.reply_to_message
    if replied.video:
        fid = replied.video.file_id
    elif replied.document:
        fid = replied.document.file_id
    else:
        await message.reply("❌ Reply to a video or document.")
        return
    await message.reply(
        f"📋 **File ID:**\n`{fid}`\n\n"
        "Use /addmedia to register this video with multiple languages."
    )


@Client.on_message(filters.command("addmedia") & filters.user(ADMIN_IDS))
async def addmedia_start(client: Client, message: Message):
    uid = message.from_user.id
    _pending[uid] = {"stage": "title"}
    await message.reply(
        "🎬 **Add New Media**\n\n"
        "**Step 1/3** — Send the **title** of the video.\n"
        "_Example: One Piece Episode 1152_"
    )


@Client.on_message(filters.command("addversion") & filters.user(ADMIN_IDS))
async def add_version(client: Client, message: Message):
    parts = message.text.split(maxsplit=3)
    if len(parts) < 4:
        await message.reply(
            "⚠️ **Usage:**\n"
            "`/addversion <main_file_id> <Label> <version_file_id>`\n\n"
            "**Example:**\n"
            "`/addversion ABC123 Hindi_Dub XYZ789`"
        )
        return
    _, main_id, label, ver_file_id = parts
    label = label.replace("_", " ")
    if main_id not in MEDIA_DB:
        await message.reply("❌ Main file ID not found. Register it first with /addmedia.")
        return
    MEDIA_DB[main_id]["versions"].append({"label": label, "file_id": ver_file_id})
    total = len(MEDIA_DB[main_id]["versions"])
    await message.reply(f"✅ Added **{label}**\nTotal versions: **{total}**")


@Client.on_message(filters.command("watch"))
async def watch_link(client: Client, message: Message):
    from config import HOST_URL
    parts = message.text.split()
    if len(parts) < 2:
        await message.reply("Usage: `/watch <file_id>`")
        return
    file_id = parts[1]
    url = f"{HOST_URL}/watch/{file_id}"
    await message.reply(f"▶️ **Watch Link:**\n{url}", disable_web_page_preview=False)


@Client.on_message(filters.command("listmedia") & filters.user(ADMIN_IDS))
async def list_media(client: Client, message: Message):
    if not MEDIA_DB:
        await message.reply("No media registered yet.")
        return
    text = "📚 **Registered Media:**\n\n"
    for main_id, meta in MEDIA_DB.items():
        text += f"🎬 **{meta['title']}**\n"
        text += f"   Main ID: `{main_id}`\n"
        for v in meta["versions"]:
            text += f"   • {v['label']} → `{v['file_id']}`\n"
        text += "\n"
    await message.reply(text)


@Client.on_message(filters.command("cancelmedia") & filters.user(ADMIN_IDS))
async def cancel_media(client: Client, message: Message):
    uid = message.from_user.id
    if _pending.pop(uid, None):
        await message.reply("❌ Media registration cancelled.")
    else:
        await message.reply("Nothing to cancel.")


@Client.on_message(filters.text & filters.private & filters.user(ADMIN_IDS))
async def addmedia_steps(client: Client, message: Message):
    uid = message.from_user.id
    state = _pending.get(uid)
    if not state:
        return
    stage = state["stage"]
    text = message.text.strip()

    if stage == "title":
        state["title"] = text
        state["stage"] = "main_id"
        await message.reply(
            f"✅ Title: **{text}**\n\n"
            "**Step 2/3** — Send the **main file_id**\n"
            "_Reply to a video with /fileid to get it_"
        )

    elif stage == "main_id":
        state["main_id"] = text
        state["versions"] = []
        state["stage"] = "versions"
        await message.reply(
            "**Step 3/3** — Send versions one by one:\n\n"
            "`<Label> <file_id>`\n\n"
            "**Examples:**\n"
            "`English Sub FILE_ID_1`\n"
            "`Hindi Dub   FILE_ID_2`\n"
            "`Arabic Sub  FILE_ID_3`\n\n"
            "Send /done when finished.\n"
            "Send /cancelmedia to cancel."
        )

    elif stage == "versions":
        if text.lower() == "/done":
            if not state["versions"]:
                await message.reply("⚠️ Add at least one version first.")
                return
            register_media(state["main_id"], state["title"], state["versions"])
            _pending.pop(uid, None)
            summary = "\n".join(f"  • {v['label']}" for v in state["versions"])
            await message.reply(
                f"✅ **Media Registered!**\n\n"
                f"🎬 {state['title']}\n"
                f"**Versions:**\n{summary}\n\n"
                f"Get watch link:\n`/watch {state['main_id']}`"
            )
            return

        parts = text.rsplit(maxsplit=1)
        if len(parts) < 2:
            await message.reply(
                "⚠️ Format: `<Label> <file_id>`\n"
                "Example: `English Sub ABC123XYZ`"
            )
            return
        label, file_id = parts
        state["versions"].append({"label": label.strip(), "file_id": file_id.strip()})
        count = len(state["versions"])
        await message.reply(
            f"✅ Version {count} added: **{label.strip()}**\n"
            "Send another or /done to finish."
        )
