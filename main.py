from fastapi import FastAPI
from schemas.index import app_graphql
from streaming.streaming import app_streaming
from audio_manegement.songs import song_img
import threading
from RabbitMQ.Audio_manegement.server import consume_messages

app = FastAPI()
app.include_router(app_graphql)
app.include_router(app_streaming)
app.include_router(song_img)

# Iniciar el consumidor de RabbitMQ en un hilo separado
consumer_thread = threading.Thread(target=consume_messages)
consumer_thread.start()
