"""
Need to move from SQLite to PostgreSQL Database -- что-то уже есть
Think about merge tasks
"""

import sqlite3 as sqlite
from distutils import dist
import time
import random as rd
import psycopg2
from simplejson import loads, dumps
from configs import db_configs
from psycopg2.extras import Json
import logging
from classes import Task

db = psycopg2.connect(**db_configs)
cur = db.cursor()

#"CREATE TABLE users(user_id SERIAL, user_name TEXT, vk_uid INTEGER, tg_uid INTEGER);"

def get_last_user_id():
    cur.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1;")
    return cur.fetchone()


def add_vk_id(user_id, vk_uid):
    cur.execute("""
        UPDATE users SET vk_uid = %s
        WHERE user_id = %s;
        """, 
        (vk_uid, user_id))
    db.commit()


def add_tg_id(user_id, tg_uid):
    cur.execute("""
        UPDATE users SET tg_uid = %s
        WHERE user_id = %s;
        """, 
        (tg_uid, user_id))
    db.commit()


def add_user(user_name, mode, chat_uid):
    cur.execute("SELECT * FROM users WHERE user_name = %s", (user_name,))
    if not cur.fetchone():
        cur.execute("""
        INSERT INTO users (user_name)
        VALUES (%s);
        """,
        (user_name,))
        db.commit()
        user_id = get_last_user_id()
        if mode == 'vk':
            add_vk_id(user_id, chat_uid)
        else:
            add_tg_id(user_id, chat_uid)
    else:
        logging.critical('User already exists')

"""
Сорян, что на русском
Че за quot???
Нигде про это нет
И kickass???
У нас нет таблички motivate...
"""

def quot():
    i = rd.randint(1, 767)
    print(i)
    db = sqlite.connect("C:/Users/Nick/Desktop/clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM Quotations WHERE id = (?)", (i,))
    string = cur.fetchone()
    return (str(string[1]) + string[2])
    db.close()


def kickass():
    i = rd.randint(1, 767)
    print(i)
    db = sqlite.connect("C:/Users/Nick/Desktop/clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM motivate WHERE id = (?)", (i,))
    db.close()

"""
Пошел осмысленный код
"""

#"CREATE TABLE task_history(id SERIAL PRIMARY KEY, task JSONB, uid INTEGER);"

def get_last_task_id():
    cur.execute("SELECT * FROM task_history ORDER BY id DESC LIMIT 1;")
    return cur.fetchone()

"""
Сюда придет class Task
"""

def add_task(user_id, task):
    task_json = task.json()
    cur.execute("""
    INSERT INTO task_history (task, uid)
    VALUES (%s, %s);
    """,
    (task_json, user_id))
    db.commit()

def set_todo(user_id, activity_name, start_time, finish_time, description, frequency):
    db = sqlite.connect("C:/Users/Nick/Desktop/clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (str(user_id),))
    is_todo = cur.fetchone()
    if is_todo[5]:
        cur.execute(
            "INSERT INTO '{table}' (activity_name, start_time, finish_time, description, frequency)  VALUES (?,?,?,?,?)".format(table=user_id), (activity_name, start_time, finish_time, description, frequency,))
        db.commit()
    else:
        s = '''CREATE TABLE {table} (id	INTEGER,activity_name	TEXT, start_time	REAL, finish_time	REAL, description	TEXT, frequency	INTEGER, PRIMARY KEY(id))'''.format(table=user_id)
        cur.execute(s)
        cur.execute("UPDATE users SET todos_t_name = {name} WHERE user_id = {id}".format(id=user_id, name=user_id))
        db.commit()
    db.close()


def get_todo(user_id):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    try:
        cur.execute("SELECT * FROM '{table}'".format(table=str(time.gmtime(time.time()).tm_mon)+'-'+str(time.gmtime(time.time()).tm_mday)))
    except Exception as e:
        print(e)
        cur.execute("CREATE TABLE %s(id INTEGER PRIMARY KEY, activity_name TEXT,"
                    "start_time REAL, finish_time REAL,"
                    " description TEXT" % str(str(time.gmtime(time.time())[1])+'-'+str(time.gmtime(time.time())[2])))
        return None
    data = cur.fetchall()
    return data
