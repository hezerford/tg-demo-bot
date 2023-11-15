import asyncio
import logging

from decouple import config
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode

from config import Settings

BOT_TOKEN = config('BOT_TOKEN')

dp = Dispatcher()

@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer(
        text=f"Hello, {markdown.hbold(message.from_user.full_name)}!",
        parse_mode=ParseMode.HTML
    )

@dp.message(Command("help"))
async def handle_help(message: types.Message):
    # text = "I'm and echo bot.\nSend me any message!"
    # entity_bold = types.MessageEntity(
    #     type="bold",
    #     offset=len("I'm and echo bot.\nSend me "),
    #     length=3,
    # )
    # entities = [entity_bold]
    # await message.answer(text=text, entities=entities)
    # text = "I'm an echo bot\\.\nSend me *any* message\\!"
    text = markdown.text(
        markdown.markdown_decoration.quote("I'm an echo bot."),
        markdown.text(
            "Send me",
            markdown.underline("literally"),
            markdown.bold("any"),
            markdown.markdown_decoration.quote("message!")),
        sep="\n",
    )
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)

@dp.message(Command("code"))
async def handle_command_code(message: types.Message):
    text = markdown.text(
        "Here's python code:",
        "",
        markdown.markdown_decoration.pre_language(
            markdown.text(
                "print('Hello world')",
                "",
                "def foo():\n   return 'bar'",
                sep="\n",
            ),
            language="python",
        ),
        sep="\n"
    )
    await message.answer(text=text)

@dp.message()
async def echo_message(message: types.Message):
    # await bot.send_message(
    #     chat_id=message.chat.id,
    #     text="Start processing...",
    # )
    # await bot.send_message(
    #     chat_id=message.chat.id,
    #     text="Deteted message..",
    #     reply_to_message_id=message.message_id,
    # )

    
    
    await message.answer(
        text="Wait a second...",
        parse_mode=None,
    )
    if message.text:
        await message.answer(
            text=message.text,
            entities=message.entities,
            parse_mode=None,
        )
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text="Something new!")

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=BOT_TOKEN,
        parse_mode=ParseMode.MARKDOWN_V2,
        )
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())