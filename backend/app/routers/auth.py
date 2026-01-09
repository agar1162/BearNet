from fastapi import APIRouter, Depends, status, Response, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timezone, datetime, timedelta

from app.deps.db import get_db
from app.schemas.auth import SignupRequest, LoginRequest
from app.schemas.models import Student, Session
from app.core.security import *

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    data: SignupRequest,
    response: Response, 
    db: AsyncSession = Depends(get_db),
):

    existing = await db.scalar(
        select(Student).where(Student.email == data.email)
    )
    
    if existing:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )
    
    student = Student(
        email=data.email,
        password_hash=hash_password(data.password)
    )
    
    db.add(student)
    await db.flush()  
    
    session_id = generate_session_token()
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)

    session = Session(
        session_token=session_id,
        student_id=student.id,
        expires_at=expires_at
    )
    
    db.add(session)
    await db.commit()

    response.set_cookie(
        key="sessionId",
        value=session_id,
        httponly=True,
        secure=True,  
        samesite="lax",
        max_age=60 * 60 * 24 * 7
    )

    return {
        "id": student.id,
        "email": student.email
    }


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    data: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    student = await db.scalar(
        select(Student).where(Student.email == data.email)
    )

    if not student or not verify_password(data.password, student.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_id = generate_session_token()
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)

    session = Session(
        session_token=session_id,
        student_id=student.id,
        expires_at=expires_at,
    )

    db.add(session)
    await db.commit()

    response.set_cookie(
        key="sessionId",
        value=session_id,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )

    return {"id": student.id, "email": student.email}



