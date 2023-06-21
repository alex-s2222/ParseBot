from model.create import get_database
from typing import List
from loguru import logger
from datetime import datetime, timedelta

class DB:
    def insert_default_user(user_id: int, date_now: datetime, date_end: datetime) -> None:
        """Вставка дефолтного пользователя в базу данных """
        collection = get_database()
        collection.insert_one({'_id': user_id,
                               'start_subscription': date_now,
                               'end_subscription': date_end,
                               'urls': []
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
            'last_output_hrefs': []
        }

        collection.update_one({'_id': user_id}, {'$push': {'urls': {'$each': [new_user_insert_url],
                                                                     '$position': 0, '$slice': 5}}})
        logger.log('INFO', f' {user_id} insert all data in DB')


    def get_user_subsctription(user_id: int) -> datetime:
        collection = get_database()
        user_data = collection.find_one({'_id': user_id})
        
        logger.log('INFO',f'{user_id} end subs')
        
        return user_data['end_subscription'] 

    def check_user_subscription(user_id: int) -> bool:
        """Если у пользователя есть активная подписка возвращаем False"""
        collection = get_database()
        user_data = collection.find_one({'_id': user_id})
        
        time = datetime.now()
        if user_data['end_subscription'] < time:
            return True
        else:
            return False
        

    def check_count_user_url(user_id :int) -> bool:
        """Получаем количество задач пользователя"""
        collection = get_database()
        user_data = collection.find_one({'_id':user_id})
        count_urls = len(user_data['urls'])

        logger.info(f' {user_id} have {count_urls} in DB')

        if count_urls >= 5:
            return True
        elif count_urls < 5:
            return False


    def check_user_titles(user_id: int, user_title: str) -> List[str,]:
        """проверка на уникальное описание """
        collection = get_database()
        user_data = collection.find_one({'_id':user_id})
        
        titles = []
        for url in user_data['urls']:
            titles.append(url['title'])

        logger.info(f' {user_id} have titles: {titles} in DB')
        
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


    def admin_set(user_id: int, number_time: int, string_time: str) -> bool:
        date_time = {'d': timedelta(days=number_time),
                 'm': timedelta(days=30*number_time),
                 'w': timedelta(weeks=number_time)}

        collection = get_database()
        time_now = datetime.now()

        user_data = collection.find_one({'_id': user_id})

        add_data = date_time.get(string_time, 0)

        user_end_subs = user_data['end_subscription']
        if add_data != 0:  
            if  user_end_subs < time_now:
                collection.update_one({'_id': user_id},{'$set': {'end_subscription': time_now + add_data}})
                return True
            elif user_end_subs > time_now:
                collection.update_one({'_id': user_id}, {'$set': {'end_subscription': user_end_subs + add_data }})
                return True
        else:
            False     
    

    

    
