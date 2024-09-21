from src.utils.repository import SQLAlchemyRepository 
from src.models.models import Companies 


class CompaniesRepository(SQLAlchemyRepository): 
    model = Companies 
