from fastapi import FastAPI, Depends, status
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .deps.db import engine, get_db
from .deps.auth import get_current_student
from .schemas.models import Base, Student, Course, StudentCourse, StudyGroupMember, StudyGroup, StudyGroupJoinRequest
from .schemas.objects import CourseDTO, StudyGroupJoinRequestDTO, StudyGroupPreviewDTO
from .routers import auth, study_group, course
from .schemas.objects import StudentDTO, StudyGroupDTO
from .schemas.models import Student
from .schemas.requests import StudentUpdateRequestDTO

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield  

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(study_group.router)
app.include_router(course.router)


@app.get(
    "/", 
    response_model=StudentDTO,
    status_code=status.HTTP_200_OK
)
async def root(
    student: Student = Depends(get_current_student)
):
    return StudentDTO.model_validate(student)

@app.get("/study_groups", response_model=list[StudyGroupDTO])
async def list_study_groups(
    student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(StudyGroup)
        .join(StudyGroupMember)
        .where(StudyGroupMember.student_id == student.id)
    )
    return result.scalars().all()

@app.patch(
    "/profile", 
    response_model=StudentDTO,
    status_code=status.HTTP_200_OK
)
async def modify_profile(
    data: StudentUpdateRequestDTO,
    student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(student, field, value)

    await db.commit()
    await db.refresh(student)

    return StudentDTO.model_validate(student)

@app.get(
    "/courses",
    response_model=list[CourseDTO],
    status_code=status.HTTP_200_OK,
)
async def list_my_courses(
    student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Course)
        .join(StudentCourse)
        .where(StudentCourse.student_id == student.id)
        .order_by(Course.title)
    )

    courses = result.scalars().all()
    return courses


@app.get(
    "/requests",
    response_model=list[StudyGroupPreviewDTO],
    status_code=status.HTTP_200_OK,
)
async def list_my_requests(
    student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(StudyGroupJoinRequest)
        .where(StudyGroupJoinRequest.student_id == student.id)
        .options(
            selectinload(StudyGroupJoinRequest.study_group)
            .selectinload(StudyGroup.course)
        )
        .order_by(StudyGroupJoinRequest.created_at.desc())
    )


    return result.scalars().all()
