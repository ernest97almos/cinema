from sqlalchemy.orm import Session
from models import Booking, Movie
from schemas import MultipleBookingCreate
from fastapi import HTTPException, status
from email_service import email_service
from sqlalchemy.orm import joinedload
from typing import List
import logging

logger = logging.getLogger(__name__)

def get_movies(db: Session):
    return db.query(Movie).all()

def get_booked_seats(db: Session, movie_id: int):
    return db.query(Booking).filter(Booking.movie_id == movie_id).all()

# УДАЛЯЕМ: def get_booked_by_email() - дублирует следующую

def create_multiple_bookings(db: Session, booking_data: MultipleBookingCreate):
    """Создание нескольких бронирований одновременно"""
    movie = db.query(Movie).filter(Movie.id == booking_data.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    successfully_booked = []
    failed_seats = []

    # Проверяем и бронируем каждое место
    for seat_id in booking_data.seat_ids:
        existing = db.query(Booking).filter(
            Booking.movie_id == booking_data.movie_id,
            Booking.seat_id == seat_id
        ).first()

        if existing:
            failed_seats.append(seat_id)
            continue

        db_booking = Booking(
            movie_id=booking_data.movie_id,
            seat_id=seat_id,
            email=booking_data.email
        )
        db.add(db_booking)
        successfully_booked.append(seat_id)

    db.commit()

    # Логируем перед отправкой email
    logger.info(f"📧 Attempting to send email to {booking_data.email} for seats {successfully_booked}")

    # Отправляем email подтверждение
    if successfully_booked:
        result = email_service.send_booking_confirmation(
            to_email=booking_data.email,
            movie_title=movie.title,
            seat_ids=successfully_booked
        )
        logger.info(f"📧 Email send result: {result}")

    return {
        "success": True,
        "message": f"Успешно забронировано {len(successfully_booked)} мест",
        "booked_seats": successfully_booked,
        "failed_seats": failed_seats
    }

def get_bookings_grouped_by_movie(db: Session, email: str):
    """Получить бронирования сгруппированные по фильмам"""
    bookings = db.query(Booking).options(joinedload(Booking.movie)).filter(Booking.email == email).all()

    # Группируем по фильмам
    grouped = {}
    for booking in bookings:
        if booking.movie.id not in grouped:
            grouped[booking.movie.id] = {
                'movie_id': booking.movie.id,  # ДОБАВЛЯЕМ movie_id
                'movie_title': booking.movie.title,
                'seat_ids': [],
                'booking_date': booking.booking_date.strftime("%d.%m.%Y %H:%M")
            }
        grouped[booking.movie.id]['seat_ids'].append(booking.seat_id)

    return list(grouped.values())