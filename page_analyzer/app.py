import os
import datetime
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash
)
from dotenv import load_dotenv
from .db import (
    add_url, get_url_by_id, get_url_by_name,
    get_all_urls, add_url_check, get_url_checks
)
from .url_utils import is_valid_url, normalize_url
from .page_parser import parse_page

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.context_processor
def inject_current_year():
    return {'current_year': datetime.datetime.now().year}


@app.route('/urls', methods=['POST'])
def add_url_handler():
    url = request.form.get('url')
    
    if not is_valid_url(url):
        flash('Некорректный URL', 'danger')
        return render_template('index.html', url=url), 422
    
    try:
        normalized_url = normalize_url(url)
        existing_url = get_url_by_name(normalized_url)
        
        if existing_url:
            flash('Страница уже существует', 'info')
            return redirect(url_for('show_url', id=existing_url['id']))
    
        url_id = add_url(normalized_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('show_url', id=url_id))
    
    except Exception as e:
        app.logger.error(f"Database error: {str(e)}")
        flash('Ошибка при добавлении страницы', 'danger')
        return redirect(url_for('index'))


@app.route('/urls')
def list_urls():
    urls = get_all_urls()
    return render_template('urls/index.html', urls=urls)


@app.route('/urls/<int:id>')
def show_url(id):
    url = get_url_by_id(id)
    if not url:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('index'))
    
    checks = get_url_checks(id)
    return render_template('urls/show.html', url=url, checks=checks)


@app.post('/urls/<int:id>/checks')
def check_url(id):
    url_data = get_url_by_id(id)
    if not url_data:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('index'))
    
    url_name = url_data['name']
    
    try:
        page_data = parse_page(url_name)
        
        add_url_check(
            id,
            page_data['status_code'],
            page_data['h1'],
            page_data['title'],
            page_data['description']
        )
        flash('Страница успешно проверена', 'success')
        
    except requests.exceptions.RequestException as e:
        if isinstance(e, requests.exceptions.Timeout):
            error_msg = 'Таймаут при проверке сайта'
        elif isinstance(e, requests.exceptions.TooManyRedirects):
            error_msg = 'Слишком много перенаправлений'
        elif isinstance(e, requests.exceptions.SSLError):
            error_msg = 'Ошибка SSL сертификата'
        else:
            error_msg = 'Произошла ошибка при проверке'
        
        flash(error_msg, 'danger')
    
    except Exception as e:
        flash(f'Неизвестная ошибка: {str(e)}', 'danger')
    
    return redirect(url_for('show_url', id=id))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)