from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from database import SessionLocal
from sqlalchemy.orm import Session
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
    name: str = Field(min_length=3)
    game: str = Field(min_length=3)
    priority: int = Field(gt=0)
    enabled: bool
    player_id: int = Field(gt=0)


@router.get("/campaign", status_code=status.HTTP_200_OK, tags=["Campaigns"])
async def read_all_campaigns(db: db_dependency):
    return db.query(Campaigns).all()

@router.get("/campaign/{campaign_id}", status_code=status.HTTP_200_OK, tags=["Campaigns"])
async def read_campaign(db: db_dependency, campaign_id: int = Path(gt=0)):
    campaign = db.query(Campaigns).filter(Campaigns.campaign_id == campaign_id).first()
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.post("/campaign", status_code=status.HTTP_201_CREATED, tags=["Campaigns"])
async def create_campaign(db: db_dependency, campaign_request: CampaignRequest):
    campaign = Campaigns(**campaign_request.model_dump())
    db.add(campaign)
    db.commit()
    return campaign

@router.put("/campaign/{campaign_id}", status_code=status.HTTP_200_OK, tags=["Campaigns"])
async def update_campaign(
    db: db_dependency,
    campaign_request: CampaignRequest,
    campaign_id: int = Path(gt=0),
):
    campaign = db.query(Campaigns).filter(Campaigns.campaign_id == campaign_id).first()
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign.name = campaign_request.name
    campaign.game = campaign_request.game
    campaign.priority = campaign_request.priority
    campaign.enabled = campaign_request.enabled
    campaign.player_id = campaign_request.player_id

    db.commit()
    return campaign

@router.delete("/campaign/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Campaigns"])
async def delete_campaign(db: db_dependency, campaign_id: int = Path(gt=0)):
    campaign = db.query(Campaigns).filter(Campaigns.campaign_id == campaign_id).first()
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")

    db.delete(campaign)
    db.commit()