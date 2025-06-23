from sqlalchemy import select
from sqlalchemy.orm import Session
import telebot
from ..config import tg_token
from ..database import Channel, add_channel, channels, engine, get_or_create_user, get_send_code, set_state

assert tg_token
bot = telebot.TeleBot(tg_token)


@bot.message_handler(commands=['add'])
def add(message: telebot.types.Message) -> None:
    assert message.text
    assert message.from_user
    channel = message.text.split()[1:]

    if not channel:
        bot.reply_to(message, 'Use /add <channel> (eg: `@ChannelName` or `https://t.me/ChannelName`)')

    channel = channel[0]
    if channel.startswith('https://t.me/'):
        channel = '@' + channel[len('https://t.me/'):]

    print(channel)
    chat_info = bot.get_chat(channel)
    user = get_or_create_user(message.from_user.id)
    add_channel(chat_info.id, user.id)
    bot.reply_to(message, f'Saved chat {chat_info.id} to send notification')


@bot.message_handler(commands=['chats'])
def chats(message: telebot.types.Message) -> None:
    assert message.from_user
    response = ''
    for channel in channels(message.from_user.id):
        chat_info = bot.get_chat(str(channel.id))
        response += f'{chat_info.title} ({chat_info.id}): active {channel.active};\n'

    if response:
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, 'No chats')


@bot.message_handler(commands=['activate', 'deactivate'])
def change_state(message: telebot.types.Message) -> None:
    assert message.text
    state, id = message.text.split()
    state = state == '/activate'
    set_state(id, state)
    bot.reply_to(message, f'state changed id: {id} state: {state}')


@bot.message_handler(commands=['send_code'])
def send_code(message: telebot.types.Message) -> None:
    assert message.from_user
    code = get_send_code(message.from_user.id)
    bot.reply_to(message, f'code is `{code}`')
