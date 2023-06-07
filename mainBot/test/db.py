import pytest
from dataclasses import dataclass

from model.data import DB
from model.create import get_database


@dataclass
class TestUser:
    user_id = 1
    insert_urls = ['avito.ru', '1avito.ru',
                   '2avito.ru', '3avito.ru', '4avito.ru']
    insert_titles = ['0', '1', '2', '3', '4']


@pytest.fixture
def default_user():
    return {'_id': TestUser.user_id, 'urls': []}


@pytest.fixture
def conn():
    return get_database()


class TestDB:
    def test_check_user(self):
        """проверка есть ли пользователь в базе данных"""
        result = DB.check_user_from_db(user_id=TestUser.user_id)
        assert result == None

    def test_insert_default_user(self, conn):
        """проверка вставки пользователя в базу данных"""
        DB.insert_default_user(user_id=TestUser.user_id)
        result = conn.find_one({'_id': TestUser.user_id})

        assert result != None
        assert result == {'_id': TestUser.user_id, 'urls': []}
    """<----------start---------->"""
    
    def test_insert_user_url_in_arr(self, conn):
        """проверка вставки задачи(url) пользователем"""
        DB.insert_user_url_and_title( user_id=TestUser.user_id, user_url=TestUser.insert_urls[0], user_title=TestUser.insert_titles[0])
        result = conn.find_one({'_id': TestUser.user_id})

        assert len(result['urls']) == 1
        assert result['urls'][0]['user_url'] == TestUser.insert_urls[0]


    def test_check_count_user_urls(self, conn):
        """проверяем кол-во задач пользователя"""
        check_count_url = DB.check_count_user_url(user_id=TestUser.user_id)
        assert check_count_url == True

        # заполняем до 5 задач
        for i in range(4):
            DB.insert_user_url_and_title(TestUser.user_id, TestUser.insert_urls[i+1], TestUser.insert_titles[i+1])

        check_count_url = DB.check_count_user_url(user_id=TestUser.user_id)
        assert check_count_url == False

    
    def test_check_user_titles(self):
        """проверка что пользователь не вводит одинаковые url"""
        dont_title = 'ops'
        
        for i in range(5):
            assert True == DB.check_user_titles(user_id=TestUser.user_id, user_title=TestUser.insert_titles[i]) 
        assert False == DB.check_user_titles(user_id=TestUser.user_id, user_title=dont_title)

    """<-----------end----------->"""
    def test_delete_user(self, conn):
        """удаляем тестового пользователя в базе данных"""
        conn.delete_one({'_id': TestUser.user_id})
