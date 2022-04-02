import psycopg2
from db.password import host, dbname, user, password


class Database:
    def __init__(self, host, dbname, user, password):
        self.conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
        self.cursor = self.conn.cursor()

    def add_users_id(self, id_):

        """Сохраняем айди пользователей"""

        self.cursor.execute(f"SELECT user_id FROM all_tg_users WHERE user_id = {id_}")
        if self.cursor.fetchone() is None:
            self.cursor.execute(f"INSERT INTO all_tg_users (user_id, user_count) VALUES ({id_}, {id_})")
            return self.conn.commit()
        return

    def add_catigories(self, catigories, id_):

        """Сохраняем айди пользователей и названия категорий"""

        self.cursor.execute(
            f"SELECT categories FROM all_tg_users WHERE user_id = {id_} AND categories = '{catigories}'")
        if self.cursor.fetchone() is None:
            self.cursor.execute(f"INSERT INTO all_tg_users (user_id, categories) VALUES ({id_}, '{catigories}')")
            self.conn.commit()
            return f"Категория {catigories} успешна создана"
        return "Данная категория уже существует"

    def add_id_photo(self, id_, catigories, key_id, hash_photo, photo_id):

        """Сохраняем айди пользователей, названия категорий, айди фоток и распределяем их по именам категорий"""

        self.cursor.execute(
            f"SELECT categories FROM all_tg_users WHERE user_id = {id_} AND categories = '{catigories}'")
        if self.cursor.fetchone() is None:
            return "Такой категории не существует"

        self.cursor.execute(
            f"INSERT INTO all_tg_users (user_id, categories, key_id_photo, hash_id_photo, photo_id) VALUES ({id_}, '{catigories}', {key_id}, '{hash_photo}', '{photo_id}')")  # Добовляем хэш и ключ
        self.conn.commit()
        return f"Фотография сохранена в категорию '{catigories}'"

    def print_photos(self, id_, catigories, keyid):

        """Выводим все фото по именям категорий"""

        self.cursor.execute(
            f"SELECT categories FROM all_tg_users WHERE user_id = {id_} AND categories = '{catigories}' AND key_id_photo = {keyid}")
        if self.cursor.fetchone() is None:
            return 0
        list_photos = []
        self.cursor.execute(f"SELECT photo_id FROM all_tg_users WHERE user_id = {id_} AND categories = '{catigories}'")
        for i in self.cursor.fetchall():
            if i[0] is None:
                continue
            list_photos.append(i[0])
        return list_photos

    def return_catigories(self, id_):

        """ Парсим категории в список list_categories и возвращаем его """

        self.cursor.execute(
            f"SELECT categories FROM all_tg_users WHERE user_id = {id_}")  # проверяем на существенность категорий
        if self.cursor.fetchall() is None:
            return
        list_categories = []
        self.cursor.execute(f"SELECT categories FROM all_tg_users WHERE user_id = {id_}")
        rows = self.cursor.fetchall()
        for row in rows:
            if row[0] is None:
                continue  # Пропускаем добавление пустых значений
            list_categories.append(row[0])
        return list_categories

    def del_categories(self, id_, categories):
        """ Удаление категорий """

        self.cursor.execute(
            f"DELETE  FROM all_tg_users WHERE user_id = {id_} AND categories = '{categories}'")
        self.conn.commit()
        return f"Категория '{categories}' успешно удалена"

    def close(self):
        self.conn.close()


'''
conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE all_tg_users(
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    user_count BIGINT,
    categories VARCHAR(200),
    photo_id TEXT,
    hash_id_photo TEXT,
    key_id_photo BIGINT

)""")
conn.commit()'''
