import uvicorn

from .tg_integration.bot import bot
from .database import engine
from .server import app


def main():
    print("Hello from twitch-notif!")
    bot.infinity_polling()


def web():
    print('starting web')
    uvicorn.run(app, host='0.0.0.0', port=8080)
