from .create import get_database


class DB:
    def update_last_output_hrefs(user_id: int, user_url: str, last_url: str) -> None:
        """добавление новой ссылки в отправленные сслылки юзера (что бы не повторялись)"""
        collection = get_database()

        collection.update_one({'_id': user_id, 'urls.user_url': user_url}, {'$push': {"urls.$.last_output_hrefs":
                                                                             {'$each': [last_url], 
                                                                              '$position': 0, '$slice': 50}}})

       
    