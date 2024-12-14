from typing import Annotated
from fastapi import APIRouter
from pydantic import BaseModel, Field
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from models import Campaigns
from starlette import status

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

class CampaignRequest(BaseModel):
    name: str = Field(min_length= 3)
    game: str = Field(min_length= 3)
    priority: int = Field(gt= 0)
    enabled: bool
    
    
@router.post("/campaign", status_code=status.HTTP_201_CREATED)
async def create_campaign(db: db_dependency, campaign_request: CampaignRequest):
    campaign_model = Campaigns(**campaign_request.model_dump())
    
    db.add(campaign_model)
    db.commit()