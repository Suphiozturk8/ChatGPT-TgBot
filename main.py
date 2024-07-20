
import json
import html
import asyncio
import requests
from datetime import datetime, timedelta

from pyrogram import Client, filters, enums, idle
from pyrogram.types import Message

from config import Config


app = Client(
    "my_app",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)


loop = asyncio.get_event_loop()


def reset_json_files():
    for file in ["data.json", "timer.json"]:
        with open(file, "w") as f:
            f.write("{}")


def chat_gpt(text):
    url = Config.API_BASE_URL + text
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("message", "No response received!")
    except requests.exceptions.RequestException as e:
        print(f"HTTP Error: {e}")
        return "HTTP Error!"
    except json.decoder.JSONDecodeError:
        return "Invalid JSON response."


def timer_set(user_id, timer, time_type, time_value):
    delta = datetime.now() + (
        timedelta(minutes=time_value)
        if time_type == "min"
        else timedelta(seconds=time_value)
    )
    timer[user_id] = {
        "y": delta.year, "m": delta.month,
        "d": delta.day, "h": delta.hour,
        "min": delta.minute, "s": delta.second
    }


def is_timer_expired(user_id, timer):
    if user_id in timer:
        expiry_time = datetime(
            timer[user_id]["y"], timer[user_id]["m"],
            timer[user_id]["d"], timer[user_id]["h"],
            timer[user_id]["min"], timer[user_id]["s"]
        )
        return datetime.now() > expiry_time
    return True


def collect_messages(user_id, message_text):
    with open("data.json", "r") as f:
        data = json.load(f)

    if user_id not in data:
        data[user_id] = {"messages": [], "count": 0}

    data[user_id]["messages"].append(message_text)
    data[user_id]["count"] += 1

    if data[user_id]["count"] >= 10:
        data[user_id] = {"messages": [], "count": 0}
    
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)
    
    return "\n".join(data[user_id]["messages"])


def is_reply_to_bot() -> filters.Filter:
    async def func(_, client: Client, message: Message) -> bool:
        return message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.id == client.me.id

    return filters.create(func, name="is_reply_to_bot")


@app.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply(
        f"Hello! {message.from_user.mention} 👋\n"
        "I am your personal AI assistant. 🤖\n\n"
        "I am here to answer your questions, provide information, and chat with you.\n"
        "You can start by asking a question right away. 📚\n\n"
        "How can I help you?"
    )


@app.on_message(filters.command("help"))
async def help(_, message: Message):
    await message.reply(
        "Hello! I am your personal AI assistant. 🤖\n\n"
        "You can interact with me using the following commands:\n\n"
        "/start - Start me and see the welcome message.\n"
        "/help - See this help message.\n"
        "/resetchat - Reset your message history.\n\n"
        "If you have any questions or requests, just send a message.\n"
        "I am here to answer your questions!"
    )


@app.on_message(filters.command("resetchat"))
async def reset(_, message: Message):
    user_id = str(message.from_user.id)
    with open("data.json", "r") as f:
        data = json.load(f)
    
    if user_id not in data or data[user_id]["count"] == 0:
        return await message.reply(
            "You do not have any saved data."
        )

    data[user_id] = {"messages": [], "count": 0}
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)
    await message.reply(
        "Your message history has been reset."
    )


@app.on_message(
    filters.text
    & (is_reply_to_bot() | filters.private)
)
async def handle_message(client: Client, message: Message):
    user_id = str(message.from_user.id)

    with open("timer.json", "r") as f:
        timer = json.load(f)

    if is_timer_expired(user_id, timer):
        timer_set(user_id, timer, "min", 0.5)
        await client.send_chat_action(
            message.chat.id, enums.ChatAction.TYPING
        )
        combined_message = collect_messages(
            user_id, message.text
        )
        response = chat_gpt(combined_message)
        await message.reply(
            html.escape(response),
            parse_mode=enums.ParseMode.MARKDOWN
        )

        with open("timer.json", "w") as f:
            json.dump(timer, f, indent=4)
    else:
        remaining_time = datetime(
            timer[user_id]["y"], timer[user_id]["m"],
            timer[user_id]["d"], timer[user_id]["h"],
            timer[user_id]["min"], timer[user_id]["s"]
        ) - datetime.now()
        await message.reply(
            f"Please wait {int(remaining_time.total_seconds())} seconds and ask your question again."
        )


async def main():
    print("\nBot is starting...")
    reset_json_files()
    await app.start()
    print("\nBot started.")
    await idle()
    print("\nBot is stopping...")
    await app.stop()
    print("\nBot stopped.")


if __name__ == "__main__":
    loop.run_until_complete(main())
