"""
Need to move from SQLite to PostgreSQL Database
"""


import sqlite3 as sqlite
from distutils import dist
from code import config
import time
import random as rd


def add_user(message):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE user_id = (?)", (message.from_user.id,))
    except Exception as e:
        config.log(Error=e, Text="DBTESTING ERROR")
    if not cur.fetchone():
        try:
            cur.execute("INSERT INTO users (user_id, first_name, last_name, username) VALUES (?,?,?,?)", (
                message.from_user.id,
                message.from_user.first_name,
                message.from_user.last_name,
                message.from_user.username))
            config.log(Text="User successfully added",
                       user=str(message.from_user.first_name + " " + message.from_user.last_name))
        except Exception as e:
            config.log(Error=e, Text="USER_ADDING_ERROR")
        db.commit()
    else:
        config.log(Error="IN_THE_BASE_YET",
                   id=message.from_user.id,
                   info=str(message.from_user.last_name) + " " + str(message.from_user.first_name),
                   username=message.from_user.username)
    db.close()


def quot():
    i = rd.randint(1, 767)
    print(i)
    db = sqlite.connect("C:/Users/Nick/Desktop/clientbase.db")
    cur = db.cursor()
    try:
        cur.execute("SELECT * FROM Quotations WHERE id = (?)", (i,))
        string = cur.fetchone()
        return (str(string[1]) + string[2])
    except Exception as e:
        config.log(Error=e, Text="NO_SUCH_QUOTATION_ID = " + str(i))
        return quot()
    db.close()


def kickass():
    i = rd.randint(1, 767)
    print(i)
    db = sqlite.connect("C:/Users/Nick/Desktop/clientbase.db")
    cur = db.cursor()
    try:
        cur.execute("SELECT * FROM motivate WHERE id = (?)", (i,))
    except Exception as e:
        config.log(Error=e, Text="NO_SUCH_MOTIVAION_ID = " + str(i))
        return kickass()
    db.close()


def set_todo(user_id, activity_name, start_time, finish_time, description, frequency):
    db = sqlite.connect("C:/Users/Nick/Desktop/clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (str(user_id),))
    is_todo = cur.fetchone()
    if is_todo[5]:
        try:
            cur.execute(
                "INSERT INTO '{table}' (activity_name, start_time, finish_time, description, frequency)  VALUES (?,?,?,?,?)".format(table=user_id), (activity_name, start_time, finish_time, description, frequency,))
            db.commit()
        except Exception as e:
            config.log(Error=e, text="INSERTING_TODO_ERROR")
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
