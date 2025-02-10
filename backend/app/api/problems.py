from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from ..db.session import get_db
from ..models.models import Problem, User
from ..services.leetcode_api import LeetCodeAPI
from .auth import get_current_user, oauth2_scheme

router = APIRouter()

class AddProblemRequest(BaseModel):
    problem_number: int

@router.get("", dependencies=[Depends(oauth2_scheme)])
async def get_problems(
    difficulty: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all problems for the current user."""
    query = db.query(Problem).filter(Problem.user_id == current_user.user_id)
    
    if difficulty:
        query = query.filter(Problem.difficulty == difficulty)
    if status:
        if status.lower() == "active":
            query = query.filter(Problem.is_active == True)
        elif status.lower() == "completed":
            query = query.filter(Problem.is_active == False)
    
    total = query.count()
    problems = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "problems": problems
    }

@router.post("")
async def add_problem(
    request: AddProblemRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a new problem to review system."""
    # Validate problem number
    problem_details = LeetCodeAPI.get_problem_details(request.problem_number)
    if not problem_details:
        raise HTTPException(status_code=404, detail="Problem not found on LeetCode")

    # Check if problem already exists for user
    existing_problem = (
        db.query(Problem)
        .filter(
            Problem.leetcode_number == request.problem_number,
            Problem.user_id == current_user.user_id
        )
        .first()
    )
    if existing_problem:
        raise HTTPException(
            status_code=400,
            detail="Problem already exists in your review list"
        )

    # Create new problem
    new_problem = Problem(
        leetcode_number=problem_details["leetcode_number"],
        title=problem_details["title"],
        difficulty=problem_details["difficulty"],
        user_id=current_user.user_id,
        first_study_date=datetime.utcnow().date(),
        next_review_date=datetime.utcnow().date(),
        stage=0
    )
    
    db.add(new_problem)
    db.commit()
    db.refresh(new_problem)
    
    return new_problem

@router.get("/stats", dependencies=[Depends(oauth2_scheme)])
async def get_problem_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get problem statistics for the current user."""
    total_problems = db.query(Problem).filter(Problem.user_id == current_user.user_id).count()
    active_problems = db.query(Problem).filter(
        Problem.user_id == current_user.user_id,
        Problem.is_active == True
    ).count()
    completed_problems = total_problems - active_problems

    difficulty_stats = (
        db.query(Problem.difficulty, func.count(Problem.problem_id))
        .filter(Problem.user_id == current_user.user_id)
        .group_by(Problem.difficulty)
        .all()
    )

    difficulty_counts = {
        difficulty: count for difficulty, count in difficulty_stats
    }

    return {
        "total_problems": total_problems,
        "active_problems": active_problems,
        "completed_problems": completed_problems,
        "difficulty_distribution": difficulty_counts
    }

@router.get("/review")
async def get_review_problems(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get problems that need to be reviewed today."""
    today = datetime.utcnow().date()
    
    problems = (
        db.query(Problem)
        .filter(
            Problem.user_id == current_user.user_id,
            Problem.next_review_date <= today,
            Problem.is_active == True
        )
        .all()
    )
    
    return problems

@router.post("/{problem_id}/complete")
async def complete_review(
    problem_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a problem review as completed."""
    problem = (
        db.query(Problem)
        .filter(
            Problem.problem_id == problem_id,
            Problem.user_id == current_user.user_id
        )
        .first()
    )
    
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    if problem.stage >= 5:  # All stages completed
        problem.is_active = False
    else:
        problem.stage += 1
        next_review = datetime.utcnow().date() + timedelta(days=[1, 2, 4, 7, 15][problem.stage - 1])
        problem.next_review_date = next_review
    
    db.commit()
    db.refresh(problem)
    
    return problem

@router.post("/{problem_id}/postpone")
async def postpone_review(
    problem_id: int,
    days: int = Query(1, ge=1, le=30),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Postpone a problem review."""
    problem = (
        db.query(Problem)
        .filter(
            Problem.problem_id == problem_id,
            Problem.user_id == current_user.user_id
        )
        .first()
    )
    
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    problem.next_review_date = datetime.utcnow().date() + timedelta(days=days)
    db.commit()
    db.refresh(problem)
    
    return problem 