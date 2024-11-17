import os

from celery import Celery
from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy.orm import Session

from src.core.db import SessionLocal
from src.core.models import SalesData, AnalysisReport
from src.logger import logger

load_dotenv(".env")

celery = Celery(
    __name__,
    broker=os.getenv("REDIS_CONNECT_URL"),
    backend=os.getenv("REDIS_CONNECT_URL"),
    broker_connection_retry_on_startup=True
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_sales_analysis(prompt):
    try:
        response = client.chat.completions.with_raw_response.create(
            messages=[{
                "role": "user",
                "content": prompt,
            }],
            model=os.getenv("NAME_OF_API_MODEL"),
        )
        completion = response.parse()
        logger.info(f"Ответ от OpenAI: {completion['choices'][0]['message']['content']}")
        return completion['choices'][0]['message']['content'].strip()
    except Exception as e:
        logger.error(f"Ошибка при запросе к OpenAI: {e}")
        return None


@celery.task
def process_sales_data(sales_records: str, date: str):
    db: Session = SessionLocal()
    try:
        total_revenue = 0
        for record in sales_records:
            total_revenue += record['quantity'] * record['price']

            sale = SalesData(
                product_id=record['product_id'],
                name=record['name'],
                quantity=record['quantity'],
                price=record['price'],
                category=record['category']
            )
            db.add(sale)
        db.commit()

        top_products = sorted(sales_records, key=lambda x: x['quantity'], reverse=True)[:3]
        top_products_str = ", ".join([f"{prod['name']} ({prod['quantity']} шт.)" for prod in top_products])
        categories = {record['category']: 0 for record in sales_records}
        for record in sales_records:
            categories[record['category']] += record['quantity']
        category_distribution = ", ".join([f"{k}: {v}" for k, v in categories.items()])

        prompt = (
            f"Проанализируй данные о продажах за {date}:\n"
            f"1. Общая выручка: {total_revenue}\n"
            f"2. Топ-3 товара по продажам: {top_products_str}\n"
            f"3. Распределение по категориям: {category_distribution}\n\n"
            "Составь краткий аналитический отчет с выводами и рекомендациями."
        )

        response = get_sales_analysis(prompt)
        llm_response = AnalysisReport(
            date=date,
            start_prompt=prompt,
            report=response
        )
        db.add(llm_response)
        db.commit()

    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка: {e}")
    finally:
        db.close()
