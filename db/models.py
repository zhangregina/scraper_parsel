from sqlalchemy import Column, Integer, String, TEXT, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # создает енджин вместе с модельнками


class AutoRiaModel(Base):
    __tablename__ = "auto"

    id = Column(Integer, primary_key=True)

    current_url = Column(String(100), nullable=True)
    title = Column(String(255), nullable=True)
    price = Column(String(100), nullable=True)
    price_usd_euro = Column(String(100), nullable=True)
    actual_cost_date = Column(String(100), nullable=True)
    in_stock = Column(String(100), nullable=True)
    car_rating = Column(String(200), nullable=True)
    credit = Column(String(100), nullable=True)
    autosalon_name = Column(String(100), nullable=True)
    autosalon_rating = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    engine = Column(String(200), nullable=True)
    gearbox = Column(String(200), nullable=True)
    privod = Column(String(200), nullable=True)
    generation = Column(String(100), nullable=True)
    car_color = Column(String(250), nullable=True)
    available_color = Column(String(250), nullable=True)
    image = Column(TEXT, nullable=True)
    max_speed = Column(String(100), nullable=True)
    vin_code = Column(String(150), nullable=True)

    created_at = Column(DateTime, default=func.now())
