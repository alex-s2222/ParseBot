import pytest
from loguru import logger

from parseUrl.Parse import parseUrl
from model.data import DB
from model.data import get_database


@pytest.fixture
def conn():
    return get_database()

@pytest.mark.asyncio
class TestParsingAvitoUrl:
    async def test_get_message(self):
        user_id = 1
        data_urls = await parseUrl().get_message(user_id=user_id)
        for data_url in data_urls:
            logger.info(f'{data_url}')
            for titles, data in data_url.items():
                if data:
                    assert data['output_user_url'] != None
                    assert data['name'] != None
                    assert data['price'] != None
                    assert data['location'] != None


    def test_delete_user(self, conn):
        """удаляем тестового пользователя в базе данных"""
        conn.delete_one({'_id': 1})
    