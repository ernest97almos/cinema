from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas
from database import get_db
from email_service import email_service

router = APIRouter()

# --- Movies ---
@router.get("/movies/", response_model=list[schemas.MovieResponse])
def get_movies(db: Session = Depends(get_db)):
    return crud.get_movies(db)

# --- Bookings ---
# УДАЛЯЕМ: @router.get("/bookings/{email}") - дублирует следующий
@router.get("/bookings/{movie_id}", response_model=list[schemas.BookingResponse])
def get_booked_seats(movie_id: int, db: Session = Depends(get_db)):
    return crud.get_booked_seats(db, movie_id)

# УДАЛЯЕМ: @router.post("/bookings/") - дублирует следующий
@router.post("/bookings-multiple/", response_model=schemas.MultipleBookingResponse)
def create_multiple_bookings(booking: schemas.MultipleBookingCreate, db: Session = Depends(get_db)):
    """Бронирование нескольких мест одновременно"""
    return crud.create_multiple_bookings(db, booking)

@router.get("/bookings-grouped/{email}", response_model=list[schemas.GroupedBookingResponse])
def get_grouped_bookings(email: str, db: Session = Depends(get_db)):
    """Получить бронирования сгруппированные по фильмам"""
    return crud.get_bookings_grouped_by_movie(db, email)

@router.post("/send-all-bookings/", response_model=schemas.EmailResponse)
async def send_all_bookings(request: schemas.EmailRequest, db: Session = Depends(get_db)):
    """Отправить все бронирования пользователя на email"""
    try:
        # Получаем сгруппированные бронирования
        grouped_bookings = crud.get_bookings_grouped_by_movie(db, request.email)

        if not grouped_bookings:
            raise HTTPException(status_code=404, detail="No bookings found for this email")

        # Отправляем email
        result = await email_service.send_all_bookings(
            to_email=request.email,
            bookings_data=grouped_bookings
        )

        return schemas.EmailResponse(
            success=result["success"],
            message=result["message"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# УДАЛЯЕМ: @router.get("/email-status/") - необязательный