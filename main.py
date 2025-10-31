from fastapi import FastAPI
from database import engine, Base
from routers import router
from movies import init_movies
from fastapi.middleware.cors import CORSMiddleware

from models import Movie, Booking


Base.metadata.drop_all(bind=engine)  # Удаляем старые таблицы
Base.metadata.create_all(bind=engine)  # Создаем новые с исправленными моделями

app = FastAPI(title="Cinema Booking API")

origins = [
    "https://cinema-front-one.vercel.app",
    "https://kino-app-lbaz.vercel.app",
    "http://localhost:3000"  # обратите внимание на http://
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

init_movies()

app.include_router(router)
