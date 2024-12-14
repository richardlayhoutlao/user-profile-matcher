import uuid
from database import Base
from sqlalchemy import JSON, UUID, Column, DateTime, Float, Integer, String, Boolean


class Campaigns(Base):
    __tablename__ = 'campaigns'

    campaign_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    game = Column(String)
    name = Column(String)
    priority = Column(Float)
    matchers = Column(JSON)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    enabled = Column(Boolean)
    last_updated = Column(DateTime)

class Players(Base):
    __tablename__ = 'players'

    player_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    credential = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)
    last_session = Column(DateTime)
    total_spent = Column(Integer)
    total_refund = Column(Integer)
    total_transactions = Column(Integer)
    last_purchase = Column(DateTime)
    active_campaigns = Column(JSON)
    devices = Column(JSON)  
    level = Column(Integer)
    xp = Column(Integer)
    total_playtime = Column(Integer)
    country = Column(String)
    language = Column(String)
    birthdate = Column(DateTime)
    gender = Column(String)
    inventory = Column(JSON)
    clan = Column(JSON)
    _customfield = Column(String)
    
    
