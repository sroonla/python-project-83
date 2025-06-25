import os
import datetime
from flask import (
    Flask, render_template, request, 
    redirect, url_for, flash, get_flashed_messages
)
from dotenv import load_dotenv
from .db import (
    add_url, get_url_by_id, get_url_by_name,
    get_all_urls, add_url_check, get_url_checks,
    is_valid_url, normalize_url
)

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.datetime.now().year}

@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)

@app.route('/urls', methods=['POST'])
def add_url_handler():
    url = request.form.get('url')
    
    if not is_valid_url(url):
        flash('Некорректный URL', 'danger')
        return render_template('index.html', url=url), 422
    
    normalized_url = normalize_url(url)
    existing_url = get_url_by_name(normalized_url)
    
    if existing_url:
        flash('Страница уже существует', 'info')
        return redirect(url_for('show_url', id=existing_url[0]))
    
    try:
        url_id = add_url(normalized_url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('show_url', id=url_id))
    except Exception as e:
        flash(f'Ошибка при добавлении страницы: {str(e)}', 'danger')
        return render_template('index.html', url=url), 500

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
    messages = get_flashed_messages(with_categories=True)
    return render_template('urls/show.html', url=url, checks=checks, messages=messages)

@app.post('/urls/<int:id>/checks')
def check_url(id):
    url = get_url_by_id(id)
    if not url:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('index'))
    
    try:
        add_url_check(id)
        flash('Страница успешно проверена', 'success')
    except Exception as e:
        flash(f'Ошибка при проверке страницы: {str(e)}', 'danger')
    
    return redirect(url_for('show_url', id=id))