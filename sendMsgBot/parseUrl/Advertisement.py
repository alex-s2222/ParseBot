from typing import NamedTuple, List
import ssl
import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import ssl_
from bs4 import BeautifulSoup

from model.data import DB

CIPHERS = 'ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-CHACHA20-POLY1305:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:GOST2012256-GOST89-GOST89:DHE-RSA-CAMELLIA256-SHA256:DHE-RSA-CAMELLIA256-SHA:GOST2001-GOST89-GOST89:AES256-GCM-SHA384:AES256-SHA256:AES256-SHA:CAMELLIA256-SHA256:CAMELLIA256-SHA:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-CAMELLIA128-SHA256:DHE-RSA-CAMELLIA128-SHA:AES128-GCM-SHA256:AES128-SHA256:AES128-SHA:CAMELLIA128-SHA256:CAMELLIA128-SHA:ECDHE-RSA-RC4-SHA:ECDHE-ECDSA-RC4-SHA:RC4-SHA:RC4-MD5:ECDHE-RSA-DES-CBC3-SHA:ECDHE-ECDSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:DES-CBC3-SHA'

class TlsAdapter(HTTPAdapter):
    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(
            ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(
            *pool_args, ssl_context=ctx, **pool_kwargs)
        

# получаем html страницу по запрашиваему url
def get_message(user_id: int) -> list:
    session = requests.session()
    adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
    session.mount("https://", adapter)

    urls = DB.get_user_urls(user_id=user_id)

    try:
        for url in urls:
            # создаем массив выходных данных
            user_data = []

            # получаем html page
            r = session.request('GET', url=url)
            print(r.text)
            # парсим данные с html page
            url_data = _parse_html(content=r.text, user_id=user_id, user_url=url)

            # добавляем данные
            user_data.append(url_data)
        return user_data

    except Exception as exception:
        print(exception)


def _parse_html(content: str, user_id: int, user_url: str) -> dict:
    soup = BeautifulSoup(content)

    # parse description
    for j, tag_div in enumerate(soup.findAll(attrs={
            'class': 'iva-item-root-_lk9K photo-slider-slider-S15A_ iva-item-list-rfgcH iva-item-redesign-rop6P iva-item-responsive-_lbhG items-item-My3ih items-listItem-Gd1jN js-catalog-item-enum'})):

        # search url and name product
        name, href = _get_name_href(tag_div)

        # search description product
        description = _get_descriptions(tag_div)

        # search price product
        price = _get_price(tag_div)

        # проверка что новая ссылка не равняется старой

        #TODO Delete and create new logic->->->

        if href in DB.get_user_output_href(user_id=user_id, user_url=user_url):
            return ''
        else:
            new_data_url = {'output_user_url': href, 
                            'name': name, 
                            'price': price}
            
            DB.update_last_output_hrefs(user_id=user_id, user_url=user_url, last_url=href)
            return new_data_url
            


        # if (href == get_output_user_url(chat_id)) or (href in get_last_output_hrefs(chat_id)):
        #     break
        # else:
        #     new_user = {'output_user_url': href,
        #                 'name': name, 
        #                 'description': description,
        #                 'price': price}
            
        #     update_user(user_id=chat_id, updated_user=new_user)
        #     # реализация очереди fifo
        #     update_last_output_hrefs(user_id=chat_id, href=href)
        #     break


def _get_name_href(tag):
    HREF_AVITO = "https://www.avito.ru"

    for tag_div_a in tag.findAll(attrs={'class': 'iva-item-titleStep-pdebR'}):
        for tag_a in tag_div_a:
            href = HREF_AVITO + tag_a.attrs.get("href")
            # print("URL:\t", href)
            name = tag_a['title']
            # print("Name:\t", name)
            return name, href


def _get_descriptions(tag):
    for tag_description in tag.findAll(
            attrs={'class': 'iva-item-text-Ge6dR iva-item-description-FDgK4 text-text-LurtD text-size-s-BxGpL'}):
        list_description = str(tag_description.text).split("\n")
        description = " ".join(list_description)
        # print("description:\t", description)
        return description


def _get_price(tag):
    for tag_name in tag.findAll(attrs={'itemprop': 'price'}):
        price = int(tag_name['content'])
        # print("price:\t", price)
        return price