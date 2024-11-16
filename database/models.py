from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    height = Column(Float)
    weight = Column(Float)
    gender = Column(String)
    age = Column(Integer)
    goal = Column(String)
    registration_date = Column(DateTime, default=datetime.utcnow)
    is_subscribed = Column(Boolean, default=False)
    subscription_end_date = Column(DateTime, nullable=True)
    
    weight_records = relationship("WeightRecord", back_populates="user")
    nutrition_plans = relationship("NutritionPlan", back_populates="user")
    workout_plans = relationship("WorkoutPlan", back_populates="user")

class WeightRecord(Base):
    __tablename__ = 'weight_records'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, default=datetime.utcnow)
    weight = Column(Float)
    
    user = relationship("User", back_populates="weight_records") 

class NutritionPlan(Base):
    __tablename__ = 'nutrition_plans'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, default=datetime.utcnow)
    calories = Column(Float)
    meal_plan = Column(String)
    
    user = relationship("User", back_populates="nutrition_plans")

class WorkoutPlan(Base):
    __tablename__ = 'workout_plans'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, default=datetime.utcnow)
    program = Column(String)
    difficulty = Column(String)
    
    user = relationship("User", back_populates="workout_plans")