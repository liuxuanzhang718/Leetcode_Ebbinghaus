from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session
from ..models.models import Problem, ReviewLog, User

class ReviewScheduler:
    # Review intervals in days for each stage
    REVIEW_INTERVALS = [0, 1, 2, 7, 15, 30]  # Day intervals for each stage
    MAX_STAGE = len(REVIEW_INTERVALS) - 1

    @staticmethod
    def calculate_next_review_date(current_stage: int, base_date: datetime = None) -> Optional[datetime]:
        """Calculate the next review date based on the current stage."""
        if current_stage > ReviewScheduler.MAX_STAGE:
            return None
        
        if base_date is None:
            base_date = datetime.utcnow()
        
        days = ReviewScheduler.REVIEW_INTERVALS[current_stage]
        return base_date + timedelta(days=days)

    @staticmethod
    def get_problems_for_review(db: Session, user_id: int, date: datetime = None) -> List[Problem]:
        """Get all problems that need to be reviewed on a specific date."""
        if date is None:
            date = datetime.utcnow().date()

        return (
            db.query(Problem)
            .filter(
                Problem.user_id == user_id,
                Problem.next_review_date <= date,
                Problem.is_active == True,
                Problem.stage <= ReviewScheduler.MAX_STAGE
            )
            .all()
        )

    @staticmethod
    def mark_review_completed(
        db: Session, 
        problem_id: int, 
        user_id: int,
        review_date: datetime = None
    ) -> Problem:
        """Mark a problem review as completed and schedule the next review."""
        if review_date is None:
            review_date = datetime.utcnow()

        problem = (
            db.query(Problem)
            .filter(Problem.problem_id == problem_id, Problem.user_id == user_id)
            .first()
        )
        
        if not problem:
            raise ValueError("Problem not found")

        # Create review log
        review_log = ReviewLog(
            problem_id=problem_id,
            user_id=user_id,
            review_date=review_date.date(),
            stage=problem.stage,
            completed=True
        )
        db.add(review_log)

        # Update problem stage and next review date
        problem.stage += 1
        next_review_date = ReviewScheduler.calculate_next_review_date(
            problem.stage, 
            review_date
        )
        
        if next_review_date:
            problem.next_review_date = next_review_date.date()
        else:
            problem.is_active = False  # All stages completed

        db.commit()
        return problem

    @staticmethod
    def postpone_review(
        db: Session,
        problem_id: int,
        user_id: int,
        days: int = 1
    ) -> Problem:
        """Postpone a problem review by specified number of days."""
        problem = (
            db.query(Problem)
            .filter(Problem.problem_id == problem_id, Problem.user_id == user_id)
            .first()
        )
        
        if not problem:
            raise ValueError("Problem not found")

        problem.next_review_date += timedelta(days=days)
        db.commit()
        return problem 