from sqlalchemy.orm import Session
from models import Booking, Movie
from schemas import BookingCreate
from fastapi import HTTPException, status

def get_movies(db: Session):
    return db.query(Movie).all()

def get_booked_seats(db: Session, movie_id: int):
    return db.query(Booking).filter(Booking.movie_id == movie_id).all()

def get_booked_by_email(db: Session, email: str):
    return db.query(Booking).filter(Booking.email == email).all()


def create_booking(db: Session, booking: BookingCreate):
    existing = db.query(Booking).filter(
        Booking.movie_id == booking.movie_id,
        Booking.seat_id == booking.seat_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seat already booked"
        )

    db_booking = Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking
