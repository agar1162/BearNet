from fastapi import APIRouter, status, Depends, HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from ..deps.auth import get_current_student
from ..deps.db import get_db
from ..schemas.objects import CourseDTO
from ..schemas.models import Course, StudentCourse, Student
from ..schemas.requests import CourseCreateRequest


router = APIRouter(prefix="/course", tags=["course"])


@router.get(
    "/search",
    response_model=list[CourseDTO],
    status_code=status.HTTP_200_OK
)
async def autofill_search(
    q: str,
    db: AsyncSession = Depends(get_db),
):
    if len(q.strip()) < 2:
        return []

    query = q.strip().lower()

    result = await db.execute(
        select(Course)
        .where(
            (Course.department.ilike(f"%{query}%")) |
            (Course.course_number.ilike(f"%{query}%")) |
            (Course.professor.ilike(f"%{query}%"))
        )
        .order_by(Course.department, Course.course_number)
        .limit(10)
    )

    return result.scalars().all()

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CourseDTO
)
async def add_course(
    data: CourseCreateRequest,
    db: AsyncSession = Depends(get_db)
):  
    existing = db.scalar(
        select(Course)
        .where(
            (Course.course_number == data.course_number) &
            (Course.department == data.department)
        )
    )
    
    if existing:
        return CourseDTO.model_validate(existing)
    
    course = Course(
        department=data.department,
        course_number=data.course_number,
        professor=data.professor,
        semester_id=data.semester_id,
    )
    
    db.add(course)
    await db.commit()
    await db.refresh(course)
    
    return CourseDTO.model_validate(course)

