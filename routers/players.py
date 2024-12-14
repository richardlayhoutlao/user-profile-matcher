from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Players
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

class PlayerRequest(BaseModel):
    name: str = Field(min_length= 3)
    total_spent: int = Field(gt= 0)

@router.get("/player", status_code=status.HTTP_200_OK, tags=["Players"])
async def read_all_players(db: db_dependency):
    return db.query(Players).all()


@router.get("/player/{player_id}", status_code=status.HTTP_200_OK, tags=["Players"])
async def read_player(db: db_dependency, player_id:int = Path(gt=0)):
    player = db.query(Players).filter(Players.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail='Player not found')
    return player

@router.post("/player", status_code=status.HTTP_201_CREATED, tags=["Players"])
async def create_player(db: db_dependency, player_request: PlayerRequest):
    player = Players(**player_request.model_dump())
    db.add(player)
    db.commit()
    return player
    
@router.put("/player/{player_id}", status_code=status.HTTP_201_CREATED, tags=["Players"])
async def update_player(db: db_dependency, player_request: PlayerRequest, player_id:int = Path(gt=0)):
    
    player = db.query(Players).filter(Players.player_id == player_id).first()
    
    if player is None:
        raise HTTPException(status_code=404, detail='Player not found.')
    
    player.name = player_request.name
    player.total_spent = player_request.total_spent
    
    db.add(player)
    db.commit()
    return player
    
    
@router.delete("/player/{player_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Players"])
async def delete_player(db: db_dependency, player_id: int = Path(gt=0)):

    player = db.query(Players).filter(Players.player_id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail='Player not found.')
    
    db.query(Players).filter(Players.player_id == player_id).delete()
    db.commit()
