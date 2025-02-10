from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
import enum
from datetime import datetime, time
from .base import Base, TimestampMixin

class DifficultyEnum(enum.Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

class Problem(Base, TimestampMixin):
    __tablename__ = "problems"

    problem_id = Column(Integer, primary_key=True)
    leetcode_number = Column(Integer, unique=True, nullable=False)
    title = Column(String, nullable=False)
    difficulty = Column(Enum(DifficultyEnum), nullable=False)
    first_study_date = Column(Date, nullable=False, default=datetime.utcnow().date)
    next_review_date = Column(Date, nullable=False, default=datetime.utcnow().date)
    stage = Column(Integer, nullable=False, default=0)  # 0-4 for 5 review stages
    is_active = Column(Boolean, nullable=False, default=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="problems")
    review_logs = relationship("ReviewLog", back_populates="problem")

class User(Base, TimestampMixin):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    notification_time = Column(Time, nullable=False, default=time(9, 0))  # Default 9:00
    timezone = Column(String, nullable=False, default="UTC")
    is_active = Column(Boolean, nullable=False, default=True)

    # Relationships
    problems = relationship("Problem", back_populates="user")
    review_logs = relationship("ReviewLog", back_populates="user")

class ReviewLog(Base, TimestampMixin):
    __tablename__ = "review_logs"

    review_id = Column(Integer, primary_key=True)
    problem_id = Column(Integer, ForeignKey("problems.problem_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    review_date = Column(Date, nullable=False, default=datetime.utcnow().date)
    stage = Column(Integer, nullable=False)
    completed = Column(Boolean, nullable=False, default=False)

    # Relationships
    problem = relationship("Problem", back_populates="review_logs")
    user = relationship("User", back_populates="review_logs") 