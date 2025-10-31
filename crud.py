from sqlalchemy.orm import Session
from models import Booking, Movie
from schemas import BookingCreate, MultipleBookingCreate
from fastapi import HTTPException, status
from email_service import email_service
from sqlalchemy.orm import joinedload
from typing import List

def get_movies(db: Session):
    return db.query(Movie).all()

def get_booked_seats(db: Session, movie_id: int):
    return db.query(Booking).filter(Booking.movie_id == movie_id).all()

def get_booked_by_email(db: Session, email: str):
    """Получить все бронирования пользователя с информацией о фильмах"""
    return db.query(Booking).options(joinedload(Booking.movie)).filter(Booking.email == email).all()

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

    # Получаем информацию о фильме для email
    movie = db.query(Movie).filter(Movie.id == booking.movie_id).first()

    # Отправляем email подтверждение
    if movie:
        email_service.send_booking_confirmation(
            to_email=booking.email,
            movie_title=movie.title,
            seat_ids=[booking.seat_id]
        )

    return db_booking

def create_multiple_bookings(db: Session, booking_data: MultipleBookingCreate):
    """Создание нескольких бронирований одновременно"""
    movie = db.query(Movie).filter(Movie.id == booking_data.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    successfully_booked = []
    failed_seats = []

    # Проверяем и бронируем каждое место
    for seat_id in booking_data.seat_ids:
        # Проверяем, не занято ли место
        existing = db.query(Booking).filter(
            Booking.movie_id == booking_data.movie_id,
            Booking.seat_id == seat_id
        ).first()

        if existing:
            failed_seats.append(seat_id)
            continue

        # Создаем бронирование
        db_booking = Booking(
            movie_id=booking_data.movie_id,
            seat_id=seat_id,
            email=booking_data.email
        )
        db.add(db_booking)
        successfully_booked.append(seat_id)

    # Сохраняем все изменения одним коммитом
    db.commit()

    # Отправляем email подтверждение только если есть успешные бронирования
    if successfully_booked:
        email_service.send_booking_confirmation(
            to_email=booking_data.email,
            movie_title=movie.title,
            seat_ids=successfully_booked
        )

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
        if booking.movie.title not in grouped:
            grouped[booking.movie.title] = {
                'movie_title': booking.movie.title,
                'seat_ids': [],
                'booking_date': booking.booking_date.strftime("%d.%m.%Y %H:%M")
            }
        grouped[booking.movie.title]['seat_ids'].append(booking.seat_id)

    return list(grouped.values())