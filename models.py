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
    name = Column(String)
    total_spent = Column(Integer)
