from sqlalchemy import create_all, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class ScrapedNews(Base):
    __tablename__ = 'scraped_news'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    summary = Column(String)
    url = Column(String, unique=True, nullable=False)
    source = Column(String)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    tickers = Column(JSON) # Store list of tickers as JSON

class MarketState(Base):
    __tablename__ = 'market_state'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    nifty_50 = Column(Float)
    sensex = Column(Float)
    weather_temp = Column(Float)
    weather_status = Column(String)
    current_season = Column(String)

# Database Setup Helper
def init_db(db_url="sqlite:///./data/onestock.db"):
    from sqlalchemy import create_engine
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
