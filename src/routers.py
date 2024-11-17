from fastapi import APIRouter

from src.reports.endpoints import router as report_router
from src.sales.endpoints import router as sales_router

main_router = APIRouter(prefix="/api")
main_router.include_router(report_router)
main_router.include_router(sales_router)
