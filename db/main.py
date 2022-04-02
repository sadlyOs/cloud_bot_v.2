import psycopg2
from psycopg2 import InterfaceError
from db.password import host, dbname, user, password


class Database:
    def __init__(self, host, dbname, user, password):
        self.conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)

    def add_users_id(self, id_):

        """Сохраняем айди пользователей"""
        with self.conn.cursor() as cursor:
            cursor.execute(f"SELECT user_id FROM all_tg_users WHERE user_id = {id_}")
            if cursor.fetchone() is None:
                cursor.execute(f"INSERT INTO all_tg_users (user_id, user_count) VALUES ({id_}, {id_})")
                self.conn.commit()

    def add_catigories(self, catigories, id_):

        """Сохраняем айди пользователей и названия категорий"""
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"SELECT categories FROM all_tg_users WHERE user_id = {id_} AND categories = '{catigories}'")
            if cursor.fetchone() is None:
                cursor.execute(f"INSERT INTO all_tg_users (user_id, categories) VALUES ({id_}, '{catigories}')")
                self.conn.commit()
                return f"Категория {catigories} успешна создана"
            return "Данная категория уже существует"

    def add_id_photo(self, id_, catigories, key_id, hash_photo, photo_id):

        """Сохраняем айди пользователей, названия категорий, айди фоток и распределяем их по именам категорий"""
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"SELECT categories FROM all_tg_users WHERE user_id = {id_} AND categories = '{catigories}'")
            if cursor.fetchone() is None:
                return "У вас нет фотографий"

            cursor.execute(
                f"INSERT INTO all_tg_users (user_id, categories, key_id_photo, hash_id_photo, photo_id) VALUES ({id_}, '{catigories}', {key_id}, '{hash_photo}', '{photo_id}')")  # Добовляем хэш и ключ
            self.conn.commit()
            return f"Фотография сохранена в категорию '{catigories}'"

    def print_photos(self, id_, catigories, keyid):

        """Выводим все фото по именям категорий"""
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"SELECT categories FROM all_tg_users WHERE user_id = {id_} AND categories = '{catigories}' AND key_id_photo = {keyid}")
            if cursor.fetchone() is None:
                return 0
            list_photos = []
            cursor.execute(
                f"SELECT photo_id FROM all_tg_users WHERE user_id = {id_} AND categories = '{catigories}'")
            for i in cursor.fetchall():
                if i[0] is None:
                    continue
                list_photos.append(i[0])
            return list_photos

    def return_catigories(self, id_):

        """ Парсим категории в список list_categories и возвращаем его """
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"SELECT categories FROM all_tg_users WHERE user_id = {id_}")  # проверяем на существенность категорий
            if cursor.fetchall() is None:
                return
            list_categories = []
            cursor.execute(f"SELECT categories FROM all_tg_users WHERE user_id = {id_}")
            rows = cursor.fetchall()
            for row in rows:
                if row[0] is None:
                    continue  # Пропускаем добавление пустых значений
                list_categories.append(row[0])
            return list_categories

    def del_categories(self, id_, categories):
        """ Удаление категорий """
        with self.conn.cursor() as cursor:
            cursor.execute(
                f"DELETE  FROM all_tg_users WHERE user_id = {id_} AND categories = '{categories}'")
            self.conn.commit()
            return f"Категория '{categories}' успешно удалена, теперь, чтобы снова появилась клавиатура добавьте категорию или нажмите на /start"


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
