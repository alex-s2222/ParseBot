from typing import NamedTuple, List
import ssl
import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import ssl_
from bs4 import BeautifulSoup

from SETTINGS import CIPHERS

class TlsAdapter(HTTPAdapter):
    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(
            ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(
            *pool_args, ssl_context=ctx, **pool_kwargs)
        
class ParseUrl(TlsAdapter):
    
    # получаем html страницу по запрашиваему url
    def get_parse_message(chat_id: int) -> None:
        session = requests.session()
        adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
        session.mount("https://", adapter)
        
        url = get_insert_user_url(chat_id)
        try:
            r = session.request('GET', url=url)
            _parse_html(content=r.text, chat_id=chat_id)
        except Exception as exception:
            print(exception)


    def _parse_html(content: str, chat_id: int) -> None:
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