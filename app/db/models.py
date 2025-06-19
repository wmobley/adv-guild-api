from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True)
    avatar_url = Column(String(255))
    guild_rank = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    authored_quests = relationship("Quest", back_populates="author")
    authored_campaigns = relationship("Campaign", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    following = relationship("Follow", foreign_keys="Follow.follower_id", back_populates="follower")
    followers = relationship("Follow", foreign_keys="Follow.followee_id", back_populates="followee")


class QuestType(Base):
    __tablename__ = "quest_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)

    quests = relationship("Quest", back_populates="quest_type")


class Difficulty(Base):
    __tablename__ = "difficulties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)

    quests = relationship("Quest", back_populates="difficulty")


class Interest(Base):
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)

    quests = relationship("Quest", back_populates="interest")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    name = Column(String(100))
    real_world_inspiration = Column(String(200))
    description = Column(Text)

    # Relationships
    quests_starting_here = relationship("Quest", foreign_keys="Quest.start_location_id", back_populates="start_location")
    quests_ending_here = relationship("Quest", foreign_keys="Quest.destination_id", back_populates="destination")
    quest_log_entries = relationship("QuestLogEntry", back_populates="location")


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    author = relationship("User", back_populates="authored_campaigns")
    quests = relationship("Quest", back_populates="campaign")


class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    synopsis = Column(Text, nullable=False)
    start_location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    destination_id = Column(Integer, ForeignKey("locations.id"))
    interest_id = Column(Integer, ForeignKey("interests.id"), nullable=False)
    itinerary = Column(Text, nullable=False)  # JSON string
    difficulty_id = Column(Integer, ForeignKey("difficulties.id"), nullable=False)
    is_public = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    quest_type_id = Column(Integer, ForeignKey("quest_types.id"), nullable=False)
    tags = Column(String(500))
    quest_giver = Column(String(100))
    reward = Column(String(500))
    companions = Column(String(500))
    lore_excerpt = Column(Text)
    artifacts_discovered = Column(String(500))
    completed = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey("users.id"))
    media_urls = Column(JSON)  # Array of strings
    likes = Column(Integer, default=0)
    bookmarks = Column(Integer, default=0)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))

    # Relationships
    author = relationship("User", back_populates="authored_quests")
    start_location = relationship("Location", foreign_keys=[start_location_id], back_populates="quests_starting_here")
    destination = relationship("Location", foreign_keys=[destination_id], back_populates="quests_ending_here")
    interest = relationship("Interest", back_populates="quests")
    difficulty = relationship("Difficulty", back_populates="quests")
    quest_type = relationship("QuestType", back_populates="quests")
    campaign = relationship("Campaign", back_populates="quests")
    comments = relationship("Comment", back_populates="quest")


class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    followee_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followee = relationship("User", foreign_keys=[followee_id], back_populates="followers")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    quest_id = Column(Integer, ForeignKey("quests.id"), nullable=False)

    # Relationships
    author = relationship("User", back_populates="comments")
    quest = relationship("Quest", back_populates="comments")


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    icon_url = Column(String(255))


class QuestLogEntry(Base):
    __tablename__ = "quest_log_entries"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    note = Column(Text, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)

    # Relationships
    location = relationship("Location", back_populates="quest_log_entries")