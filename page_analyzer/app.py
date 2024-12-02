import os
import requests
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    flash,
    get_flashed_messages,
    url_for,
    redirect
)
from page_analyzer.url import validate_url, normalize_url
from page_analyzer.html import parse_seo_tags_from_html
from page_analyzer.database import (
    add_new_url,
    add_new_url_check,
    get_url_info_by_url_id,
    get_url_id_by_url_name,
    get_url_checks_by_url_id,
    get_all_urls
)


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def add_url():
    url_name = request.form.get('url', '', type=str)
    if not validate_url(url_name):
        flash('Некорректный URL', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            messages=messages,
            url_name=url_name
        ), 422
    url_name = normalize_url(url_name)
    url_id = get_url_id_by_url_name(url_name)
    if not url_id:
        flash('Страница успешно добавлена', 'success')
        add_new_url(url_name)
        url_id = get_url_id_by_url_name(url_name)
    else:
        flash('Страница уже существует', 'info')
    return redirect(url_for('show_url', url_id=url_id), 302)


@app.get('/urls')
def show_all_urls():
    urls = get_all_urls()
    return render_template(
        'show_all_urls.html',
        urls=urls
    )


@app.route('/urls/<int:url_id>')
def show_url(url_id):
    url_info = get_url_info_by_url_id(url_id)
    if not url_info:
        return render_template('404.html'), 404
    url_checks = get_url_checks_by_url_id(url_id)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'show_url.html',
        messages=messages,
        url=url_info,
        url_checks=url_checks
    )


@app.post('/urls/<int:url_id>/checks')
def check_url(url_id):
    url_info = get_url_info_by_url_id(url_id)
    if not url_info:
        return render_template('404.html'), 404
    try:
        resp = requests.get(url_info['name'])
        resp.raise_for_status()
        values = {
            'url_id': url_id,
            'status_code': resp.status_code,
        }
        values.update(parse_seo_tags_from_html(resp.text))
        add_new_url_check(values)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('show_url', url_id=url_id), 302)
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url', url_id=url_id))


if __name__ == '__main__':
    app.run()
