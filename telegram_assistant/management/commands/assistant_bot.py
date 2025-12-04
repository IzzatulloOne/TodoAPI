import asyncio
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password

from todo_app.models import Todo
from telegram_assistant.models import TelegramSession

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command as AiogramCommand
from aiogram.filters.command import CommandStart
from asgiref.sync import sync_to_async

TOKEN = "8534351601:AAEqQI5kBngf3txhwoRedzTcpKGuOId2cI8"
User = get_user_model()


@sync_to_async
def get_user(tg_id: int):
    try:
        return User.objects.get(username=str(tg_id))
    except User.DoesNotExist:
        return None


@sync_to_async
def get_session(user):
    return TelegramSession.objects.get_or_create(user=user)[0]


@sync_to_async
def is_logged_in(user) -> bool:
    try:
        return TelegramSession.objects.get(user=user).logged_in
    except TelegramSession.DoesNotExist:
        return False


def auth_required(handler):
    async def wrapper(message: types.Message):
        user = await get_user(message.from_user.id)
        if not user:
            await message.answer("Зарегистрируйся: /register <пароль>")
            return
        if not await is_logged_in(user):
            await message.answer("Войди: /login <пароль>")
            return
        return await handler(message, user=user)
    return wrapper


async def cmd_start(message: types.Message):
    await message.answer("Привет! TODO-бот\n\nКоманды:\n/register <пароль>\n/login <пароль>\n/all\n/add <текст>\n/done <id>\n/logout")


async def cmd_register(message: types.Message):
    if len(message.text.split()) < 2:
        await message.answer("Использование: /register <пароль>")
        return
    password = message.text.split(maxsplit=1)[1]
    if await get_user(message.from_user.id):
        await message.answer("Ты уже зарегистрирован")
        return

    await sync_to_async(User.objects.create)(
        username=str(message.from_user.id),
        password=make_password(password)
    )
    user = await get_user(message.from_user.id)
    session = await get_session(user)
    session.logged_in = True
    await sync_to_async(session.save)()
    await message.answer("Регистрация успешна!")


async def cmd_login(message: types.Message):
    if len(message.text.split()) < 2:
        await message.answer("Использование: /login <пароль>")
        return
    password = message.text.split(maxsplit=1)[1]
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("Сначала зарегистрируйся")
        return
    if not check_password(password, user.password):
        await message.answer("Неверный пароль")
        return
    session = await get_session(user)
    session.logged_in = True
    await sync_to_async(session.save)()
    await message.answer("Вход выполнен!")


async def cmd_logout(message: types.Message):
    user = await get_user(message.from_user.id)
    if user:
        session = await get_session(user)
        session.logged_in = False
        await sync_to_async(session.save)()
        await message.answer("Выход выполнен")
    else:
        await message.answer("Ты и так не авторизован")


@auth_required
async def cmd_all(message: types.Message, user):
    todos = await sync_to_async(list)(Todo.objects.filter(user=user).order_by('-id'))
    if not todos:
        await message.answer("Задач нет")
        return
    text = "Твои задачи:\n\n"
    for t in todos:
        status = "Выполнена" if t.complited else "В процессе"
        text += f"{status} <b>{t.id}</b>. {t.title}\n"
    await message.answer(text, parse_mode="HTML")


@auth_required
async def cmd_add(message: types.Message, user):
    text = message.text[len("/add"):].strip()
    if not text:
        await message.answer("Использование: /add <текст>")
        return
    await sync_to_async(Todo.objects.create)(user=user, title=text)
    await message.answer("Задача добавлена")


@auth_required
async def cmd_done(message: types.Message, user):
    try:
        todo_id = int(message.text.split()[1])
    except:
        await message.answer("Использование: /done <id>")
        return
    try:
        todo = await sync_to_async(Todo.objects.get)(id=todo_id, user=user)
        todo.complited = True
        await sync_to_async(todo.save)()
        await message.answer("Задача выполнена")
    except Todo.DoesNotExist:
        await message.answer("Задача не найдена")


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_register, AiogramCommand(commands=["register"]))
    dp.message.register(cmd_login,    AiogramCommand(commands=["login"]))
    dp.message.register(cmd_logout,   AiogramCommand(commands=["logout"]))
    dp.message.register(cmd_all,      AiogramCommand(commands=["all"]))
    dp.message.register(cmd_add,      AiogramCommand(commands=["add"]))
    dp.message.register(cmd_done,     AiogramCommand(commands=["done"]))

    print("Бот запущен и ждёт сообщений...")
    await dp.start_polling(bot)


class Command(BaseCommand):
    help = "Запуск Telegram TODO бота"

    def handle(self, *args, **options):
        asyncio.run(main())