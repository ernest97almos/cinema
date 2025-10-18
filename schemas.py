from pydantic import BaseModel
from datetime import datetime

class MovieResponse(BaseModel):
    id: int
    title: str
    genre: str
    age_rating: str
    duration: str
    country: str
    imdb_rating: str
    year: str
    actors: str
    description: str

    model_config = {
        "from_attributes": True
    }

class BookingCreate(BaseModel):
    movie_id: int
    seat_id: int
    email: str

class BookingResponse(BaseModel):
    id: int
    movie_id: int
    seat_id: int
    email: str
    booking_date: datetime

    model_config = {
        "from_attributes": True
    }
