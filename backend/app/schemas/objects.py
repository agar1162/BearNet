from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


# ---------- Semester ----------

class SemesterDTO(BaseModel):
    id: int
    term: str
    year: int


    class Config:
        from_attributes = True


# ---------- Course ----------

class CourseDTO(BaseModel):
    id: int
    department: str
    course_number: str
    professor: str
    semester: SemesterDTO

    class Config:
        from_attributes = True


# ---------- Student (public-facing subset) ----------

class StudentDTO(BaseModel):
    id: int
    email: str
    major: Optional[str]
    class_year: Optional[str]
    linkedin: Optional[str]
    

    class Config:
        from_attributes = True


# ---------- Study Group ----------

class StudyGroupDTO(BaseModel):
    id: int
    owner_id: int
    location: str
    course: CourseDTO
    meeting_time: datetime
    meeting_day: Optional[str] = None
    members: List[StudentDTO]
    capacity: int

    class Config:
        from_attributes = True
        
class StudyGroupPreviewDTO(BaseModel):
    id: int
    location: str
    meeting_time: datetime
    meeting_day: Optional[str] = None
    capacity: int
    course_name: str

    class Config:
        from_attributes = True


class StudyGroupJoinRequestDTO(BaseModel):
    id: int
    created_at: datetime
    message: Optional[str] = None
    study_group: StudyGroupPreviewDTO

    class Config:
        from_attributes = True
        


