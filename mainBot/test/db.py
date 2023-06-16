import pytest
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

from model.data import DB
from model.create import get_database


@dataclass
class User:
    _id = 1
    _urls = ['avito.ru', '1avito.ru',
                   '2avito.ru', '3avito.ru', '4avito.ru']
    _titles = ['0', '1', '2', '3', '4']


@pytest.fixture
def default_user():
    return {'_id': User._id, 'urls': []}


@pytest.fixture
def conn():
    return get_database()

@pytest.fixture
def get_time() -> List[datetime,] :
    now = datetime.now()
    end = now + timedelta(hours=24)
    return [now, end]


class TestDB:
    def test_check_user(self):
        """проверка есть ли пользователь в базе данных"""
        result = DB.check_user_from_db(user_id=User._id)
        assert result == None

    def test_insert_default_user(self, conn, get_time):
        """проверка вставки пользователя в базу данных"""
        time = get_time
        DB.insert_default_user(User._id, *time)
        result = conn.find_one({'_id': User._id})

        assert result != None
        assert result['_id'] == User._id
        assert result['start_subscription'].date() == time[0].date()
        assert result['end_subscription'].date() == time[1].date()
    """<----------start---------->"""

    def test_get_user_subs(self, get_time):
        end_user_subs = DB.get_user_subsctription(user_id=User._id)
        assert end_user_subs.date() == get_time[1].date()


    def test_check_user_subsription(self):
        """проверка на то что у пользователя действует подписка"""
        assert DB.check_user_subscription(user_id=User._id) == False

    """<-------subscriptions------->"""
    
    def test_insert_user_url_in_arr(self, conn):
        """проверка вставки задачи(url) пользователем"""
        DB.insert_user_url_and_title( user_id=User._id, user_url=User._urls[0], user_title=User._titles[0])
        result = conn.find_one({'_id': User._id})

        assert len(result['urls']) == 1
        assert result['urls'][0]['user_url'] == User._urls[0]


    def test_check_count_user_urls(self, conn):
        """проверяем кол-во задач пользователя"""
        check_count_url = DB.check_count_user_url(user_id=User._id)
        assert check_count_url == False

        # заполняем до 5 задач
        for i in range(4):
            DB.insert_user_url_and_title(User._id, User._urls[i+1], User._titles[i+1])

        check_count_url = DB.check_count_user_url(user_id=User._id)
        assert check_count_url == True

    
    def test_check_user_titles(self):
        """проверка что пользователь не вводит одинаковые url"""
        dont_title = 'ops'
        
        for i in range(5):
            assert True == DB.check_user_titles(user_id=User._id, user_title=User._titles[i]) 
        assert False == DB.check_user_titles(user_id=User._id, user_title=dont_title)

    """<-----------end----------->"""
    def test_delete_user(self, conn):
        """удаляем тестового пользователя в базе данных"""
        conn.delete_one({'_id': User._id})
