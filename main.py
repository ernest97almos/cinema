from fastapi import FastAPI
from database import engine, Base
from routers import router
from movies import init_movies
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "https://kino-app-lbaz.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI(title="Cinema Booking API")

Base.metadata.create_all(bind=engine)

init_movies()

app.include_router(router)
