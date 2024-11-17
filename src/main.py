from contextlib import asynccontextmanager
from http import HTTPStatus
from xml.etree import ElementTree

from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from redis.asyncio import Redis

from src.celery_tasks import process_sales_data
from src.core.config import settings
from src.core.utils import log_and_raise_error, check_token, get_redis_client
from src.logger import logger
from src.routers import main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not settings.test:
        app.state.redis_client = Redis(
            host="redis",
            port=6379,
            db=0,
            password=settings.redis_password,
            decode_responses=True
        )
    logger.info("Произведено подключение к редис.")
    yield
    if not settings.test:
        await app.state.redis_client.close()
    logger.info("Редис отключен.")


app = FastAPI(lifespan=lifespan)

app.include_router(main_router)


@app.post(
    "/",
    dependencies=[Depends(check_token)],
)
async def analyze_sales(
    request: Request,
    redis_client=Depends(get_redis_client)
):
    xml_data = await request.body()

    root = ElementTree.fromstring(xml_data)
    date = root.attrib.get('date')

    if redis_client:
        if await redis_client.exists(date):
            return JSONResponse(
                {"message": "Статистика за эту дату уже собрана."},
                status_code=HTTPStatus.OK
            )

    sales_records: list = []
    products = root.find('products')

    if products is not None:
        for product in products.findall('product'):
            try:
                product_id = int(product.find('id').text)
                name = product.find('name').text
                quantity = int(product.find('quantity').text)
                price = float(product.find('price').text)
                category = product.find('category').text

                if any([product_id, name, quantity, price, category]) is None:
                    raise AttributeError("Данные элемента некорректные, все элементы должны быть в наличии!")
                elif quantity <= 0:
                    raise ValueError("Значение количества элемента должно быть больше чем 0.")

                sales_records.append(
                    {
                        'product_id': product_id,
                        'name': name,
                        'quantity': quantity,
                        'price': price,
                        'category': category
                    }
                )
            except (AttributeError, ValueError) as e:
                logger.error(
                    f"Некорректные данные в продукте: {ElementTree.tostring(product, encoding='utf-8').decode('utf-8')}. Ошибка: {e}"
                )
                continue
    elif products is None:
        log_and_raise_error(
            message_log="В запросе отсутствуют данные!",
            message_error="В запросе отсутствуют данные!",
            status_code=HTTPStatus.BAD_REQUEST
        )

    task = process_sales_data.delay(sales_records=sales_records, date=date)

    if redis_client:
        await redis_client.set(date, "filer", ex=settings.cache_life_period)
    return JSONResponse({"task_id": task.id})
