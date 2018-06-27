"""
Need to move from SQLite to PostgreSQL Database -- DONE
"""

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
    cur.execute("SELECT * FROM users ORDER BY user_id DESC LIMIT 1;")
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

#"CREATE TABLE task_history(id SERIAL PRIMARY KEY, task JSONB, user_id INTEGER, task_result INTEGER);"

def get_last_task_id():
    cur.execute("SELECT * FROM task_history ORDER BY id DESC LIMIT 1;")
    return cur.fetchone()


def add_task_to_history(user_id, task, task_result):
    task_json = task.json()
    cur.execute("""
    INSERT INTO task_history (task, user_id, task_result)
    VALUES (%s, %s, %s);
    """,
    (task_json, user_id, task_result))
    db.commit()


def get_tasks_from_history(user_id, tasks_count=-1):
    cur.execute("SELECT task, task_result FROM task_history WHERE user_id = %s;", (user_id,))
    tasks = cur.fetchall()
    real_tasks_count = len(tasks)
    if (tasks_count == -1):
        tasks_count = real_tasks_count
    if (tasks_count <= real_tasks_count):
        return ((task[0], task[1]) for task in cur.fetchall())[-tasks_count:]
    else:
        logging.critical("User doesn't have enough tasks")


def clear_task_history(user_id):
    cur.execute("DELETE FROM task_history WHERE user_id = %s;", (user_id,))
    db.commit()


def delete_user(user_id):
    clear_task_history(user_id)
    cur.execute("DELETE FROM users WHERE user_id = %s;", (user_id,))
    db.commit()
