from bs4 import BeautifulSoup


def parse_seo_tags_from_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    parsed_values = {
        'h1': soup.h1.string if soup.h1 else '',
        'title': soup.title.string if soup.title else '',
        'description': ''
    }
    for meta in soup.find_all('meta'):
        if meta.get('name') == 'description':
            parsed_values['description'] = meta.get('content')
            break
    return parsed_values
