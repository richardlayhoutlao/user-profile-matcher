from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field
import pytz
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Campaigns, Players
from database import SessionLocal

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
    total_spent: int = Field(gt= 0)
    modified : datetime
    last_session : datetime
    total_spent : int = Field(gt= 0)
    total_refund : int = Field(gt= 0)
    total_transactions : int = Field(gt= 0)
    last_purchase : datetime
    active_campaigns: list[str]  # List of active campaign IDs
    devices: list[Device]
    level : int = Field(gt= 0)
    xp : int = Field(gt= 0)
    total_playtime : int = Field(gt= 0)
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