#!/usr/bin/env python3
import cgi
import html
import sys
import codecs
import psycopg2
from psycopg2 import sql
import sqlite3

DB_NAME = "coursework"  # Данные бд Паши
DB_USER = "yarik"
DB_PASS = "6A0k8W8u"
DB_HOST = "eaplfm.com"
DB_PORT = "5432"

# для исправления бага с отображением, вроде бы кодировку меняет
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS,
                            host=DB_HOST, port=DB_PORT)  # соединяемся с базой
    cursor = conn.cursor()  # получаем курсор к базе
    form = cgi.FieldStorage()  # получение формы
    # escape используем, чтобы предотвратить уязвимость при заполнении
    name = html.escape(form.getfirst("name"))
    sname = html.escape(form.getfirst("sname"))
    try:  # Если отчество не указано, то об этом будет сообщаться
        patr = html.escape(form.getfirst("patr"))
    except:
        patr = "Не указано"
    age = html.escape(form.getvalue("age"))
    gender = html.escape(form.getvalue("gender"))
    adress = form.getvalue("adress")
    password = form.getvalue("password")
    mailing = form.getvalue("mailing")
    if mailing == "on":  # получаем булевское значение
        mailing = True
        discount = 7  # размер скидки зависит от подтверждения рассылки
    else:
        mailing = False
        discount = 5

    conn.autocommit = True
    values = [
        (name, sname, patr, age, gender, adress, password,
         mailing, discount)  # все поля для заполнения
    ]
    insert = sql.SQL('INSERT INTO users VALUES {}').format(  # переменная, чтобы в последующем работало помещение в бд
        sql.SQL(',').join(map(sql.Literal, values)))
    cursor.execute(insert)
    conn.close()  # закрываем
    print("Content-type: text/html\n")
    print("""<!DOCTYPE HTML>
         <html>
         <head>
             <meta charset="UTF-8">
             <link rel="stylesheet" href="../stylesheets/user_page.css" />
             <title>Спасибо за регистрацию!</title>
         </head>
         <body>
         <div class="nav">
      <a href="../index.html">Главная</a>
    </div>""")
    print("<h1>Благодарим вас за регистрацию!</h1>")
#print("<a href=\"../index.html\">На главную</a>")
    print("""</body>
         </html>""")
except:
    print("Content-type: text/html\n")
    print("""<!DOCTYPE HTML>
         <html>
         <head>
             <meta charset="UTF-8">
             <title>Подключение к бд</title>
         </head>
         <body>""")
    print("<h1>Ошибка!</h1>")
    print("""</body>
         </html>""")
