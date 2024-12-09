import requests

from page_analyzer.html_parser import parse_page


def get_url_status_and_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        page_data = parse_page(response.text)
        return response.status_code, page_data
    except requests.RequestException:
        return 0, {'h1': '', 'title': '', 'description': 'Ошибка сети'}
