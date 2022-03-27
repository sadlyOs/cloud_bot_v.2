import psycopg2
from db.password import host, dbname, user, password


class Database:
    def __init__(self, host, dbname, user, password):
        self.conn = psycopg2.connect(host=host, database=dbname, user=user, password=password)
        self.cursor = self.conn.cursor()

    def add_users_id(self, id_):

        """Сохраняем айди пользователей"""

        self.cursor.execute(f"SELECT user_id FROM users WHERE user_id = {id_}")
        if self.cursor.fetchone() is None:
            self.cursor.execute(f"INSERT INTO users (user_id, user_id_for_count) VALUES ({id_}, {id_})")
            self.conn.commit()
            return "Приветствую"
        return "Приветствую"

    def add_catigories(self, catigories, id_):

        """Сохраняем айди пользователей и названия категорий"""

        self.cursor.execute(f"SELECT categories FROM users WHERE user_id = {id_} AND categories = '{catigories}'")
        if self.cursor.fetchone() is None:
            self.cursor.execute(f"INSERT INTO users (user_id, categories) VALUES ({id_}, '{catigories}')")
            self.conn.commit()
            return f"Категория {catigories} успешна создана"
        return "Данная категория уже существует"

    def add_id_photo(self, id_, catigories, id_photo):

        """Сохраняем айди пользователей, названия категорий, айди фоток и распределяем их по именаа категорий"""

        self.cursor.execute(f"SELECT categories FROM users WHERE user_id = {id_} AND categories = '{catigories}'")
        if self.cursor.fetchone() is None:
            return "Такой категории не существует"

        self.cursor.execute(
            f"INSERT INTO users (user_id, categories, photo_id) VALUES ({id_}, '{catigories}', '{id_photo}')")
        self.conn.commit()
        return f"Фотография сохранена в категорию '{catigories}'"

    def print_photos(self, id_, catigories):

        """Выводим все фото по именям категорий"""

        self.cursor.execute(f"SELECT categories FROM users WHERE user_id = {id_} AND categories = '{catigories}'")
        if self.cursor.fetchone() is None:
            return 0
        list_photos = []
        self.cursor.execute(f"SELECT photo_id FROM users WHERE user_id = {id_} AND categories = '{catigories}'")
        for i in self.cursor.fetchall():
            if i[0] is None:
                continue
            list_photos.append(i[0])
        return list_photos

    def info_count_users(self):
        self.cursor.execute("SELECT COUNT(user_id_for_count) FROM users WHERE user_id_for_count != NULL")
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()


"""
conn = psycopg2.connect(database=dbname, user=user, password=password, host=host)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    user_id INT,
    categories VARCHAR(30),
    photo_id VARCHAR(200),
    user_id_for_count INT   
);''')
conn.commit()
"""

