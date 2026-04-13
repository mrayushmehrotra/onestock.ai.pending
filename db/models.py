from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import datetime

Base = declarative_base()

class PredictionRun(Base):
    __tablename__ = "prediction_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_at = Column(DateTime(timezone=True), server_default=func.now())
    symbols_analyzed = Column(Integer)
    model_version = Column(String)

    predictions = relationship("Prediction", back_populates="run")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("prediction_runs.id"))
    symbol = Column(String, index=True)
    boom_score = Column(Float)
    confidence = Column(String)
    risk_flag = Column(String, nullable=True)
    cleared = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    run = relationship("PredictionRun", back_populates="predictions")
    outcome = relationship("Outcome", back_populates="prediction", uselist=False)

class Outcome(Base):
    __tablename__ = "outcomes"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id"))
    actual_return = Column(Float)
    was_correct = Column(Boolean)
    evaluated_at = Column(DateTime(timezone=True), onupdate=func.now())

    prediction = relationship("Prediction", back_populates="outcome")

class DailyPrice(Base):
    __tablename__ = "daily_prices"

    symbol = Column(String, primary_key=True, index=True)
    date = Column(Date, primary_key=True, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
