from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from http import HTTPStatus


async def test_analyze_sales_success(get_test_headers, client: AsyncClient):
    mock_celery_task = AsyncMock()
    mock_celery_task.id = "12345"
    mock_celery_task.state = "PENDING"

    xml_data = """
        <sales date="2024-11-12">
            <products>
                <product>
                    <id>1</id>
                    <name>Product 1</name>
                    <quantity>10</quantity>
                    <price>100.0</price>
                    <category>Category 1</category>
                </product>
                <product>
                    <id>2</id>
                    <name>Product 2</name>
                    <quantity>5</quantity>
                    <price>200.0</price>
                    <category>Category 2</category>
                </product>
            </products>
        </sales>
    """

    with patch('src.celery_tasks.process_sales_data.delay', return_value=mock_celery_task):
        response = await client.post("/", content=xml_data, headers=get_test_headers)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"task_id": "12345"}


async def test_analyze_sales_invalid_data(get_test_headers, client: AsyncClient):

    invalid_xml_data = """
        <sales date="2024-11-12">
        </sales>
    """

    response = await client.post("/", content=invalid_xml_data, headers=get_test_headers)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "В запросе отсутствуют данные!"}