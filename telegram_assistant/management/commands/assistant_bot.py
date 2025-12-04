import asyncio
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from todo_app.models import Todo

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command as CommandFilter

TOKEN = "8534351601:AAEqQI5kBngf3txhwoRedzTcpKGuOId2cI8"

User = get_user_model()

async def get_user(message: types.Message):
    """
    Получаем пользователя по telegram_id. Если нет, возвращаем None.
    """
    try:
        user = User.objects.get(username=str(message.from_user.id))
        return user
    except User.DoesNotExist:
        return None


async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Это TODO бот.\n"
        "/register <пароль> – зарегистрироваться\n"
        "/login <пароль> – войти\n"
        "/all – список задач\n"
        "/add <текст> – создать задачу\n"
        "/done <id> – завершить задачу"
    )


async def cmd_register(message: types.Message):
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        await message.answer("Используй: /register <пароль>")
        return

    password = parts[1]

    if await get_user(message):
        await message.answer("Ты уже зарегистрирован.")
        return

    User.objects.create(
        username=str(message.from_user.id),
        password=make_password(password)
    )
    await message.answer("Регистрация успешна! Теперь можно /login.")


async def cmd_login(message: types.Message):
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        await message.answer("Используй: /login <пароль>")
        return

    password = parts[1]
    user = await get_user(message)
    if not user:
        await message.answer("Ты ещё не зарегистрирован. Используй /register <пароль>")
        return

    if check_password(password, user.password):
        await message.answer("Вход успешен! Теперь можно работать с задачами.")
    else:
        await message.answer("Неверный пароль.")


async def cmd_all(message: types.Message):
    user = await get_user(message)
    if not user:
        await message.answer("Ты не зарегистрирован. Используй /register <пароль>")
        return

    todos = Todo.objects.filter(user=user).order_by("-id")
    if not todos:
        await message.answer("У тебя нет задач.")
        return

    text = ""
    for t in todos:
        status = "✔️" if t.complited else "❌"
        text += f"{t.id}. {t.title}  {status}\n"

    await message.answer(text)


async def cmd_add(message: types.Message):
    parts = message.text.split(" ", 1)
    if len(parts) < 2:
        await message.answer("Используй: /add <текст>")
        return

    title = parts[1]

    user = await get_user(message)
    if not user:
        await message.answer("Ты не зарегистрирован. Используй /register <пароль>")
        return

    Todo.objects.create(user=user, title=title, description="")
    await message.answer("Задача добавлена ✔️")


async def cmd_done(message: types.Message):
    parts = message.text.split(" ")
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Используй: /done <id>")
        return

    todo_id = int(parts[1])
    user = await get_user(message)
    if not user:
        await message.answer("Ты не зарегистрирован. Используй /register <пароль>")
        return

    try:
        todo = Todo.objects.get(id=todo_id, user=user)
    except Todo.DoesNotExist:
        await message.answer("Нет такого ID у твоих задач.")
        return

    todo.complited = True
    todo.save()
    await message.answer("Задача выполнена ✔️")


async def run_bot():
    bot = Bot(TOKEN)
    dp = Dispatcher()

    dp.message.register(cmd_start, CommandFilter("start"))
    dp.message.register(cmd_register, CommandFilter("register"))
    dp.message.register(cmd_login, CommandFilter("login"))
    dp.message.register(cmd_all, CommandFilter("all"))
    dp.message.register(cmd_add, CommandFilter("add"))
    dp.message.register(cmd_done, CommandFilter("done"))

    await dp.start_polling(bot)


class Command(BaseCommand):
    help = "Start Telegram Bot"

    def handle(self, *args, **kwargs):
        asyncio.run(run_bot())