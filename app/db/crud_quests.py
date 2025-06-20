from sqlalchemy.orm import Session
from typing import Optional
from app.db.models import Quest, UserQuestBookmark
from app.db.schemas import QuestCreate, QuestUpdate

def create_quest(db: Session, quest: QuestCreate, author_id: int) -> Quest:
    db_quest = Quest(
        name=quest.name,
        synopsis=quest.synopsis,
        itinerary=quest.itinerary,
        reward=quest.reward,
        is_public=quest.is_public,
        author_id=author_id,
        start_location_id=quest.start_location_id,
        destination_id=quest.destination_id,
        interest_id=quest.interest_id,
        difficulty_id=quest.difficulty_id,
        quest_type_id=quest.quest_type_id,
        campaign_id=quest.campaign_id
    )
    db.add(db_quest)
    db.commit()
    db.refresh(db_quest)
    return db_quest

def get_quest(db: Session, quest_id: int) -> Quest | None:
    return db.query(Quest).filter(Quest.id == quest_id).first()

def get_quests(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    is_public: Optional[bool] = None,
    difficulty_id: Optional[int] = None,
    quest_type_id: Optional[int] = None,
    interest_id: Optional[int] = None,
    author_id: Optional[int] = None,
    campaign_id: Optional[int] = None,
    # Add other filter parameters as needed
) -> list[Quest]:
    query = db.query(Quest)
    if is_public is not None:
        query = query.filter(Quest.is_public == is_public)
    if difficulty_id is not None:
        query = query.filter(Quest.difficulty_id == difficulty_id)
    if quest_type_id is not None:
        query = query.filter(Quest.quest_type_id == quest_type_id)
    if interest_id is not None:
        query = query.filter(Quest.interest_id == interest_id)
    if author_id is not None:
        query = query.filter(Quest.author_id == author_id)
    if campaign_id is not None:
        query = query.filter(Quest.campaign_id == campaign_id)

    return query.offset(skip).limit(limit).all()

def update_quest(db: Session, db_quest: Quest, quest_in: QuestUpdate) -> Quest:
    update_data = quest_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_quest, key, value)
    db.add(db_quest)
    db.commit()
    db.refresh(db_quest)
    return db_quest

# The original errors on lines 84, 104, 115 of your previous crud_quests.py
# are likely resolved by this new structure, which avoids direct assignment
# of SQLAlchemy Column objects to integer variables or using them in `max()`.

def like_quest(db: Session, quest_id: int) -> Optional[Quest]:
    db_quest = get_quest(db, quest_id)
    if db_quest:
        db_quest.likes += 1  # type: ignore [assignment]
        db.add(db_quest)
        db.commit()
        db.refresh(db_quest)
    return db_quest

def get_quest_bookmark_by_user_and_quest(db: Session, user_id: int, quest_id: int) -> Optional[UserQuestBookmark]:
    return db.query(UserQuestBookmark).filter(
        UserQuestBookmark.user_id == user_id,
        UserQuestBookmark.quest_id == quest_id
    ).first()

def add_quest_bookmark_for_user(db: Session, user_id: int, quest_id: int) -> Optional[Quest]:
    db_quest = get_quest(db, quest_id)
    if db_quest:
        # Check if already bookmarked to prevent duplicate entries (though UniqueConstraint handles this)
        existing_bookmark = get_quest_bookmark_by_user_and_quest(db, user_id, quest_id)
        if not existing_bookmark:
            db_bookmark = UserQuestBookmark(user_id=user_id, quest_id=quest_id)
            db.add(db_bookmark)
            db_quest.bookmarks += 1  # type: ignore [assignment] # Increment denormalized count
            db.add(db_quest)
            db.commit()
            db.refresh(db_quest)
    return db_quest

def remove_quest_bookmark_for_user(db: Session, user_id: int, quest_id: int) -> Optional[Quest]:
    db_quest = get_quest(db, quest_id)
    if db_quest:
        db_bookmark = get_quest_bookmark_by_user_and_quest(db, user_id, quest_id)
        if db_bookmark:
            db.delete(db_bookmark)
            db_quest.bookmarks -= 1  # type: ignore [assignment] # Decrement denormalized count
            db.add(db_quest)
            db.commit()
            db.refresh(db_quest)
    return db_quest