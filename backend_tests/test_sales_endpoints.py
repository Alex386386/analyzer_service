from httpx import AsyncClient


async def test_particular_sale_in_db(get_test_headers, client: AsyncClient):
    """
    Проверка как отрабатывает получение конкретного объекта продажи из БД по id.
    """
    response = await client.get(
        "/api/sales/get-one/1", headers=get_test_headers
    )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data == {"detail": "Объект продажи не найден!"}


async def test_sale_in_db(get_test_headers, client: AsyncClient):
    """
    Получение всех объектов продажи из БД.
    """
    response = await client.get(
        "/api/sales/get-all", headers=get_test_headers
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list), "В качестве ответа вернулись не прогназируемые данные."
