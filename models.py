import os
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    DateTime,
    JSON,
    Numeric,
    ForeignKey,
    create_engine,
    text,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Resolve database URL with required transformations
raw_url = os.getenv("DATABASE_URL", os.getenv("POSTGRES_URL", "sqlite:///./app.db"))
if raw_url.startswith("postgresql+asyncpg://"):
    raw_url = raw_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
if raw_url.startswith("postgres://"):
    raw_url = raw_url.replace("postgres://", "postgresql+psycopg://")

# Determine if we need SSL (any non‑localhost and not SQLite)
connect_args = {}
if not raw_url.startswith("sqlite") and "localhost" not in raw_url and "127.0.0.1" not in raw_url:
    connect_args["sslmode"] = "require"

engine = create_engine(raw_url, echo=False, future=True, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# Prefix for all tables to avoid collisions
TABLE_PREFIX = "smartcal_ai_197103_"

class User(Base):
    __tablename__ = f"{TABLE_PREFIX}users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=True)
    dietary_preferences = Column(JSON, nullable=True, server_default=text("'{}'::jsonb"))
    health_goals = Column(JSON, nullable=True, server_default=text("'{}'::jsonb"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    meal_plans = relationship("MealPlan", back_populates="user")
    meals = relationship("Meal", back_populates="user")
    smart_plate_entries = relationship("SmartPlateEntry", back_populates="user")
    ai_predictions = relationship("AIPrediction", back_populates="user")

class MealPlan(Base):
    __tablename__ = f"{TABLE_PREFIX}meal_plans"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey(f"{TABLE_PREFIX}users.id"), nullable=False)
    start_date = Column(Date, nullable=False, default=datetime.utcnow)
    end_date = Column(Date, nullable=True)
    ai_model_version = Column(String, nullable=True)
    status = Column(String, nullable=False, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="meal_plans")
    meals = relationship("Meal", back_populates="meal_plan")

class Meal(Base):
    __tablename__ = f"{TABLE_PREFIX}meals"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    meal_plan_id = Column(String, ForeignKey(f"{TABLE_PREFIX}meal_plans.id"), nullable=False)
    user_id = Column(String, ForeignKey(f"{TABLE_PREFIX}users.id"), nullable=False)
    meal_type = Column(String, nullable=False)
    meal_date = Column(Date, nullable=False, default=datetime.utcnow)
    calories = Column(Integer, nullable=True)
    protein = Column(Numeric(10, 2), nullable=True)
    carbohydrates = Column(Numeric(10, 2), nullable=True)
    fat = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    meal_plan = relationship("MealPlan", back_populates="meals")
    user = relationship("User", back_populates="meals")
    smart_plate_entries = relationship("SmartPlateEntry", back_populates="meal")

class FoodItem(Base):
    __tablename__ = f"{TABLE_PREFIX}food_items"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    calories = Column(Integer, nullable=True)
    protein = Column(Numeric(10, 2), nullable=True)
    carbohydrates = Column(Numeric(10, 2), nullable=True)
    fat = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SmartPlateEntry(Base):
    __tablename__ = f"{TABLE_PREFIX}smart_plate_entries"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey(f"{TABLE_PREFIX}users.id"), nullable=False)
    meal_id = Column(String, ForeignKey(f"{TABLE_PREFIX}meals.id"), nullable=True)
    image_path = Column(String, nullable=True)
    ai_prediction = Column(JSON, nullable=True, server_default=text("'{}'::jsonb"))
    calories = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="smart_plate_entries")
    meal = relationship("Meal", back_populates="smart_plate_entries")

class AIPrediction(Base):
    __tablename__ = f"{TABLE_PREFIX}ai_predictions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey(f"{TABLE_PREFIX}users.id"), nullable=False)
    type = Column(String, nullable=False)
    prediction = Column(JSON, nullable=False, server_default=text("'{}'::jsonb"))
    confidence = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="ai_predictions")
