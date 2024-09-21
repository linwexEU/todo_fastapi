from pydantic import BaseModel 


class CompaniesAdd(BaseModel): 
    name: str 
    creator: int 


class CompaniesAddExpected(BaseModel): 
    name: str


class CompaniesAddResponse(BaseModel): 
    CompanyHasCreated: bool 


class CompaniesAddUserResponse(BaseModel): 
    UserHasBeenAdded: bool


class AllCompaniesResponse(CompaniesAddExpected): 
    pass  


class CompaniesFilters(BaseModel):
    id: int | None = None
    name: str | None = None
    creator: int | None = None
