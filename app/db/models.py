from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    avatar_url = Column(String(500), nullable=True)
    guild_rank = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    authored_quests = relationship("Quest", back_populates="author", foreign_keys="Quest.author_id")
    authored_campaigns = relationship("Campaign", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    following = relationship("Follow", foreign_keys="Follow.follower_id", back_populates="follower")
    # quest_bookmarks relationship will be added below
    followers = relationship("Follow", foreign_keys="Follow.followee_id", back_populates="followee")


class QuestType(Base):
    __tablename__ = "quest_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    quests = relationship("Quest", back_populates="quest_type")


class Difficulty(Base):
    __tablename__ = "difficulties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    quests = relationship("Quest", back_populates="difficulty")


class Interest(Base):
    __tablename__ = "interests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    quests = relationship("Quest", back_populates="interest")


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    name = Column(String(200), nullable=False)
    real_world_inspiration = Column(String(300), nullable=True)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)

    # Relationships
    start_quests = relationship("Quest", back_populates="start_location", foreign_keys="Quest.start_location_id")
    destination_quests = relationship("Quest", back_populates="destination", foreign_keys="Quest.destination_id")
    quest_log_entries = relationship("QuestLogEntry", back_populates="location")


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=True, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    author = relationship("User", back_populates="authored_campaigns")
    quests = relationship("Quest", back_populates="campaign")


class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    synopsis = Column(Text, nullable=True)
    start_location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    destination_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    interest_id = Column(Integer, ForeignKey("interests.id"), nullable=True)
    itinerary = Column(Text, nullable=True)  # JSON string
    difficulty_id = Column(Integer, ForeignKey("difficulties.id"), nullable=True)
    is_public = Column(Boolean, default=True)
    quest_type_id = Column(Integer, ForeignKey("quest_types.id"), nullable=True)
    tags = Column(String(500), nullable=True)
    quest_giver = Column(String(200), nullable=True)
    reward = Column(String(500), nullable=True)
    companions = Column(String(500), nullable=True)
    lore_excerpt = Column(Text, nullable=True)
    artifacts_discovered = Column(String(500), nullable=True)
    completed = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    media_urls = Column(JSON, nullable=True)  # Array of strings
    likes = Column(Integer, default=0)
    bookmarks = Column(Integer, default=0)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    author = relationship("User", back_populates="authored_quests", foreign_keys=[author_id])
    start_location = relationship("Location", back_populates="start_quests", foreign_keys=[start_location_id])
    destination = relationship("Location", back_populates="destination_quests", foreign_keys=[destination_id])
    interest = relationship("Interest", back_populates="quests")
    difficulty = relationship("Difficulty", back_populates="quests")
    quest_type = relationship("QuestType", back_populates="quests")
    campaign = relationship("Campaign", back_populates="quests")
    # user_bookmarks relationship will be added below
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


class UserQuestBookmark(Base):
    __tablename__ = "user_quest_bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quest_id = Column(Integer, ForeignKey("quests.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="quest_bookmarks")
    quest = relationship("Quest", back_populates="user_bookmarks")

    # Add unique constraint to ensure a user can bookmark a quest only once
    __table_args__ = (UniqueConstraint('user_id', 'quest_id', name='uq_user_quest_bookmark'),)


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


# Update User and Quest models with relationships to UserQuestBookmark
User.quest_bookmarks = relationship("UserQuestBookmark", back_populates="user", cascade="all, delete-orphan")
Quest.user_bookmarks = relationship("UserQuestBookmark", back_populates="quest", cascade="all, delete-orphan")

# Note regarding Quest.bookmarks column:
# The existing `Quest.bookmarks = Column(Integer, default=0)` is a simple counter.
# With the `UserQuestBookmark` table, this integer column can serve as a denormalized count
# for quick lookups, but you'll need to implement logic to keep it synchronized (e.g., using event listeners or application logic).
# Alternatively, you could remove this column and derive the count from `len(quest.user_bookmarks)` or a database query.