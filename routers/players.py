from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field
import pytz
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Campaigns, Players
from database import SessionLocal
from routers.campaigns import Matchers

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

class Device(BaseModel):
    id: int
    model: str
    carrier: str
    firmware: str

class Clan(BaseModel):
    id: str
    name: str

class PlayerRequest(BaseModel):
    credential: str
    created : datetime
    modified : datetime
    last_session : datetime
    total_spent : float 
    total_refund : float 
    total_transactions : int 
    last_purchase : datetime
    active_campaigns: list[str]
    devices: list[Device]
    level : int = Field(gt= 0)
    xp : int 
    total_playtime : float 
    country : str
    language : str
    birthdate : datetime
    gender : str
    inventory: dict
    clan: dict
    _customfield : str
    

@router.get("/get_client_config/{player_id}", status_code=status.HTTP_200_OK, tags=["Players"])
async def get_client_config(db: db_dependency, player_id:str):
    player = db.query(Players).filter(Players.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail='Player not found')
    
    current_time = datetime.now(pytz.UTC)
    active_campaign = db.query(Campaigns).filter(
        Campaigns.enabled == True,
        Campaigns.start_date <= current_time,
        Campaigns.end_date >= current_time
    ).order_by(Campaigns.priority.desc()).first()
    
    if not active_campaign:
        return {
            "player_id": player.player_id,
            "active_campaigns": player.active_campaigns,
            "message": "No active campaigns available."
        }
    
    matchers = active_campaign.matchers
    min_level = matchers["level"]["min"]
    max_level = matchers["level"]["max"]

    if not (min_level <= player.level <= max_level):
        return {
            "player_id": player.player_id,
            "player_level": player.level,
            "campaign_min_level": min_level,
            "campaign_max_level": max_level,
            "message": "Player does not match the campaign criteria."
        }
    

    
    
    return player

@router.get("/player", status_code=status.HTTP_200_OK, tags=["Players"])
async def read_all_players(db: db_dependency):
    return db.query(Players).all()


@router.get("/player/{player_id}", status_code=status.HTTP_200_OK, tags=["Players"])
async def read_player(db: db_dependency, player_id:str):
    player = db.query(Players).filter(Players.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail='Player not found')
    return player

@router.post("/player", status_code=status.HTTP_201_CREATED, tags=["Players"])
async def create_player(db: db_dependency, player_request: PlayerRequest):
    player = Players(**player_request.model_dump())
    
    timezone = pytz.timezone('America/New_York')
    player.created = datetime.now(timezone)
    player.modified = datetime.now(timezone)
    
    db.add(player)
    db.commit()
    
@router.put("/player/{player_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Players"])
async def update_player(db: db_dependency, player_request: PlayerRequest, player_id:str):
    
    player = db.query(Players).filter(Players.player_id == player_id).first()
    
    if player is None:
        raise HTTPException(status_code=404, detail='Player not found.')
    
    updatable_data = player_request.model_dump()
    
    for field, value in updatable_data.items():
        setattr(player, field, value)
    
    timezone = pytz.timezone('America/New_York')
    player.modified = datetime.now(timezone)
    
    db.add(player)
    db.commit()
    
    
@router.delete("/player/{player_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Players"])
async def delete_player(db: db_dependency, player_id: str):

    player = db.query(Players).filter(Players.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail='Player not found.')
    
    db.query(Players).filter(Players.player_id == player_id).delete()
    db.commit()
    
    
    
    