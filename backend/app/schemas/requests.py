from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class StudyGroupUpdateDTO(BaseModel):
    location: Optional[str] = None
    meeting_time: Optional[datetime] = None
    meeting_day: Optional[str] = None
    
class StudyGroupCreateDTO(BaseModel):
    course_id: int
    semester_id: int
    location: str
    meeting_time: datetime
    meeting_day: Optional[str] = None
    
    
class StudyGroupRequestDTO(BaseModel):
    message: Optional[str] = None
    
class StudentUpdateRequestDTO(BaseModel):
    major: str | None = None
    class_year: str | None = None
    linkedin: str | None = None
    email: str | None = None
    

class CourseCreateRequest(BaseModel):
    department: str
    course_number: str
    professor: str
    semester_id: int