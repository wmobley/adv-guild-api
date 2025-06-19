#!/usr/bin/env python3
"""
Script to seed the database with sample data
"""
import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List, Union, cast

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.db.database import SessionLocal, engine
from app.db.models import Base, User, Location, Quest, Campaign, QuestType, Difficulty, Interest
from app.db import crud, schemas


def get_db() -> Session:
    db = SessionLocal()
    try:
        return db
    finally:
        pass  # Don't close here since we're returning the session


def create_sample_data() -> Dict[str, Any]:
    """Create sample data for the Adventure Guild API"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create reference data first
        quest_types_data = [
            "Dungeon Crawl",
            "Monster Hunt",
            "Escort Mission",
            "Treasure Hunt",
            "Investigation",
            "Rescue Mission"
        ]
        
        difficulties_data = [
            "Novice",
            "Apprentice", 
            "Journeyman",
            "Expert",
            "Master",
            "Legendary"
        ]
        
        interests_data = [
            "Combat",
            "Magic",
            "Stealth",
            "Diplomacy",
            "Exploration",
            "Crafting"
        ]
        
        # Create quest types
        quest_types: List[QuestType] = []
        for qt_name in quest_types_data:
            existing_qt = db.query(QuestType).filter(QuestType.name == qt_name).first()
            if not existing_qt:
                qt = crud.create_quest_type(db, qt_name)
                quest_types.append(qt)
            else:
                quest_types.append(existing_qt)
        
        # Create difficulties
        difficulties: List[Difficulty] = []
        for diff_name in difficulties_data:
            existing_diff = db.query(Difficulty).filter(Difficulty.name == diff_name).first()
            if not existing_diff:
                diff = crud.create_difficulty(db, diff_name)
                difficulties.append(diff)
            else:
                difficulties.append(existing_diff)
        
        # Create interests
        interests: List[Interest] = []
        for int_name in interests_data:
            existing_int = db.query(Interest).filter(Interest.name == int_name).first()
            if not existing_int:
                interest = crud.create_interest(db, int_name)
                interests.append(interest)
            else:
                interests.append(existing_int)
        
        # Create sample users
        users: List[User] = []
        
        # User 1
        existing_user1 = crud.get_user_by_email(db, "master@adventurers-guild.com")
        if not existing_user1:
            user_create1 = schemas.UserCreate(
                email="master@adventurers-guild.com",
                display_name="Guild Master Aldric"
            )
            user1 = crud.create_user(db, user_create1)
            users.append(user1)
        else:
            users.append(existing_user1)
        
        # User 2
        existing_user2 = crud.get_user_by_email(db, "knight@adventurers-guild.com")
        if not existing_user2:
            user_create2 = schemas.UserCreate(
                email="knight@adventurers-guild.com",
                display_name="Sir Galahad the Brave"
            )
            user2 = crud.create_user(db, user_create2)
            users.append(user2)
        else:
            users.append(existing_user2)
        
        # User 3
        existing_user3 = crud.get_user_by_email(db, "mage@adventurers-guild.com")
        if not existing_user3:
            user_create3 = schemas.UserCreate(
                email="mage@adventurers-guild.com",
                display_name="Archmage Merlin"
            )
            user3 = crud.create_user(db, user_create3)
            users.append(user3)
        else:
            users.append(existing_user3)
        
        # Create sample locations
        locations: List[Location] = []
        
        # Location 1
        existing_loc1 = db.query(Location).filter(Location.name == "Whispering Woods").first()
        if not existing_loc1:
            location_create1 = schemas.LocationCreate(
                name="Whispering Woods",
                description="A mysterious forest where ancient spirits dwell",
                latitude=45.5231,
                longitude=-122.6765
            )
            location1 = crud.create_location(db, location_create1)
            locations.append(location1)
        else:
            locations.append(existing_loc1)
        
        # Location 2
        existing_loc2 = db.query(Location).filter(Location.name == "Dragon's Peak").first()
        if not existing_loc2:
            location_create2 = schemas.LocationCreate(
                name="Dragon's Peak",
                description="A treacherous mountain where dragons are said to nest",
                latitude=46.8523,
                longitude=-121.7603
            )
            location2 = crud.create_location(db, location_create2)
            locations.append(location2)
        else:
            locations.append(existing_loc2)
        
        # Location 3
        existing_loc3 = db.query(Location).filter(Location.name == "Sunken Ruins").first()
        if not existing_loc3:
            location_create3 = schemas.LocationCreate(
                name="Sunken Ruins",
                description="Ancient underwater ruins filled with lost treasures",
                latitude=44.9778,
                longitude=-124.0618
            )
            location3 = crud.create_location(db, location_create3)
            locations.append(location3)
        else:
            locations.append(existing_loc3)
        
        # Create sample quests
        quests: List[Quest] = []
        
        if users and locations:  # Ensure we have users and locations
            # Find the related entities for Quest 1
            combat_interest = db.query(Interest).filter(Interest.name == "Combat").first()
            apprentice_difficulty = db.query(Difficulty).filter(Difficulty.name == "Apprentice").first()
            dungeon_quest_type = db.query(QuestType).filter(QuestType.name == "Dungeon Crawl").first()
            
            if combat_interest and apprentice_difficulty and dungeon_quest_type:
                quest_create1 = schemas.QuestCreate(
                    name="Clear the Goblin Cave",
                    synopsis="A group of goblins has taken residence in the old mine. Clear them out and secure the area.",
                    itinerary="""1. Meet with the mine foreman at the entrance
2. Explore the upper tunnels and clear out goblin scouts
3. Locate and defeat the goblin chieftain in the lower chambers
4. Secure any stolen goods and return them to the townspeople
5. Report back to the Guild with proof of completion"""
                    ,
                    reward="500 gold pieces",
                    is_public=True,
                    start_location_id=int(locations[0].id),
                    interest_id=int(combat_interest.id),
                    difficulty_id=int(apprentice_difficulty.id),
                    quest_type_id=int(dungeon_quest_type.id)
                )
                quest1 = crud.create_quest(db, quest_create1, int(users[0].id))
                quests.append(quest1)
            
            # Find the related entities for Quest 2
            magic_interest = db.query(Interest).filter(Interest.name == "Magic").first()
            expert_difficulty = db.query(Difficulty).filter(Difficulty.name == "Expert").first()
            treasure_quest_type = db.query(QuestType).filter(QuestType.name == "Treasure Hunt").first()
            
            if magic_interest and expert_difficulty and treasure_quest_type:
                quest_create2 = schemas.QuestCreate(
                    name="Retrieve the Lost Artifact",
                    synopsis="The Orb of Tidal Mastery, a powerful artifact capable of controlling water and weather, was lost when the ancient city of Aquatillia sank beneath the waves 500 years ago. Recent magical disturbances suggest the orb is still active and must be retrieved before it falls into the wrong hands.",
                    itinerary=
                        """Obtain underwater breathing equipment from the Guild's alchemist
                        Dive to the sunken ruins and navigate the flooded streets
                        Solve the ancient puzzles protecting the temple entrance
                        Defeat the guardian spirits that protect the orb
                        Safely extract the artifact and return it to the Guild vault""",
                    reward="1000 gold pieces",
                    is_public=True,
                    start_location_id=int(locations[2].id),
                    interest_id=int(magic_interest.id),
                    difficulty_id=int(expert_difficulty.id),
                    quest_type_id=int(treasure_quest_type.id)
                )
                quest2 = crud.create_quest(db, quest_create2, int(users[0].id))
                quests.append(quest2)
        
        # Create sample campaigns
        campaigns: List[Campaign] = []
        
        if users:  # Ensure we have users
            campaign_create = schemas.CampaignCreate(
                title="The Dragon's Awakening",
                description="A series of connected quests dealing with an ancient dragon's return"
            )
            campaign = crud.create_campaign(db, campaign_create, int(users[0].id))
            campaigns.append(campaign)
        
        db.commit()
        
        return {
            "message": "Sample data created successfully",
            "users_created": len(users),
            "locations_created": len(locations),
            "quests_created": len(quests),
            "campaigns_created": len(campaigns),
            "quest_types_created": len(quest_types),
            "difficulties_created": len(difficulties),
            "interests_created": len(interests)
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