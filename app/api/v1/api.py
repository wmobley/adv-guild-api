from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, quests, locations, campaigns, reference

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(quests.router, prefix="/quests", tags=["quests"])
api_router.include_router(locations.router, prefix="/locations", tags=["locations"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(reference.router, prefix="/reference", tags=["reference-data"])