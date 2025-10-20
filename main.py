from fastapi import FastAPI
from database import engine, Base
from routers import router
from movies import init_movies
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Cinema Booking API")

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




Base.metadata.create_all(bind=engine)

init_movies()

app.include_router(router)
