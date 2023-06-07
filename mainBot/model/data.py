from model.create import get_database
from typing import List
from loguru import logger


class DB:
    def insert_default_user(user_id: int) -> None:
        """Вставка дефолтного пользователя в базу данных """
        collection = get_database()
        collection.insert_one({'_id': user_id, 'urls':
                               []
                               })
        
        logger.log('INFO', f' {user_id} insert in DB')

    
    def check_user_from_db(user_id :int):
        """проверяет есть ли пользователь в базе данных"""
        collection = get_database()
        user = collection.find_one({'_id':user_id})

        logger.log('INFO', f'{user_id} check user in DB')
        return user


    def insert_user_url_and_title(user_id: int, user_url: str, user_title: str) -> None:
        """Вставка новой словаря(ссылки) для парсинга от пользователя"""
        collection = get_database()
        new_user_insert_url = {
            'user_url': user_url,
            'title': user_title,
            'name': '',
            'output_user_ulr': '',
            'description': '',
            'price': 0,
            'last_output_hrefs': []
        }

        collection.update_one({'_id': user_id}, {'$push': {'urls': {'$each': [new_user_insert_url],
                                                                     '$position': 0, '$slice': 5}}})
        logger.log('INFO', f' {user_id} insert all data in DB')


    def check_count_user_url(user_id :int) -> bool:
        """Получаем количество задач пользователя"""
        collection = get_database()
        user_data = collection.find_one({'_id':user_id})
        count_urls = len(user_data['urls'])

        logger.info(f' {user_id} have {count_urls} in DB')

        if count_urls < 5:
            return True
        elif count_urls >= 5:
            return False

    # not log
    def check_user_titles(user_id: int, user_title: str) -> List[str,]:
        """проверка на уникальное описание """
        collection = get_database()
        user_data = collection.find_one({'_id':user_id})
        
        titles = []
        for url in user_data['urls']:
            titles.append(url['title'])
        
        if user_title in titles:
            return True
        else:
            return False


    def get_urls(user_id: int) -> dict:
        """получаем словарь всех url пользователя """
        collection = get_database()
        user_data = collection.find_one({'_id':user_id})

        logger.log('DB', f'{user_id} get urld')

        return user_data['urls']
    
    
    def delete_url_by_title(user_id: int, title: int):
        """удаляем выпранный url по выбранному title """
        collection = get_database()
        collection.update_one({'_id': user_id}, {'$pull': {'urls': {'title': title}}})
        logger.log('INFO', f' {user_id} delete url in DB')        
    
    #not used
    def set_title_url(user_id: int, user_url:str, title:str) -> None:
        """вставаить краткое описание url -> title"""
        collection = get_database()
        collection.update_one({'_id': user_id,'urls':{'$elemMatch':{'user_url':user_url}}},{'$set':{'urls.$.title':title}})

        logger.log('INFO', f' {user_id} insert title DB')