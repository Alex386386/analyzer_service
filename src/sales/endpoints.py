from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_async_session
from src.core.utils import Tags, check_exists_and_get_or_return_error, check_token
from src.sales.crud import sales_crud
from src.sales.schemas import SalesDB

router = APIRouter(
    prefix="/sales",
    tags=[Tags.sales],
    dependencies=[Depends(check_token)],
)


@router.get(
    "/get-one/{sale_id}",
    response_model=SalesDB
)
async def get_sale_by_id(
    sale_id: int = Path(...), session: AsyncSession = Depends(get_async_session)
):
    return await check_exists_and_get_or_return_error(
        db_id=sale_id,
        crud=sales_crud,
        method_name="get",
        error="Объект продажи не найден!",
        status_code=status.HTTP_404_NOT_FOUND,
        session=session,
    )


@router.get(
    "/get-all",
    response_model=list[SalesDB]
)
async def get_all_sales(
    session: AsyncSession = Depends(get_async_session),
):
    try:
        return await sales_crud.get_multi(session=session)
    except Exception as e:
        raise HTTPException(
            detail=f"{e}",
            status_code=500,
        )