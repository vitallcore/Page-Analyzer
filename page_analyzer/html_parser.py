from bs4 import BeautifulSoup


def parse_page(response_text):
    html_data = BeautifulSoup(response_text, 'html.parser')
    page_data = {'title': html_data.title.string if html_data.title else None,
                 'h1': html_data.h1.string if html_data.h1 else None}

    description = html_data.find('meta', {'name': 'description'})
    if description:
        description = description.get('content')

    page_data['description'] = description

    return page_data
