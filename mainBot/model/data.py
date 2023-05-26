from model.create import get_database
# from create import get_database
from typing import List


# - используется

class DB:
    
    def insert_default_user(user_id: int) -> None:
        """Вставка дефолтного пользователя в базу данных """
        collection = get_database()
        collection.insert_one({'_id': user_id, 'urls':
                               []
                               })

    
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
    
    #TODO right func check user 
    def check_user_from_db(user_id :int):
        pass

    #TODO right func check length user urls then < 5
    def check_count_user_url(user_id :int):
        pass


    def get_user_titles(user_id :int) -> List[str,]:
        pass 

<<<<<<< HEAD
        collection.update_one(
            {'_id': 1}, {'$pull': {'urls': {'user_url': insert_user_url}}})


    def update_last_output_hrefs(user_id: int, user_url: str, last_url: str) -> None:
        """добавление новой ссылки в отправленные сслылки юзера (что бы не повторялись отправленые ссылки)"""
        collection = get_database()

        collection.update_one({'_id': user_id, 'urls.user_url': user_url}, {'$push': {"urls.$.last_output_hrefs":
                                                                             {'$each': [last_url], 
                                                                              '$position': 0, '$slice': 50}}})

    def get_user(user_id: int ) -> dict:
        collection = get_database()
        
        user = collection.find_one({'_id': user_id})
        return user         

    #not test and database
=======
    
>>>>>>> b6cb929 (optimiz)
    def set_title_url(user_id: int, user_url:str, title:str) -> None:
        """краткое название url """
        collection = get_database()
        collection.update_one({'_id': user_id,'urls':{'$elemMatch':{'user_url':user_url}}},{'$set':{'urls.$.title':title}})

    
    def get_title_url(user_id: int, user_url:str) -> str:
        """получаем краткое описание url"""
        collection = get_database()
        user_data = collection.find_one({'_id':user_id},({'urls':{'$elemMatch':{'user_url':user_url}}}))
        return user_data['urls'][0]['title']


    def get_urls(user_id: int) -> dict:
        collection = get_database()
        user_data = collection.find_one({'_id':user_id})
        return user_data['urls']
    
<<<<<<< HEAD
=======
    
    def delete_url_by_title(user_id: int, title: int):
        """удаляем выпранный url по выбранному title """
        collection = get_database()
        collection.update_one({'_id': user_id}, {'$pull': {'urls': {'title': title}}})
    
>>>>>>> b6cb929 (optimiz)
