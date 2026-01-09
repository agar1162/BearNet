from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, func, UniqueConstraint, Boolean
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Semester(Base):
    __tablename__ = "semesters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    term: Mapped[str] = mapped_column(
        String(16),  #
        nullable=False
    )

    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint("term", "year"),
    )

    courses: Mapped[list["Course"]] = relationship(
        back_populates="semester",
        cascade="all, delete-orphan"
    )


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    
    linkedin: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )
    
    class_year: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
        index=True
    )
    
    major: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )
    
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    sessions: Mapped[list["Session"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan"
    )

    study_groups: Mapped[list["StudyGroup"]] = relationship(
        secondary="study_group_members",
        back_populates="members"
    )
    
    courses: Mapped[list["Course"]] = relationship(
        secondary="student_courses",
        back_populates="students"
    )
    
    join_requests: Mapped[list["StudyGroupJoinRequest"]] = relationship(
        cascade="all, delete-orphan"
    )

class StudyGroupMember(Base):
    __tablename__ = "study_group_members"

    study_group_id: Mapped[int] = mapped_column(
        ForeignKey("studyGroups.id", ondelete="CASCADE"),
        primary_key=True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"),
        primary_key=True
    )


class StudyGroup(Base):
    __tablename__ = "studyGroups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    capacity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=5
    )
    
    isPrivate: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
        ) 
    
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    semester_id: Mapped[int] = mapped_column(
        ForeignKey("semesters.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    semester: Mapped["Semester"] = relationship()

    location: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    meeting_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    meeting_day: Mapped[str] = mapped_column(
        String(32),
        nullable=True
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    course: Mapped["Course"] = relationship(
        back_populates="study_groups"
    )

    members: Mapped[list["Student"]] = relationship(
        secondary="study_group_members",
        back_populates="study_groups"
    )
    
    join_requests: Mapped[list["StudyGroupJoinRequest"]] = relationship(
        cascade="all, delete-orphan"
    )
    
    @property
    def course_name(self) -> str:
        return f"{self.course.department} {self.course.course_number}"
        


class StudyGroupJoinRequest(Base):
    __tablename__ = "study_group_join_requests"

    id: Mapped[int] = mapped_column(primary_key=True)

    study_group_id: Mapped[int] = mapped_column(
        ForeignKey("studyGroups.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    
    message: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    
    student: Mapped["Student"] = relationship()
    
    study_group: Mapped["StudyGroup"] = relationship()


    __table_args__ = (
        UniqueConstraint("study_group_id", "student_id"),
    )

class StudentCourse(Base):
    __tablename__ = "student_courses"

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"),
        primary_key=True
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id", ondelete="CASCADE"),
        primary_key=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    semester_id: Mapped[int] = mapped_column(
        ForeignKey("semesters.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    semester: Mapped["Semester"] = relationship(
        back_populates="courses"
    )

    students: Mapped[list["Student"]] = relationship(
        secondary="student_courses",
        back_populates="courses"
    )

    department: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )
    
    course_number: Mapped[str] = mapped_column(
        String(16),
        nullable=False
    )
    
    professor: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    study_groups: Mapped[list["StudyGroup"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("department", "course_number", "semester_id"),
    )

class Session(Base):
    __tablename__ = "sessions"

    session_token: Mapped[str] = mapped_column(
        String(128),
        primary_key=True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )

    student: Mapped["Student"] = relationship(
        back_populates="sessions"
    )
