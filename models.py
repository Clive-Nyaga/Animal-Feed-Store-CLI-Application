from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default='user')
    
    transactions = relationship("Transaction", back_populates="user")

class Feed(Base):
    __tablename__ = 'feeds'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)
    
    transactions = relationship("Transaction", back_populates="feed")

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    feed_id = Column(Integer, ForeignKey('feeds.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="transactions")
    feed = relationship("Feed", back_populates="transactions")

# Database setup
engine = create_engine('sqlite:///animal_feed_store.db')
Session = sessionmaker(bind=engine)