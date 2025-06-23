from fastapi import FastAPI, Request, Response

from app.database import channels, channels_by_code
from app.tg_integration.bot import bot

app = FastAPI()


@app.get('/send')
def send(request: Request, code: str) -> Response:
    with open('notif_template.md') as f:
        message = f.read()
    for channel in channels_by_code(code):
        bot.send_message(str(channel.id), message)

    return Response(status_code=200)
