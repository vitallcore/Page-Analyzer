# import pytest
# from playwright.sync_api import Page, expect
# from page_analyzer import app
# from page_analyzer.db import (
#     get_connection,
#     add_url_to_db,
#     get_url_by_name,
#     get_url_by_id,
#     add_check_to_db,
#     get_checks_desc,
#     get_urls_with_latest_check
# )
#
#
# @pytest.fixture
# def url():
#     return 'https://hello_world.com'
#
# @pytest.fixture
# def home_page():
#     return 'https://python-project-83-rael.onrender.com/'
#
#
# def test_add_url_to_db_and_get_url_by_name(url):
#     add_url_to_db(url)
#     curr_url = get_url_by_name(url)
#
#     assert curr_url[0].name == url
#
#
# def test_get_url_by_id():
#     curr_url = get_url_by_id(1)
#
#     assert curr_url[0].id == 1
#
#
# def test_add_check_to_db_and_get_checks_desc():
#     page_data = {
#         'title': 'Hello',
#         'h1': 'World',
#         'description': None,
#     }
#
#     add_check_to_db(1, 200, page_data)
#
#     checks = get_checks_desc(1)
#
#     assert checks[0].id == 1
#     assert checks[0].status_code == 200
#     assert checks[0].title == 'Hello'
#     assert checks[0].h1 == 'World'
#     assert checks[0].description == ''
#
#
# def test_get_urls_with_latest_check(url):
#     urls_and_checks = get_urls_with_latest_check()
#     url_with_check = urls_and_checks[0]
#     assert url_with_check.name == url
#     assert url_with_check.status_code == '200'
#
#
# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client
#
#
# def test_get_index(client):
#     response = client.get('/')
#     assert response.status_code == 200
#
#
# def test_get_urls(client):
#     response = client.get('/urls')
#     assert response.status_code == 200
#
#
# def test_page_not_found(client):
#     response = client.get('/something')
#     assert response.status_code == 404
#
#
# def test_post_url(client):
#     response = client.post('/urls', data={'url': 'https://right1.com'})
#     assert response.status_code == 302
#
#
# def test_post_incorrect_url(client):
#     response = client.post('/urls', data={'url': 'htps://right.com'})
#     assert response.status_code == 422
#
#
# def test_get_url(client):
#     response = client.get('/urls/2')
#     text = response.get_data(as_text=True)
#     assert 'ID' in text
#     assert '2' in text
#     assert 'Имя' in text
#     assert 'https://right1.com' in text
#
#
# def test_url_added(page: Page, home_page):
#     page.goto(home_page, timeout=15000)
#     page.locator('input[name="url"]').type('http://right.com')
#     page.locator('input[type="submit"]').click()
#     expect(page.get_by_text('Страница успешно добавлена')).to_be_visible()
#
#
# def test_url_already_added(page: Page, home_page):
#     page.goto(home_page)
#     page.locator('input[name="url"]').type('http://right.com')
#     page.locator('input[type="submit"]').click()
#     expect(page.get_by_text('Страница уже существует')).to_be_visible()
#
#
# def test_url_validator(page: Page, home_page):
#     page.goto(home_page)
#     page.locator('input[name="url"]').type('htp://wrong.com')
#     page.locator('input[type="submit"]').click()
#     expect(page.get_by_text('Некорректный URL')).to_be_visible()
#     page.locator('input[name="url"]').type('W' * 256)
#     page.locator('input[type="submit"]').click()
#
#
# def test_url_not_pass_check(page: Page, home_page):
#     page.goto(home_page)
#     page.locator('input[name="url"]').type('http://wrong.com')
#     page.locator('input[type="submit"]').click()
#     page.locator('text=Запустить проверку').click()
#     expect(page.get_by_text('Произошла ошибка при проверке')).to_be_visible()
#
#
# def test_url_pass_check_and_check_info_added(page: Page, home_page):
#     page.goto(home_page)
#     page.locator('input[name="url"]').type('https://www.google.com/')
#     page.locator('input[type="submit"]').click()
#     page.locator('text=Запустить проверку').click()
#
#     expect(page.get_by_text('Страница успешно проверена')).to_be_visible()
#
#
# def test_drop_tables():
#     conn = get_connection()
#     query = "tests/fixtures/database.sql"
#
#     with conn.cursor() as cur, open(query, 'r') as data_base_restart:
#         cur.execute(data_base_restart.read())
#
#         conn.commit()
#         conn.close()
