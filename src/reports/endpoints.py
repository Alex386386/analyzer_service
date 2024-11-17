from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_async_session
from src.core.utils import Tags, check_exists_and_get_or_return_error, check_token
from src.reports.crud import report_crud
from src.reports.schemas import ReportDB

router = APIRouter(
    prefix="/report",
    tags=[Tags.reports],
    dependencies=[Depends(check_token)],
)


@router.get(
    "/get-one/{report_id}",
    response_model=ReportDB
)
async def get_report_by_id_for_admin(
    report_id: int = Path(...), session: AsyncSession = Depends(get_async_session)
):
    return await check_exists_and_get_or_return_error(
        db_id=report_id,
        crud=report_crud,
        method_name="get",
        error="Такого отчёта нет в системе!",
        status_code=status.HTTP_404_NOT_FOUND,
        session=session,
    )


@router.get(
    "/get-all",
    response_model=list[ReportDB]
)
async def get_all_reports(
    session: AsyncSession = Depends(get_async_session),
):
    try:
        return await report_crud.get_multi(session=session)
    except Exception as e:
        raise HTTPException(
            detail=f"{e}",
            status_code=500,
        )
