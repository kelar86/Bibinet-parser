import re
import requests
import uuid
import os
from lxml import html, etree


def __save_photo(url):
    if not os.path.exists('./img'):
        os.mkdir('./img', mode=0o777)

    file_name = "img/" + str(uuid.uuid4()) + '.jpg'

    if requests.head(url).ok:
        p = requests.get(url)
        with open(file_name, "wb") as file:
            file.write(p.content)
            return str(os.path.abspath(file_name))
    else:
        return None


def __get_part_type(page):
    tree = html.fromstring(page)
    return tree.xpath("//*[@class='part']/div/a/text()")


def __get_mark(page):
    tree = html.fromstring(page)
    autos = tree.xpath("//*[@class='auto']/strong/text()")
    return [re.match(r'^[A-Z][a-z]+(\s*[a-z]*)', item).group(0).strip() for item in autos]


def __get_price(page):
    tree = html.fromstring(page)
    prices = tree.xpath("//*[@class='price']/strong/text()")
    prices = [item.replace(' ', '') for item in prices]
    return list(filter(lambda item: re.match(r'^[0-9]+$', item), prices))


def __get_photo(page):
    tree = html.fromstring(page)
    img_urls = tree.xpath("//*[@class='photo']/a")
    img_urls = [etree.tostring(url, encoding='unicode') for url in img_urls]
    img_urls = [re.search(r'https:.*jpg', item).group(0) for item in img_urls]
    return [__save_photo(url) for url in img_urls]


def __get_company(page):
    tree = html.fromstring(page)
    return tree.xpath("//*[@class='company']/a[1]/text()")


def __get_model(page):
    tree = html.fromstring(page)
    autos = tree.xpath("//*[@class='auto']/strong/text()")
    return [re.search(r'(.[A-Z][a-z\-]*)|([A-Z][a-z]*$)', item).group(0).strip() for item in autos]


def __group_results(items):
    return list(map(lambda item: item.group(1).strip() if item is not None else None, items))


def __get_frame_engine_year(page):
    tree = html.fromstring(page)
    columns = tree.xpath("//*[@class='auto']")
    columns = [etree.tostring(column, encoding='unicode') for column in columns]

    frames = __group_results([re.search(r'.кузов:\s(.*?)<', column) for column in columns])
    engines = __group_results([re.search(r'.двигатель:\s(.*?)<', column) for column in columns])
    years = __group_results([re.search(r'.год\sвыпуска:\s(.*?)<', column) for column in columns])

    return {'frames': frames, 'engines': engines, 'years': years}


def get_page_data(pages):
    for page in pages:
        frame_engine_year = __get_frame_engine_year(page)
        return tuple(zip(__get_part_type(page),
                         __get_mark(page),
                         __get_model(page),
                         frame_engine_year['frames'],
                         frame_engine_year['engines'],
                         frame_engine_year['years'],
                         __get_price(page),
                         __get_company(page),
                         __get_photo(page)))


def have_results(url):
    page = requests.get(url).text

    return not re.match(r'<div id=\"fs_not_rezult\"', page)


def get_list_of_models(page):
    tree = html.fromstring(page)
    return tree.xpath("//*[@id='catalog_block_select']/div/span/a/text()")
