from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Campaigns
from database import SessionLocal
import pytz

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
    start_date: datetime
    end_date: datetime
    enabled: bool = Field(default=True)

@router.get("/campaign", status_code=status.HTTP_200_OK, tags=["Campaigns"])
async def read_all_campaigns(db: db_dependency):
    return db.query(Campaigns).all()


@router.get("/campaign/{campaign_id}", status_code=status.HTTP_200_OK, tags=["Campaigns"])
async def read_campaign(db: db_dependency, campaign_id:int = Path(gt=0)):
    campaign = db.query(Campaigns).filter(Campaigns.campaign_id == campaign_id).first()
    if campaign is None:
        raise HTTPException(status_code=404, detail='Campaign not found')
    return campaign

@router.post("/campaign", status_code=status.HTTP_201_CREATED, tags=["Campaigns"])
async def create_campaign(db: db_dependency, campaign_request: CampaignRequest):
    campaign = Campaigns(**campaign_request.model_dump())
    
    timezone = pytz.timezone('America/New_York')
    campaign.last_updated = datetime.now(timezone)
    
    db.add(campaign)
    db.commit()
    
@router.put("/campaign/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Campaigns"])
async def update_campaign(db: db_dependency, campaign_request: CampaignRequest, campaign_id:int = Path(gt=0)):
    
    campaign = db.query(Campaigns).filter(Campaigns.campaign_id == campaign_id).first()
    
    if campaign is None:
        raise HTTPException(status_code=404, detail='Campaign not found.')
    
    updatable_data = campaign_request.model_dump()
    
    for field, value in updatable_data.items():
        setattr(campaign, field, value)
    
    timezone = pytz.timezone('America/New_York')
    campaign.last_updated = datetime.now(timezone)
    
    db.add(campaign)
    db.commit()
    
    
@router.delete("/campaign/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Campaigns"])
async def delete_campaign(db: db_dependency, campaign_id: int = Path(gt=0)):

    campaign = db.query(Campaigns).filter(Campaigns.campaign_id == campaign_id).first()
    if campaign is None:
        raise HTTPException(status_code=404, detail='Campaign not found.')
    
    db.query(Campaigns).filter(Campaigns.campaign_id == campaign_id).delete()
    db.commit()
