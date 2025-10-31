from pydantic import BaseModel
from datetime import datetime
from typing import List

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

class BookingResponse(BaseModel):
    id: int
    movie_id: int
    seat_id: int
    email: str
    booking_date: datetime

    model_config = {
        "from_attributes": True
    }

class MultipleBookingCreate(BaseModel):
    movie_id: int
    seat_ids: List[int]
    email: str

class MultipleBookingResponse(BaseModel):
    success: bool
    message: str
    booked_seats: List[int]
    failed_seats: List[int] = []

# ОБНОВЛЯЕМ: добавляем movie_id
class GroupedBookingResponse(BaseModel):
    movie_id: int
    movie_title: str
    seat_ids: List[int]
    booking_date: str

class EmailRequest(BaseModel):
    email: str

class EmailResponse(BaseModel):
    success: bool
    message: str