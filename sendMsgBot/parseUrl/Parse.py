import ssl
import aiohttp
import asyncio 
from bs4 import BeautifulSoup
from pprint import pprint 
from SETTINGS import FORCED_CIPHERS
from typing import List, Dict
from model.data import DB


class parseUrl:
    async def get_message(self, user_id :int) -> List[Dict,]:
        user_urls = DB.get_user_urls_and_title(user_id=user_id)
        # cоздаем список под задачи
        tasks = []
        for urls in user_urls:
            for title, url in urls.items():
                # создаем и задносим задачи
                task = asyncio.create_task(self.__get_data_url(url=url, title=title, user_id=user_id))
                tasks.append(task)

        # запускаем задачи
        data_urls = await asyncio.gather(*tasks)

        return data_urls
        # обрабатываем полученые 
        # for data_url in data_urls:
        #     for title, url in data_url.items():
        #         msq = f'\t#{title} \n'  +\
        #                 f'{url["output_user_url"]} \n' +\
        #                 f'{url["name"]} \n' +\
        #                 f'{url["price"]} \n'
        #     print(msq)


    async def __get_data_url(self, url :str, title :str, user_id :int) -> Dict:
        sslcontext = ssl.create_default_context()
        sslcontext.options |= ssl.OP_NO_SSLv3
        sslcontext.set_ciphers(FORCED_CIPHERS)

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=50, verify_ssl=False)) as session:
            r = await session.get(url, ssl=sslcontext)
            url_data = self.__parse_html(content=await r.text(), user_id=user_id, user_url=url)
            return {title:url_data}


    def __parse_html(self, content: str, user_id: int, user_url: str) -> Dict:
        soup = BeautifulSoup(content)

        for j, tag_div in enumerate(soup.findAll(attrs={
                'class': 'iva-item-root-_lk9K photo-slider-slider-S15A_ iva-item-list-rfgcH iva-item-redesign-rop6P iva-item-responsive-_lbhG items-item-My3ih items-listItem-Gd1jN js-catalog-item-enum'})):

            # search url and name product
            name, href = self.__get_name_href(tag_div)

            # search description product
            description = self.__get_descriptions(tag_div)

            # search price product
            price = self.__get_price(tag_div)

            # проверка что новая ссылка не равняется старой
            if href in DB.get_user_output_href(user_id=user_id, user_url=user_url):
                return ''
            else:
                new_data_url = {'output_user_url': href, 
                                'name': name, 
                                'price': price}
                
                DB.update_last_output_hrefs(user_id=user_id, user_url=user_url, last_url=href)
            return new_data_url


    def __get_name_href(self, tag) -> str:
        HREF_AVITO = "https://www.avito.ru"

        for tag_div_a in tag.findAll(attrs={'class': 'iva-item-titleStep-pdebR'}):
            for tag_a in tag_div_a:
                href = HREF_AVITO + tag_a.attrs.get("href")
                # print("URL:\t", href)
                name = tag_a['title']
                # print("Name:\t", name)
                return name, href


    def __get_descriptions(self,tag) -> str:
        for tag_description in tag.findAll(
                attrs={'class': 'iva-item-text-Ge6dR iva-item-description-FDgK4 text-text-LurtD text-size-s-BxGpL'}):
            list_description = str(tag_description.text).split("\n")
            description = " ".join(list_description)
            # print("description:\t", description)
            return description


    def __get_price(self,tag) -> str:
        for tag_name in tag.findAll(attrs={'itemprop': 'price'}):
            price = int(tag_name['content'])
            # print("price:\t", price)
            return price


from datetime import datetime


if __name__ == "__main__":
    start = datetime.now()
    asyncio.run(parseUrl().main())
    end = datetime.now() - start
    print(end)

    a = parseUrl()
    