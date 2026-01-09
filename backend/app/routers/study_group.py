from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..deps.db import get_db
from ..schemas.models import Student, StudyGroup, StudyGroupJoinRequest
from ..deps.auth import get_current_student
from ..schemas.requests import StudyGroupUpdateDTO, StudyGroupCreateDTO, StudyGroupRequestDTO
from ..schemas.objects import StudyGroupDTO

router = APIRouter(prefix="/study-group", tags=["study-group"])

async def get_study_group_or_404(
    study_group_id: int,
    db: AsyncSession,
) -> StudyGroup:
    study_group = await db.scalar(
        select(StudyGroup)
        .where(StudyGroup.id == study_group_id)
        .options(
            selectinload(StudyGroup.members),
            selectinload(StudyGroup.course),
        )
    )

    if not study_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study group not found",
        )

    return study_group

@router.get(
    "/{study_group_id}", 
    status_code=status.HTTP_200_OK, 
    response_model=StudyGroupDTO
)
async def fetch_study_group_info(
    study_group_id: int, 
    db: AsyncSession = Depends(get_db),
):
    study_group = await get_study_group_or_404(study_group_id, db)
    
    return StudyGroupDTO.model_validate(study_group)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=StudyGroupDTO
)
async def create_study_group(
    data: StudyGroupCreateDTO,
    student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    group = StudyGroup(
        course_id=data.course_id,
        semester_id=data.semester_id,
        location=data.location,
        meeting_time=data.meeting_time,
        meeting_day=data.meeting_day,
        creator_id=student.id,
    )
    
    db.add(group)
    await db.commit()
    await db.refresh(group)
    return StudyGroupDTO.model_validate(group)

@router.post(
    "/{study_group_id}",
    status_code=status.HTTP_202_ACCEPTED
)
async def join_study_group(
    study_group_id: int,
    student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    study_group = await get_study_group_or_404(study_group_id, db)
    
    if student in study_group.members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already a member of this study group"
        )
        
    if study_group.isPrivate:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Study group is private"
        )
        
    
    if len(study_group.members) >= study_group.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Study group is full"
        )
    
    study_group.members.append(student)
    await db.commit()

    
@router.post(
    "/{study_group_id}/request",
    status_code=status.HTTP_201_CREATED
)
async def request_study_group(
    study_group_id: int,
    data: StudyGroupRequestDTO,
    student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    study_group = await get_study_group_or_404(study_group_id, db)
        
    if student in study_group.members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't Join Group Already In"
        )
        
    existing = await db.scalar(
        select(StudyGroupJoinRequest).where(
            StudyGroupJoinRequest.study_group_id == study_group.id,
            StudyGroupJoinRequest.student_id == student.id,
        )
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Join request already submitted",
        )
        
    request = StudyGroupJoinRequest(
        study_group_id= study_group.id,
        student_id = student.id,
        message= data.message
    )
    
    study_group.join_requests.append(request)
    await db.commit()


@router.post(
    "/{study_group_id}/request/{request_id}/accept",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=StudyGroupDTO
)
async def accept_student(
    study_group_id: int,
    request_id: int,
    student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    study_group = await get_study_group_or_404(study_group_id, db)

    if study_group.owner_id != student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners may accept join requests"
        )

    join_request = await db.scalar(
        select(StudyGroupJoinRequest)
        .where(
            StudyGroupJoinRequest.id == request_id,
            StudyGroupJoinRequest.study_group_id == study_group.id,
        )
        .options(selectinload(StudyGroupJoinRequest.student))
    )

    if not join_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Join request not found"
        )

    if join_request.student in study_group.members:
        await db.delete(join_request)
        await db.commit()
        return StudyGroupDTO.model_validate(study_group)

    if len(study_group.members) >= study_group.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Study group is full"
        )

    study_group.members.append(join_request.student)
    await db.delete(join_request)
    await db.commit()
    await db.refresh(study_group)

    return StudyGroupDTO.model_validate(study_group)

@router.delete(
    "/{study_group_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_study_group(
    study_group_id: int,
    student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    study_group = await get_study_group_or_404(study_group_id, db)

    if study_group.owner_id != student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not Owner Of This Study Group"
        )
    
    db.delete(study_group)
    await db.commit()    

@router.post(
    "/{study_group_id}/leave",
    status_code=status.HTTP_204_NO_CONTENT
)
async def leave_study_group(
    study_group_id: int,
    student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    study_group = await get_study_group_or_404(study_group_id, db)
    
    if student not in study_group.members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is not a member of this group"
        )
    
    if student.id == study_group.owner_id:
        remaining_members = [
            m for m in study_group.members if m.id != student.id
        ]

        if not remaining_members:
            await db.delete(study_group)
            await db.commit()
            return 
            

        new_owner = min(remaining_members, key=lambda m: m.id)
        study_group.owner_id = new_owner.id
    
    study_group.members.remove(student)
    await db.commit()


@router.post(
    "/{study_group_id}/kick/{kicked_member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_student_from_group(
    study_group_id: int,
    kicked_member_id: int,
    student: Student = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    
    study_group = await get_study_group_or_404(study_group_id, db)
    
    if student.id != study_group.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Owner Can Remove Members"
        )
        
    kicked_member = await db.scalar(
        select(Student)
        .where(Student.id == kicked_member_id)
    )
    
    if not kicked_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
        
    if kicked_member not in study_group.members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Requested Member Not In This Group"
        )
        
    if kicked_member.id == study_group.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owner cannot remove themselves from the group"
        )
    
    study_group.members.remove(kicked_member)
    await db.commit()