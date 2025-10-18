from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    genre = Column(String)
    age_rating = Column(String)
    duration = Column(String)
    country = Column(String)
    imdb_rating = Column(String)
    year = Column(String)
    actors = Column(String)
    description = Column(String)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    seat_id = Column(Integer)
    email = Column(String)
    booking_date = Column(DateTime, default=datetime.utcnow)

    movie = relationship("Movie")

    __table_args__ = (
        UniqueConstraint("movie_id", "seat_id", name="unique_movie_seat"),
    )
