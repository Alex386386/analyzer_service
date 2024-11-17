from src.core.crud_foundation import CRUDBase
from src.core.models import SalesData


class SalesDataCRUD(CRUDBase):

    pass

sales_crud = SalesDataCRUD(SalesData)
