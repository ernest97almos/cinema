from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db

router = APIRouter()

# --- Movies ---
@router.get("/movies/", response_model=list[schemas.MovieResponse])
def get_movies(db: Session = Depends(get_db)):
    return crud.get_movies(db)

# --- Bookings ---
@router.get("/bookings/{movie_id}", response_model=list[schemas.BookingResponse])
def get_booked_seats(movie_id: int, db: Session = Depends(get_db)):
    return crud.get_booked_seats(db, movie_id)

@router.post("/bookings/", response_model=schemas.BookingResponse)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    return crud.create_booking(db, booking)
