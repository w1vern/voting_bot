
import asyncio

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ChatType
from aiogram.filters import Command
from aiogram.types import InputPollOption, Message, MenuButtonDefault

from bot.env import env_config
from bot.logger import setup_logger

from aiogram.types import (
    BotCommandScopeDefault,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeAllGroupChats,
    BotCommandScopeAllChatAdministrators,
)

logger = setup_logger(__name__)

router = Router()


# @router.message(
#     Command("poll"),
#     F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP})
# )
# async def create_poll(message: Message, bot: Bot) -> None:
#     await bot.send_poll(
#         chat_id=message.chat.id,
#         question="?",
#         options=[InputPollOption(text=str(i)) for i in range(1, 11)],
#         is_anonymous=False,
#         type="regular",
#         allows_multiple_answers=False,
#         message_thread_id=message.message_thread_id,
#     )


@router.message(
    F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}),
    F.text.contains("make-poll"),
)
async def create_poll_on_keyword(message: Message) -> None:
    await message.reply_poll(
        question="?",
        options=[InputPollOption(text=str(i)) for i in range(1, 11)],
        is_anonymous=False,
        type="regular",
        allows_multiple_answers=False,
    )


async def start_bot() -> None:
    retry_delay = 5
    max_retry_delay = 60

    while True:
        session = AiohttpSession(
            proxy=env_config.proxy) if env_config.proxy else AiohttpSession()
        try:
            bot = Bot(
                token=env_config.token,
                session=session,
            )
            await bot.delete_my_commands()
            await bot.set_chat_menu_button(menu_button=MenuButtonDefault())
            dp = Dispatcher()
            dp.include_router(router)
            retry_delay = 5
            await dp.start_polling(bot)
            break
        except Exception as e:
            logger.error(
                "Polling stopped with error: %s. Retrying in %ds...", e, retry_delay)
            await asyncio.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, max_retry_delay)
        finally:
            await session.close()
