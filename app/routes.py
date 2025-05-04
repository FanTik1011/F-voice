import json
from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt

routes = Blueprint("routes", __name__)
bcrypt = Bcrypt()

# Демо-користувачі
users = {
    "admin": {"password": bcrypt.generate_password_hash("admin123").decode('utf-8'), "role": "admin"}
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.role = users[username]["role"]

login_manager = LoginManager()
@login_manager.user_loader
def load_user(username):
    return User(username) if username in users else None

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and bcrypt.check_password_hash(users[username]["password"], password):
            user = User(username)
            login_user(user)
            return redirect(url_for('routes.index'))
    return render_template('login.html')

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/news')
def news():
    with open('static/data/news.json', 'r', encoding='utf-8') as file:
        news_list = json.load(file)
    return render_template('news.html', news_list=news_list)

@routes.route('/api/news')
def api_news():
    with open('static/data/news.json', 'r', encoding='utf-8') as file:
        news_list = json.load(file)
    return jsonify(news_list)

@routes.route('/api/manage_news', methods=['POST'])
@login_required
def manage_news():
    if current_user.role != "admin":
        return jsonify({"error": "Доступ заборонено"}), 403
    
    data = request.json
    with open('static/data/news.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return jsonify({"message": "Новина оновлена"})
