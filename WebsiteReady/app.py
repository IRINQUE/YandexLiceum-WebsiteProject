from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import random
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, UserMixin, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'IRINQUE_TOP7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app=app)

login_manager = LoginManager()
login_manager.login_view = '/'
login_manager.session_protection = 'strong'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return '<users %r>' % self.id


class Passwords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(100), unique=True)
    P1 = db.Column(db.Text())
    P2 = db.Column(db.Text())
    P3 = db.Column(db.Text())
    P4 = db.Column(db.Text())
    L1 = db.Column(db.Text())
    L2 = db.Column(db.Text())
    L3 = db.Column(db.Text())
    L4 = db.Column(db.Text())

    def __repr__(self):
        return '<passwords %r>' % self.id
      
def generate(Parameters, PasswordLength):
    global FivthPasswords
    SmallChars = "abcdefghijklmnopqrstuvwxyz"
    BigChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    Nums = "0123456789"
    SpecialChars = "#%&$@"

    Chars = []
    FivthPasswords = list()
    for Param in Parameters:
        if Param == "UseNum":
            Chars += Nums
        if Param == "UseLettersSmall":
            Chars += SmallChars
        if Param == "UseLettersBig":
            Chars += BigChars
        if Param == "UseSpecialLetters":
            Chars += SpecialChars

    for n in range(5):
        password =''
        for i in range(int(PasswordLength)):
            password += random.choice(Chars)
        FivthPasswords.append(password)
    return FivthPasswords

# Страничка LogOut(Готово 8.04.23)     
@app.route('/logout')
@login_required
def logout():
    # Проверка Авторизации
    if current_user.is_authenticated:
        # Деавторизация Пользователя
        logout_user()
        # Перенаправление на Главную Страницу
        return redirect(url_for('mainpage'))
    else:
        # Перенаправление на Главную Страницу
        return redirect(url_for('mainpage'))

""" <-- содержимое сайта  --> """
# Страница Главная(Готово 8.04.23)   
@app.route('/')
def mainpage():
    return render_template('PageMain.html')


""" <-- ФУНКЦИЯ САЙТА --> """
# Страница Генератор(Готово 8.04.23)   
@app.route('/generator', methods=['POST', "GET"])
def generator():
    if request.method == "POST":
        Parameters = list()
        for req in request.form:
            if req[0:2] == "Us" or req[0:2] == "Pa":
                Parameters.append(req)
        PasswordLength = request.form.get('PasswordLen')
        generate(Parameters, PasswordLength)
        return render_template('FuncGenerator.html', FivthPasswords = FivthPasswords)
    return render_template('FuncGenerator.html')


""" <-- ЗАМЕТКИ ПОЛЬЗОВАТЕЛЕЙ --> """
# Страница Заметки(Готово 8.04.23)   
@app.route('/notes', methods=['POST', "GET"])
@login_required
def notes():
    if current_user.is_authenticated:
        # Перенос на страничку с паролем 1
        if "PasswordButton1" in request.form:
            return redirect(url_for('userpassword1'))
        # Перенос на страничку с паролем 2
        if "PasswordButton2" in request.form:
            return redirect(url_for('userpassword2'))
        # Перенос на страничку с паролем 3
        if "PasswordButton3" in request.form:
            return redirect(url_for('userpassword3'))
        # Перенос на страничку с паролем 4
        if "PasswordButton4" in request.form:
            return redirect(url_for('userpassword4'))
    # Возврат На страничку Notes   
    return render_template('FuncNotes.html')


""" <-- РАБОТА С АККАУНТАМИ ПОЛЬЗОВАТЕЛЕЙ --> """  
# Страница Регистрация(Готово 8.04.23)   
@app.route('/registration', methods=['POST', "GET"])
def registration(): 
    if request.method == "POST":
        try:
            if "RegisterData" in request.form:     
                password_hash = generate_password_hash(request.form['Password'])
                user = User(nickname=request.form['Username'], password=password_hash)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
        except:
            print("Error")
        return render_template('FuncRegistration.html')
    return render_template('FuncRegistration.html')

# Страница Логин(Готово 8.04.23)   
@app.route('/login', methods=['POST', "GET"])
def login():
    # Проверка Авторизации
    if current_user.is_authenticated:
        # Возврат К Страничке с Заметками
        return redirect(url_for('notes'))  
    else:
        # Если метод передачи информации
        if request.method == "POST":
            try:
                # Если кнопка возврата к главной странице
                if "ToRegButton" in request.form:
                    return redirect(url_for('registration')) # Перенос к Mainpage
                UserPassword = request.form['Password'] # Пароль Пользователя
                Nickname = request.form["Username"] # Никнейм Пользователя
                user = User.query.filter_by(nickname=Nickname).first() # Все данные о пользователе
                if check_password_hash(user.password, UserPassword): # Проверка Правильности пароля
                    login_user(user, remember=False) # Авторизация Пользователя
                    return redirect(url_for('notes')) # Редирект к Notes  
            except:   
                return render_template('FuncLogin.html') # Загрузка Страницы LoginHTML
    return render_template('FuncLogin.html') # Загрузка Страницы LoginHTML


"""                                                                                  <-- ПАРОЛИ ПОЛЬЗОВАТЕЛЕЙ -->                                                                                   """
# Пароль 1(Готово 8.04.23) 
@app.route('/userpassword1', methods=['POST', 'GET'])
@login_required
def userpassword1():
    if current_user.is_authenticated:
        if request.method == "POST" and "SaveData" in request.form: # Если передаются данные
            UserData = Passwords.query.filter_by(nickname=current_user.nickname).first() # Все данные о пользователе
            UserPassword = request.form['Password'] # Получаем Пароль из Формы
            UserNickname = request.form["Username"] # Получаем Логин из Формы
            UserData.L1 = UserNickname # Обновляем Логин
            UserData.P1 = UserPassword # Обновляем Пароль
            db.session.commit() # Подтверждаем Операцию
        UserData = Passwords.query.filter_by(nickname=current_user.nickname).first() # Все данные о пользователе
        return render_template('UserPassword1.html', Username=UserData.L1, Password=UserData.P1) # Выводим данные

# Пароль 2(Готово 8.04.23) 
@app.route('/userpassword2', methods=['POST', 'GET'])
@login_required
def userpassword2():
    if current_user.is_authenticated:
        if request.method == "POST" and "SaveData" in request.form: # Если передаются данные
            UserData = Passwords.query.filter_by(nickname=current_user.nickname).first() # Все данные о пользователе
            UserPassword = request.form['Password'] # Получаем Пароль из Формы
            UserNickname = request.form["Username"] # Получаем Логин из Формы
            UserData.L2 = UserNickname # Обновляем Логин
            UserData.P2 = UserPassword # Обновляем Пароль
            db.session.commit() # Подтверждаем Операцию
        UserData = Passwords.query.filter_by(nickname=current_user.nickname).first() # Все данные о пользователе
        return render_template('UserPassword2.html', Username=UserData.L2, Password=UserData.P2) # Выводим данные

# Пароль 3(Готово 8.04.23) 
@app.route('/userpassword3', methods=['POST', 'GET'])
@login_required
def userpassword3():
    if current_user.is_authenticated:
        if request.method == "POST" and "SaveData" in request.form: # Если передаются данные
            UserData = Passwords.query.filter_by(nickname=current_user.nickname).first() # Все данные о пользователе
            UserPassword = request.form['Password'] # Получаем Пароль из Формы
            UserNickname = request.form["Username"] # Получаем Логин из Формы
            UserData.L3 = UserNickname # Обновляем Логин
            UserData.P3 = UserPassword # Обновляем Пароль
            db.session.commit() # Подтверждаем Операцию
        UserData = Passwords.query.filter_by(nickname=current_user.nickname).first() # Все данные о пользователе
        return render_template('UserPassword3.html', Username=UserData.L3, Password=UserData.P3) # Выводим данные

# Пароль 4(Готово 8.04.23) 
@app.route('/userpassword4', methods=['POST', 'GET'])
@login_required
def userpassword4():
    if current_user.is_authenticated:
        if request.method == "POST" and "SaveData" in request.form: # Если передаются данные
            UserData = Passwords.query.filter_by(nickname=current_user.nickname).first() # Все данные о пользователе
            UserPassword = request.form['Password'] # Получаем Пароль из Формы
            UserNickname = request.form["Username"] # Получаем Логин из Формы
            UserData.L4 = UserNickname # Обновляем Логин
            UserData.P4 = UserPassword # Обновляем Пароль
            db.session.commit() # Подтверждаем Операцию
        UserData = Passwords.query.filter_by(nickname=current_user.nickname).first() # Все данные о пользователе
        return render_template('UserPassword1.html', Username=UserData.L4, Password=UserData.P4) # Выводим данные

# Запуск Приложения
if __name__ == "__main__":
    app.run()