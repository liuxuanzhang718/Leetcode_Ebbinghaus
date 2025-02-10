from celery import Celery
from celery.schedules import crontab
from sqlalchemy.orm import Session
from datetime import datetime
import pytz

from .core.config import settings
from .db.session import SessionLocal
from .models.models import User, Problem
from .core.review_scheduler import ReviewScheduler
from .services.email_service import EmailService

celery = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

@celery.task
def send_daily_reminders():
    """Send daily review reminders to all active users."""
    db = SessionLocal()
    try:
        # Get all active users
        users = db.query(User).filter(User.is_active == True).all()
        
        for user in users:
            # Convert current time to user's timezone
            user_tz = pytz.timezone(user.timezone)
            user_time = datetime.now(user_tz)
            
            # Check if it's notification time for this user
            if user_time.hour == user.notification_time.hour and \
               user_time.minute == user.notification_time.minute:
                
                # Get problems for review
                problems = ReviewScheduler.get_problems_for_review(
                    db, user.user_id, user_time
                )
                
                if problems:
                    # Send email notification
                    EmailService.send_review_reminder(user, problems)
    finally:
        db.close()

@celery.task
def cleanup_completed_reviews():
    """Clean up completed reviews and update problem stages."""
    db = SessionLocal()
    try:
        # Get all problems that have completed all stages
        completed_problems = (
            db.query(Problem)
            .filter(
                Problem.stage > ReviewScheduler.MAX_STAGE,
                Problem.is_active == True
            )
            .all()
        )
        
        for problem in completed_problems:
            problem.is_active = False
        
        db.commit()
    finally:
        db.close()

# Schedule periodic tasks
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Send reminders every minute (will check user's preferred time)
    sender.add_periodic_task(
        crontab(minute='*'),
        send_daily_reminders.s(),
        name='send-daily-reminders'
    )
    
    # Clean up at midnight
    sender.add_periodic_task(
        crontab(hour=0, minute=0),
        cleanup_completed_reviews.s(),
        name='cleanup-completed-reviews'
    ) 