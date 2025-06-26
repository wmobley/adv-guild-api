#!/usr/bin/env python3
"""
Script to seed the database with sample data
"""
from pathlib import Path
import sys
import os
import json
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List, Union, cast

# Load environment variables from .env file
from dotenv import load_dotenv

# Get the project root directory (parent of scripts directory)
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'

# Load the .env file
load_dotenv(env_path)

# Set default values if not found in environment
os.environ.setdefault('DATABASE_URL', 'sqlite:///./adventure_guild.db')
os.environ.setdefault('JWT_SECRET_KEY', 'default-secret-key-for-development')
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
# Now import your app modules
from app.db.database import SessionLocal, engine
from app.db.models import Base, User, Location, Quest, Campaign, QuestType, Difficulty, Interest
from app.db import schemas, crud_locations, crud_quests, crud_campaigns, crud_reference_data
from app.core.password import get_password_hash

# Note: The `type: ignore` for `app.db.models` is a temporary measure if mypy
# complains about models not having certain attributes when imported here.
# It's better to fix the underlying model definitions if possible.


def get_or_create(db: Session, model: type, defaults: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Any:
    """
    Generic helper to get an object or create it if it doesn't exist.
    `kwargs` are used for the query.
    `defaults` are used for creating the new object.
    """
    instance = db.query(model).filter_by(**kwargs).first()
    if not instance:
        params = {**kwargs, **(defaults or {})}
        instance = model(**params)
        db.add(instance)
        db.flush()  # Flush to get ID for relationships before commit
    return instance


def create_sample_data() -> Dict[str, Any]:
    """Create sample data for the Adventure Guild API"""
    
    # Create tables
    Base.metadata.drop_all(bind=engine) # Drop all tables to ensure a clean slate and latest schema
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # Load all sample data from the JSON file
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_data.json')
    with open(data_path, 'r') as f:
        sample_data = json.load(f)

    try:
        # Create reference data first
        quest_types = {item['name']: get_or_create(db, QuestType, name=item['name']) for item in sample_data['quest_types']}
        difficulties = {item['name']: get_or_create(db, Difficulty, name=item['name']) for item in sample_data['difficulties']}
        interests = {item['name']: get_or_create(db, Interest, name=item['name']) for item in sample_data['interests']}

        # Create sample users
        users = {}
        for user_data in sample_data["users"]:
            user_email = user_data["email"]
            user_defaults = {
                "display_name": user_data["display_name"],
                "hashed_password": get_password_hash("password123"),
                "avatar_url": user_data.get("avatar_url"),
                "guild_rank": user_data.get("guild_rank"),
            }
            users[user_email] = get_or_create(db, User, email=user_email, defaults=user_defaults)

        # Create sample locations
        locations = {loc['name']: get_or_create(db, Location, name=loc['name'], defaults=loc) for loc in sample_data['locations']}

        # Create sample campaigns
        campaigns = {}
        default_author = next(iter(users.values())) # Get the first user as a default author
        for camp_data in sample_data['campaigns']:
            campaigns[camp_data['title']] = get_or_create(db, Campaign, title=camp_data['title'], defaults={'author_id': default_author.id, **camp_data})

        # Create sample quests
        quests = []
        for quest_data in sample_data['sample_quests']:
            # This is a simplified mapping. A more robust implementation would handle missing keys.
            start_location = locations.get("Edinburgh Castle")
            if not start_location:
                raise ValueError("Seed data is missing required location: Edinburgh Castle")
            quest_defaults = {
                "author_id": default_author.id,
                "start_location_id": start_location.id, # Example mapping
                "interest_id": interests.get("Supernatural Encounter", next(iter(interests.values()))).id,
                "difficulty_id": difficulties.get("Adventurer's Challenge", next(iter(difficulties.values()))).id,
                "quest_type_id": quest_types.get("Supernatural Encounter", next(iter(quest_types.values()))).id,
                **quest_data
            }
            quests.append(get_or_create(db, Quest, name=quest_data['name'], defaults=quest_defaults))
        
        db.commit()
        
        return {
            "message": "Sample data created successfully",
            "users": len(users),
            "locations": len(locations),
            "quests": len(quests),
            "campaigns": len(campaigns),
            "quest_types": len(quest_types),
            "difficulties": len(difficulties),
            "interests": len(interests)
        }
        
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    result = create_sample_data()
    print("Seed data creation completed:")
    for key, value in result.items():
        print(f"  {key}: {value}")