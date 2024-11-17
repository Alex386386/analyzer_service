from httpx import AsyncClient


async def test_particular_report_in_db(get_test_headers, client: AsyncClient):
    """
    Проверка как отрабатывает получение конкретного отчёта из БД по id.
    """
    response = await client.get(
        "/api/report/get-one/1", headers=get_test_headers
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data == {"detail": "Такого отчёта нет в системе!"}


async def test_reports_in_db(get_test_headers, client: AsyncClient):
    """
    Получение отчётов из БД.
    """
    response = await client.get(
        "/api/report/get-all", headers=get_test_headers
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list), "В качестве ответа вернулись не прогназируемые данные."
