#!/usr/bin/env python3
import cgi
import html
import sys
import codecs
import psycopg2
from psycopg2 import sql
import sqlite3
import pyqrcode

DB_NAME = "coursework"  # Данные бд Паши
DB_USER = "yarik"
DB_PASS = "6A0k8W8u"
DB_HOST = "eaplfm.com"
DB_PORT = "5432"  

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS,
                            host=DB_HOST, port=DB_PORT)  # соединяемся с базой
    cursor = conn.cursor()
    form = cgi.FieldStorage()  # получение формы
    email = form.getvalue("user_adress")
    password = str(form.getvalue("user_password"))

    cursor.execute(
        'SELECT * FROM users WHERE adress = %(email)s', {'email': email})  # по емейлу собираем все данные
    info = cursor.fetchall()  # получить все данные
    d_password = str(info[0][6])  # для сравнения паролей

    if (password == d_password):  # на случай, если пароль совпал
        code = pyqrcode.create(
            "Скидка:"+str(info[0][8])+"%", encoding='utf-8')  # генерация кода
        code.png('qr-codes\\qr.png', scale=8)  # Место сохранения и параметры
        print("Content-type: text/html\n")
        print("""<!DOCTYPE HTML>
         <html>
         <head>
             <meta charset="UTF-8">
             <title>Страница пользователя</title>
         </head>
         <body>""")
        print("<h1>Добрый день, " + info[0]
              [1] + " " + info[0][0] + "!"+"</h1>")
        print("<br />Ваш qr-code:<br />")
        print("<img src=\"../qr-codes\\qr.png\" alt=\"Ошибка qr-code\">")
        print("""</body>
         </html>""")
    else:  # если пароль оказался неверным
        print("Content-type: text/html\n")
        print("""<!DOCTYPE HTML>
         <html>
         <head>
             <meta charset="UTF-8">
             <title>Ошибка входа!</title>
         </head>
         <body>""")
        print("<h1>Неверный логин или пароль!</h1>")
        print("<a href=\"../input_form.html\">назад</a>")
        print("""</body>
         </html>""")

except:  # если email'a нет в базе
    print("Content-type: text/html\n")
    print("""<!DOCTYPE HTML>
         <html>
         <head>
             <meta charset="UTF-8">
             <title>Ошибка входа!</title>
         </head>
         <body>""")
    print("<h1>Неверный логин или пароль!</h1>")
    print("<a href=\"../input_form.html\">назад</a>")
    print("""</body>
         </html>""")
