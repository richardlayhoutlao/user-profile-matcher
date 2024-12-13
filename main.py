from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path
import models
from models import Players
from database import engine, SessionLocal
from starlette import status

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/", status_code=status.HTTP_200_OK)
async def read_all_players(db: db_dependency):
    return db.query(Players).all()


@app.get("/players/{player_id}", status_code=status.HTTP_200_OK)
async def read_player(db: db_dependency, player_id:int = Path(gt=0)):
    player_model = db.query(Players).filter(Players.player_id == player_id).first()
    if player_model is not None:
        return player_model
    raise HTTPException(status_code=404, detail='Player not found')
