from fastapi import FastAPI
from database import engine, Base
from routers import router
from movies import init_movies
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Cinema Booking API")

origins = [
    "https://cinema-front-one.vercel.app",
    "https://kino-app-lbaz.vercel.app",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def database_exists():
    return os.path.exists("cinema.db")

if not database_exists():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")


    init_movies()
else:
    print("✅ Database already exists, skipping creation")

app.include_router(router)
