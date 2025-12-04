import asyncio
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from todo_app.models import Todo

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command as CommandFilter


TOKEN = "8534351601:AAEqQI5kBngf3txhwoRedzTcpKGuOId2cI8"

User = get_user_model()


# --- ХЕНДЛЕРЫ ДОЛЖНЫ БЫТЬ ОТДЕЛЬНО ---
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Это TODO бот.\n"
        "/all – список задач\n"
        "/add <текст> – создать задачу\n"
        "/done <id> – завершить задачу"
    )


async def cmd_all(message: types.Message):
    try:
        user = User.objects.get(username=message.from_user.id)
    except User.DoesNotExist:
        await message.answer("Ты ещё не зарегистрирован.")
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

    user, created = User.objects.get_or_create(
        username=message.from_user.id,
        defaults={"password": "telegram_user"}
    )

    Todo.objects.create(
        user=user,
        title=title,
        description=""
    )

    await message.answer("Добавлено ✔️")


async def cmd_done(message: types.Message):
    parts = message.text.split(" ")
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Используй: /done <id>")
        return

    todo_id = int(parts[1])

    try:
        todo = Todo.objects.get(id=todo_id)
    except Todo.DoesNotExist:
        await message.answer("Нет такого ID")
        return

    todo.complited = True
    todo.save()

    await message.answer("Выполнено ✔️")


# --- ОСНОВНОЙ ЦИКЛ БОТА ---
async def run_bot():
    bot = Bot(TOKEN)
    dp = Dispatcher()

    # регистрация хендлеров
    dp.message.register(cmd_start, CommandFilter("start"))
    dp.message.register(cmd_all, CommandFilter("all"))
    dp.message.register(cmd_add, CommandFilter("add"))
    dp.message.register(cmd_done, CommandFilter("done"))

    await dp.start_polling(bot)


class Command(BaseCommand):
    help = "Start Telegram Bot"

    def handle(self, *args, **kwargs):
        asyncio.run(run_bot())
