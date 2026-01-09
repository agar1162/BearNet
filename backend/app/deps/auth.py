from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import  datetime
from typing import List

from app.deps.db import get_db
from app.schemas.models import Student, Session, StudyGroup
from app.core.security import *


async def get_current_student(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Student:
    token = request.cookies.get("sessionId")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = await db.scalar(
        select(Session)
        .where(Session.session_token == token)
    )

    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session expired")

    return session.student

