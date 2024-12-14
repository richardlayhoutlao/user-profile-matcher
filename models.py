from database import Base
from sqlalchemy import Column, DateTime, Integer, String, Boolean


class Campaigns(Base):
    __tablename__ = 'campaigns'

    campaign_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    game = Column(String)
    priority = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    enabled = Column(Boolean)
    last_updated = Column(DateTime)

class Players(Base):
    __tablename__ = 'players'

    player_id = Column(Integer, primary_key=True, index=True)
    credential = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)
    last_session = Column(DateTime)
    total_spent = Column(Integer)
    total_refund = Column(Integer)
    total_transactions = Column(Integer)
    last_purchase = Column(DateTime)
    level = Column(Integer)
    xp = Column(Integer)
    total_playtime = Column(Integer)
    country = Column(String)
    language = Column(String)
    birthdate = Column(DateTime)
    gender = Column(String)
    _customfield = Column(String)
    
    
