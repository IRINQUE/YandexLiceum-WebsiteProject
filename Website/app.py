from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.db'
db = SQLAlchemy(app)

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
        

@app.route('/')
def mainpage():
    return render_template('Main.html')

@app.route('/generator', methods=['post', "GET"])
def generator():
    if request.method == "POST":
        Parameters = list()
        for req in request.form:
            if req[0:2] == "Us" or req[0:2] == "Pa":
                Parameters.append(req)
        PasswordLength = request.form.get('PasswordLen')
        generate(Parameters, PasswordLength)
        return render_template('Generator.html', FivthPasswords = FivthPasswords)
    return render_template('Generator.html')

@app.route('/passwords')
def passwords():
    return render_template('Passwords.html')

if __name__ == "__main__":
    app.run()