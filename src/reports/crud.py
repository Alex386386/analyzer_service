from src.core.crud_foundation import CRUDBase
from src.core.models import AnalysisReport


class ReportCRUD(CRUDBase):
    pass


report_crud = ReportCRUD(AnalysisReport)
