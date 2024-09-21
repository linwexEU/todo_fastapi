from src.schemas.companies import CompaniesAdd, CompaniesFilters
from src.repositories.companies import CompaniesRepository 
from src.models.models import Companies


class CompaniesService: 
    def __init__(self, comp_repo: CompaniesRepository): 
        self.comp_repo: CompaniesRepository = comp_repo() 

    async def add(self, data: CompaniesAdd): 
        data_to_dict = data.model_dump() 
        await self.comp_repo.add(data_to_dict) 

    async def get_all(self) -> list[Companies]:
        result = await self.comp_repo.get_all()
        return result

    async def get_by_filters(self, filters: CompaniesFilters) -> list[Companies]:
        filters_to_dict = filters.model_dump(exclude_none=True)
        result = await self.comp_repo.get_by_filters(filters_to_dict)
        return result
