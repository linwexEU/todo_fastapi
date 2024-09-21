from pydantic import BaseModel 
from typing import Literal


class TasksAdd(BaseModel): 
    task: str
    status: Literal["Done", "In Process"]
    creator: int 
    assignee: int


class TasksEmployeeAddExpect(BaseModel): 
    task: str


class TasksAddResponse(BaseModel): 
    TaskHasCreated: bool


class TasksFilters(BaseModel): 
    id: int | None = None
    task: str | None = None 
    status: Literal["Done", "In Process", None] = None 
    creator: int | None = None 
    assignee: int | None = None 


class TasksUpdate(BaseModel): 
    TaskHasUpdated: bool


class TasksInfo(TasksEmployeeAddExpect): 
    id: int
    status: Literal["Done", "In Process"]


class TasksDelete(BaseModel): 
    TaskHasDeleted: bool 


class TasksEmployerAddExpect(BaseModel): 
    task: str
    assignee: int 


class AssigneeInfo(BaseModel): 
    id: int 
    username: str 
    status: Literal["Employee", "Employer"] 


class TasksWithAssignee(BaseModel): 
    id: int
    task: str 
    status: Literal["In Process", "Done"]
    assignee_user: AssigneeInfo
