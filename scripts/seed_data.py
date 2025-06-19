#!/usr/bin/env python3
"""
Script to seed the database with sample data
"""
import sys
import os
import json
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.db.database import engine
from app.db import models


def load_sample_data():
    """Load sample data from JSON file"""
    current_dir = os.path.dirname(os.path.dirname(__file__))
    json_path = os.path.join(current_dir, 'data', 'sample_data.json')
    
    with open(json_path, 'r') as f:
        return json.load(f)


def seed_reference_data(db: Session, data: dict):
    """Seed reference data tables"""
    print("Seeding reference data...")
    
    # Quest Types
    for item in data['quest_types']:
        if not db.query(models.QuestType).filter(models.QuestType.name == item['name']).first():
            quest_type = models.QuestType(name=item['name'])
            db.add(quest_type)
    
    # Difficulties
    for item in data['difficulties']:
        if not db.query(models.Difficulty).filter(models.Difficulty.name == item['name']).first():
            difficulty = models.Difficulty(name=item['name'])
            db.add(difficulty)
    
    # Interests
    for item in data['interests']:
        if not db.query(models.Interest).filter(models.Interest.name == item['name']).first():
            interest = models.Interest(name=item['name'])
            db.add(interest)
    
    db.commit()
    print("Reference data seeded successfully!")


def seed_locations(db: Session, data: dict):
    """Seed locations"""
    print("Seeding locations...")
    
    for item in data['locations']:
        if not db.query(models.Location).filter(models.Location.name == item['name']).first():
            location = models.Location(
                latitude=item['latitude'],
                longitude=item['longitude'],
                name=item['name'],
                real_world_inspiration=item['real_world_inspiration'],
                description=item['description']
            )
            db.add(location)
    
    db.commit()
    print("Locations seeded successfully!")


def seed_users(db: Session, data: dict):
    """Seed users"""
    print("Seeding users...")
    
    for item in data['users']:
        if not db.query(models.User).filter(models.User.email == item['email']).first():
            user = models.User(
                display_name=item['display_name'],
                email=item['email'],
                avatar_url=item['avatar_url'],
                guild_rank=item['guild_rank']
            )
            db.add(user)
    
    db.commit()
    print("Users seeded successfully!")


def seed_campaigns(db: Session, data: dict):
    """Seed campaigns"""
    print("Seeding campaigns...")
    
    # Get first user as author
    first_user = db.query(models.User).first()
    if not first_user:
        print("No users found, skipping campaigns")
        return
    
    for item in data['campaigns']:
        if not db.query(models.Campaign).filter(models.Campaign.title == item['title']).first():
            campaign = models.Campaign(
                title=item['title'],
                description=item['description'],
                author_id=first_user.id
            )
            db.add(campaign)
    
    db.commit()
    print("Campaigns seeded successfully!")


def seed_quests(db: Session, data: dict):
    """Seed sample quests"""
    print("Seeding quests...")
    
    # Get required reference data
    first_user = db.query(models.User).first()
    first_campaign = db.query(models.Campaign).first()
    default_interest = db.query(models.Interest).filter(models.Interest.name == "Ancient Mythology").first()
    default_difficulty = db.query(models.Difficulty).filter(models.Difficulty.name == "Adventurer's Challenge").first()
    default_quest_type = db.query(models.QuestType).filter(models.QuestType.name == "Mythological Pilgrimage").first()
    
    if not all([first_user, default_interest, default_difficulty, default_quest_type]):
        print("Missing required reference data, skipping quests")
        return
    
    # Location mapping for quests
    location_mapping = {
        "The Phantom of Edinburgh Castle": "Edinburgh Castle",
        "Decoding the Stonehenge Stargate": "Stonehenge Portal",
        "Athena's Lost Wisdom": "Acropolis of Athena",
        "Gladiator Spirits of the Colosseum": "Colosseum Arena",
        "The Pharaoh's Cosmic Key": "Great Pyramid Nexus"
    }
    
    for quest_data in data['sample_quests']:
        if not db.query(models.Quest).filter(models.Quest.name == quest_data['name']).first():
            # Find the start location
            location_name = location_mapping.get(quest_data['name'])
            start_location = None
            if location_name:
                start_location = db.query(models.Location).filter(models.Location.name == location_name).first()
            
            if not start_location:
                print(f"Location not found for quest: {quest_data['name']}, skipping...")
                continue
            
            quest = models.Quest(
                name=quest_data['name'],
                synopsis=quest_data['synopsis'],
                start_location_id=start_location.id,
                interest_id=default_interest.id,
                itinerary=quest_data['itinerary'],
                difficulty_id=default_difficulty.id,
                is_public=True,
                quest_type_id=default_quest_type.id,
                tags=quest_data['tags'],
                quest_giver=quest_data['quest_giver'],
                reward=quest_data['reward'],
                companions=quest_data['companions'],
                lore_excerpt=quest_data['lore_excerpt'],
                artifacts_discovered=quest_data['artifacts_discovered'],
                completed=False,
                author_id=first_user.id,
                media_urls=quest_data['media_urls'],
                campaign_id=first_campaign.id if first_campaign else None,
                likes=0,
                bookmarks=0
            )
            db.add(quest)
    
    db.commit()
    print("Quests seeded successfully!")


def main():
    """Main seeding function"""
    print("Starting database seeding...")
    
    # Load sample data
    try:
        data = load_sample_data()
    except FileNotFoundError:
        print("Error: sample_data.json not found in data/ directory")
        return
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return
    
    # Create database session
    db = Session(engine)
    
    try:
        # Seed data in order (respecting foreign key constraints)
        seed_reference_data(db, data)
        seed_locations(db, data)
        seed_users(db, data)
        seed_campaigns(db, data)
        seed_quests(db, data)
        
        print("Database seeding completed successfully!")
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()