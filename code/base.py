import logging
import psycopg2 as pg

# "CREATE TABLE users(user_id SERIAL, user_name TEXT, vk_uid INTEGER, tg_uid INTEGER);"


class DatabaseConnection:
    # use with context managers:
    #   with database as
    def __enter__(self):
        try:
            self.__conn = pg.connect(self._configs)
        except pg.Error as e:
            logging.critical("%s occurred while connecting PostgreSQL Database" % str(e))
        return self.__conn.cur()

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.__conn.commit()
        except pg.Error as e:
            logging.critical("%s occurred, can\'t save data, changes would be reverted" % str(e))
        self.__conn.close()


def get_user_id(mode, uid):
    if mode is not 'tg' and mode is not 'vk':
        raise Exception('Wrong user_id mode called - %s' % mode)
    request = 'SELECT user_id FROM users WHERE %s_uid =' % mode
    request += '%s;'
    with DatabaseConnection() as cur:
        cur.execute(request, (uid, ))
        return cur.fetchone()


def get_last_user_id():
    with DatabaseConnection() as cur:
        cur.execute("SELECT * FROM users ORDER BY user_id DESC LIMIT 1;")
        return cur.fetchone()


def add_vk_id(user_id, vk_uid):
    with DatabaseConnection() as cur:
        cur.execute("UPDATE users SET vk_uid = %s WHERE user_id = %s;", (vk_uid, user_id))


def add_tg_id(user_id, tg_uid):
    with DatabaseConnection() as cur:
        cur.execute("UPDATE users SET tg_uid = %s WHERE user_id = %s;", (tg_uid, user_id))


# mode types: 'vk' | 'tg'
def add_user(user_name, mode, chat_uid):
    with DatabaseConnection() as cur:
        cur.execute("SELECT * FROM users WHERE user_name = %s", (user_name,))
        if not cur.fetchone():
            cur.execute("INSERT INTO users (user_name) VALUES (%s);", (user_name,))
            user_id = get_last_user_id()
            if mode == 'vk':
                add_vk_id(user_id, chat_uid)
            else:
                add_tg_id(user_id, chat_uid)
        else:
            logging.critical('User already exists')


# "CREATE TABLE task_history(id SERIAL PRIMARY KEY, task JSONB, user_id INTEGER, task_result INTEGER);"

def get_last_task_id():
    with DatabaseConnection() as cur:
        cur.execute("SELECT * FROM task_history ORDER BY id DESC LIMIT 1;")
        return cur.fetchone()


def add_task_to_history(user_id, task, task_result):
    task_json = task.json()
    with DatabaseConnection() as cur:
        cur.execute("INSERT INTO task_history (task, user_id, task_result) VALUES (%s, %s, %s);",
                    (task_json, user_id, task_result))


def get_tasks_from_history(user_id, tasks_count=-1):
    with DatabaseConnection() as cur:
        cur.execute("SELECT task, task_result FROM task_history WHERE user_id = %s;", (user_id,))
        tasks = cur.fetchall()
        real_tasks_count = len(tasks)
        if tasks_count == -1:
            tasks_count = real_tasks_count
        if tasks_count <= real_tasks_count:
            return ((task[0], task[1]) for task in cur.fetchall())[-tasks_count:]
        else:
            logging.critical("User doesn't have enough tasks")


def clear_task_history(user_id):
    with DatabaseConnection() as cur:
        cur.execute("DELETE FROM task_history WHERE user_id = %s;", (user_id,))


def delete_user(user_id):
    clear_task_history(user_id)
    with DatabaseConnection() as cur:
        cur.execute("DELETE FROM users WHERE user_id = %s;", (user_id,))
