from fastapi import HTTPException, status


class BaseException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(self.status_code, self.detail)


class TokenHasBeenExpired(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token has been expired"


class UserNotFound(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User Not Found"


class CompanyAlreadyExist(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Company already exist"


class UserNotEmployer(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User is not employer"


class CantAssigneeTaskToEmployer(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "You can't create task for employer"


class UserNotEmployee(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User is not employee"


class TaskAlreadyExist(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Task already exist"


class TaskNotFound(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Task Not Found"


class CompanyNotFound(BaseException):
    status_code =  status.HTTP_404_NOT_FOUND
    detail = "Company Not Found"


class CantCreateTaskForEmployee(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Employee NOT IN YOUR COMPANY or you try to ADD TASK FOR EMPLOYER or Employee not exist"


class NotYourTask(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "This task don't belong to you"


class UserNameHasAlreadyExist(BaseException): 
    status_code = status.HTTP_409_CONFLICT 
    detail = "User with this NAME already exist"


class UserEmailHasAlreadyExist(BaseException): 
    status_code = status.HTTP_409_CONFLICT 
    detail = "User with this EMAIL already exist"

