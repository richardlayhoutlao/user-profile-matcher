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

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_players(db: db_dependency):
    return db.query(Players).all()


@router.get("/player/{player_id}", status_code=status.HTTP_200_OK)
async def read_player(db: db_dependency, player_id:int = Path(gt=0)):
    player_model = db.query(Players).filter(Players.player_id == player_id).first()
    if player_model is not None:
        return player_model
    raise HTTPException(status_code=404, detail='Player not found')

@router.post("/player", status_code=status.HTTP_201_CREATED)
async def create_player(db: db_dependency, player_request: PlayerRequest):
    player_model = Players(**player_request.model_dump())
    
    db.add(player_model)
    db.commit()
    
@router.put("/player/{player_id}", status_code=status.HTTP_201_CREATED)
async def update_player(db: db_dependency, player_request: PlayerRequest, player_id:int = Path(gt=0)):
    
    player_model = db.query(Players).filter(Players.player_id == player_id).first()
    
    if player_model is None:
        raise HTTPException(status_code=404, detail='Player not found.')
    
    player_model.name = player_request.name
    player_model.total_spent = player_request.total_spent
    
    db.add(player_model)
    db.commit()
    
    
@router.delete("/player/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(db: db_dependency, player_id: int = Path(gt=0)):

    player_model = db.query(Players).filter(Players.player_id == player_id).first()
    if player_model is None:
        raise HTTPException(status_code=404, detail='Player not found.')
    
    db.query(Players).filter(Players.player_id == player_id).delete()
    db.commit()