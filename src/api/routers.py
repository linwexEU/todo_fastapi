from src.api.users import router as users_router 
from src.api.tasks_employee import router as tasks_employee_router
from src.api.tasks_employer import router as tasks_employer_router 
from src.api.companies import router as companies_router


all_routers = [users_router, tasks_employee_router, tasks_employer_router, companies_router]
