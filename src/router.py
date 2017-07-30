import requests

from src import my_parser

BASE_URL = 'https://bibinet.ru/part/all'
PAGE_PART = 'page='
MAX_PAGES = 3


def route(mark, model, max_pages=MAX_PAGES):
    pages = __paginator(max_pages)
    mark = mark.strip().lower()
    model = __model_name_format(model)
    urls = __url_constructor(mark, model, pages)
    urls = __check_urls_is_ok(urls)
    return __get_html_pages(urls)


def __url_constructor(mark, model, pages):
    return list(map(lambda url: BASE_URL + '/' + mark + '/' + model + url, pages))


def __paginator(max_pages):
    list_page_suffix = ['']
    for i in range(1, max_pages):
        list_page_suffix.append('/' + PAGE_PART + str(i))
    return list_page_suffix


def __model_name_format(model_name):
    model_name = model_name.strip().lower()
    return model_name.replace(' ', '-')


def __check_urls_is_ok(url_list):
    return filter(lambda url: requests.head(url).ok, url_list)


def __get_html_pages(url_list):
    return [requests.get(url).text for url in url_list if my_parser.have_results(url)]


def get_start_page(url):
    page = requests.get(url).text
    return page
