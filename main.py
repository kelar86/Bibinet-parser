import repository
import router
import my_parser

MAX_MODELS = 3


def main(mark='honda'):

    start_url = router.BASE_URL + '/' + mark
    start_page = router.get_start_page(start_url)
    models = my_parser.get_list_of_models(start_page)

    repository.create_base()

    for model in models[0:MAX_MODELS]:
        pages = router.route(mark, model)
        data = my_parser.get_page_data(pages)

        repository.add(data)


if __name__ == '__main__':
    main()
