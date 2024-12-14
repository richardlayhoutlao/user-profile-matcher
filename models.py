from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean


class Campaigns(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    game = Column(String, unique=True)
    priority = Column(Integer)
    enabled = Column(Boolean)

class Players(Base):
    __tablename__ = 'players'

    player_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    total_spent = Column(Integer)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
