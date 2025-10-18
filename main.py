from fastapi import FastAPI
from database import engine, Base
from routers import router
from movies import init_movies

app = FastAPI(title="Cinema Booking API")

Base.metadata.create_all(bind=engine)

init_movies()

app.include_router(router)
