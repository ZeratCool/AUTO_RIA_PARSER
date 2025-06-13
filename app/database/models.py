from sqlalchemy import Index
from sqlalchemy import Column, String, Integer, Float, DateTime
from app.database.engine import Base
from datetime import datetime

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False, index=True)
    title = Column(String)
    price_usd = Column(Float)
    odometer = Column(Integer)
    username = Column(String)
    phone_number = Column(String, index=True)
    image_url = Column(String)
    images_count = Column(Integer)
    car_number = Column(String)
    car_vin = Column(String, index=True)
    datetime_found = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_car_phone", "phone_number"),
        Index("ix_car_vin", "car_vin"),
    )