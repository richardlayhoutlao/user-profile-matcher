from database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Players(Base):
    __tablename__ = 'players'

    player_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    total_spent = Column(Integer)
