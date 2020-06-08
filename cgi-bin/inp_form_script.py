#!/usr/bin/env python3
import cgi
import html
import sys
import os
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

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS,
                        host=DB_HOST, port=DB_PORT)  # соединяемся с базой
cursor = conn.cursor()
form = cgi.FieldStorage()  # получение формы
email = form.getvalue("user_adress")
password = str(form.getvalue("user_password"))
try:
    cursor.execute(
        'SELECT * FROM users WHERE adress = %(email)s', {'email': email})  # по емейлу собираем все данные
    info = cursor.fetchall()  # получить все данные
    d_password = str(info[0][6])  # для сравнения паролей

    if (password == d_password):  # на случай, если пароль совпал
        code = pyqrcode.create(
            "Скидка:"+str(info[0][8])+"%", encoding='utf-8')  # генерация кода
        # Место сохранения и параметры
        code.png('qr-codes\\'+str(info[0][9])+'.png', scale=8)
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
        print(
            '  <img src=\"../qr-codes\\'+str(info[0][9])+'.png\">  ')
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
    print("<h1>Email отсутствует в базе!</h1>")
    print("<a href=\"../input_form.html\">назад</a>")
    print("""</body>
         </html>""")

# if flag == True:
#     path = 'qr-codes\\'+id_for_unistall+'.png'
#     os.remove(path)
