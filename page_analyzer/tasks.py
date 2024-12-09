import requests

from page_analyzer.celery_config import celery_app
from page_analyzer.db import add_check_to_db, get_urls_with_latest_check
from page_analyzer.html_parser import parse_page


@celery_app.task
def async_check_all_urls():
    all_urls = get_urls_with_latest_check()
    for url in all_urls:
        try:
            response = requests.get(url.name)
        except requests.exceptions.RequestException:
            add_check_to_db(
                url.id,
                0,
                {'title': '', 'h1': '', 'description': 'Ошибка сети'}
            )
            continue
        page_data = parse_page(response.text)
        status_code = response.status_code
        add_check_to_db(url.id, status_code, page_data)
