from page_analyzer.celery_config import celery_app
from page_analyzer.db import add_check_to_db, get_urls_with_latest_check
from page_analyzer.helpers import get_url_status_and_data


@celery_app.task
def async_check_all_urls():
    all_urls = get_urls_with_latest_check()
    for url in all_urls:
        status_code, page_data = get_url_status_and_data(url.name)
        add_check_to_db(url.id, status_code, page_data)
