from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.db.db import Base


class Users(Base): 
    __tablename__ = "users" 

    id: Mapped[int] = mapped_column(primary_key=True, unique=True) 
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)  
    status: Mapped[str] = mapped_column(nullable=False) 
    company: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    creator_tasks = relationship("Tasks", foreign_keys="[Tasks.creator]", back_populates="creator_user")
    assigee_tasks = relationship("Tasks", foreign_keys="[Tasks.assignee]", back_populates="assignee_user")


class Tasks(Base): 
    __tablename__ = "tasks" 

    id: Mapped[int] = mapped_column(primary_key=True) 
    task: Mapped[str] = mapped_column(nullable=False, unique=True) 
    status: Mapped[str] = mapped_column(nullable=False) 
    creator: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    assignee: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    creator_user = relationship("Users", foreign_keys=[creator], back_populates="creator_tasks")
    assignee_user = relationship("Users", foreign_keys=[assignee], back_populates="assigee_tasks")


class Companies(Base): 
    __tablename__ = "companies" 

    id: Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str] = mapped_column(nullable=False, unique=True) 
    creator: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    