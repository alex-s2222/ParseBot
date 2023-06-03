from model.create import get_database
# from create import get_database
from typing import List
from loguru import logger


class DB:
    def insert_default_user(user_id: int) -> None:
        """Вставка дефолтного пользователя в базу данных """
        collection = get_database()
        collection.insert_one({'_id': user_id, 'urls':
                               []
                               })
        
        logger.log('DB', f' {user_id} insert in DB')

    
    def insert_user_url_in_arr(user_id: int, insert_user_url: str) -> None:
        """Вставка новой словаря(ссылки) для парсинга от пользователя"""
        collection = get_database()
        new_user_insert_url = {
            'user_url': insert_user_url,
            'title':'',
            'name': '',
            'output_user_ulr': '',
            'description': '',
            'price': 0,
            'last_output_hrefs': []
        }

        collection.update_one({'_id': user_id}, {'$push': {'urls': {'$each': [new_user_insert_url],
                                                                     '$position': 0, '$slice': 5}}})
        logger.log('DB', f' {user_id} insert all data in DB')

    
    def check_user_from_db(user_id :int):
        """проверяет есть ли пользователь в базе данных"""
        collection = get_database()
        user = collection.find_one({'_id':user_id})

        logger.log('DB', f'{user_id} check user in DB')

        return user

    #TODO right func check length user urls then < 5
    def check_count_user_url(user_id :int):
        pass


    def get_user_titles(user_id :int) -> List[str,]:
        pass 

    
    def set_title_url(user_id: int, user_url:str, title:str) -> None:
        """вставаить краткое описание url -> title"""
        collection = get_database()
        collection.update_one({'_id': user_id,'urls':{'$elemMatch':{'user_url':user_url}}},{'$set':{'urls.$.title':title}})

        logger.log('DB', f' {user_id} insert title DB')

    #мб удалить 
    def get_title_url(user_id: int, user_url:str) -> str:
        """получаем краткое описание url"""
        collection = get_database()
        user_data = collection.find_one({'_id':user_id},({'urls':{'$elemMatch':{'user_url':user_url}}}))

        logger.log('DB', f'{user_id} get title from DB')

        return user_data['urls'][0]['title']


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
        logger.log('DB', f' {user_id} delete url in DB')        
    
