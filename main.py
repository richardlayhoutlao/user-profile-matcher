from fastapi import FastAPI
import models
from database import engine
from routers import players, campaigns

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(players.router)
app.include_router(campaigns.router)