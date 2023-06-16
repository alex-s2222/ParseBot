from .create import get_database
from typing import List
from datetime import datetime


class DB:
    
    def update_last_output_hrefs(user_id: int, user_url: str, last_url: str) -> None:
        """добавление новой ссылки в отправленные сслылки юзера (что бы не повторялись)"""
        collection = get_database()

        collection.update_one({'_id': user_id, 'urls.user_url': user_url}, {'$push': {"urls.$.last_output_hrefs":
                                                                             {'$each': [last_url], 
                                                                              '$position': 0, '$slice': 50}}})
    

    def get_user_output_href(user_id: int, user_url :str):
        collection = get_database()
        
        user_data = collection.find_one({'_id':user_id},{'urls':{'$elemMatch':{'user_url': user_url}}})
        url_data = user_data['urls'][0]
        return url_data['last_output_hrefs']

       
    def get_urls(user_id: int) -> dict:
        """получаем словарь всех url пользователя """
        collection = get_database()
        user_data = collection.find_one({'_id':user_id})
        return user_data['urls']
    

    def check_user_subscription(user_id: int) -> bool:
        """Если у пользователя есть активная подписка возвращаем False"""
        collection = get_database()
        user_data = collection.find_one({'_id':user_id})

        time = datetime.now()
        if user_data['end_subscription'] < time:
            return True
        else:
            return False


    def get_user_urls_and_title(user_id :int) -> List:
        """возвращаем список url пользователя"""
        collection = get_database()
        user_data = collection.find_one({'_id':user_id})
        urls = []
        for url_data in user_data['urls']:
            url = url_data['user_url']
            title = url_data['title']
            urls.append({title: url})
        return urls
