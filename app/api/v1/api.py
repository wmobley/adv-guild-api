from fastapi import APIRouter
from app.api.v1.endpoints import auth, campaigns, locations, quests, reference, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(quests.router, prefix="/quests", tags=["Quests"])
api_router.include_router(locations.router, prefix="/locations", tags=["locations"])
api_router.include_router(
    campaigns.router, prefix="/campaigns", tags=["Campaigns"]
)
api_router.include_router(
    reference.router, prefix="/reference", tags=["Reference Data"]
)