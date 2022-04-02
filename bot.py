from db.password import host, dbname, user, password
from aiogram.utils.exceptions import ValidationError
from aiogram.dispatcher import FSMContext
from aiogram import types, executor
from aiogram.types import InputMediaPhoto
from inline.inlinekey import create_choice, add_key
from dispatchers import bot, dp
from db.main import Database
from states.State import States, State_s, State_del
from info_file import info
import hashlib

database = Database(host, dbname, user, password)


@dp.message_handler(commands=['start'])
async def add_user_id(msg: types.Message):
    id_user = msg.from_user.id
    print(database.add_users_id(id_user))
    choice = create_choice()
    a = database.return_catigories(id_user)
    if not a:
        await msg.answer(
            """Добавьте одну категорию,чтобы появилась клавиатура,после добавление ещё раз нажмите старт\n
Чтобы посмотреть как создать категорию нажмие на /info""")
        return
    await msg.answer(text="Приветствую,нажми /info, чтобы узнать о командах", reply_markup=choice)  # Выводим клавиатуру


@dp.callback_query_handler(text_contains='but1', state=None)
async def get_photo_id(call: types.CallbackQuery):
    """ Проверяем нажатие первой кнопки """

    global id_
    await call.answer(cache_time=60)
    id_ = call.from_user.id  # Получаем id_user
    a = database.return_catigories(id_)
    if not a:
        await call.answer(
            """Добавьте одну категорию,чтобы появилась клавиатура,после добавление ещё раз нажмите старт\n
Чтобы посмотреть как создать категорию нажмие на /info""")
        return
    await bot.send_message(call.from_user.id,
                           "Выберите категорею, в которой вы сохраните фото",
                           reply_markup=add_key(id_))  # Выводим категории в виде кнопок
    await States.state1.set()


@dp.callback_query_handler(lambda answ: answ.data in database.return_catigories(id_),
                           state=States.state1)  # Проверяем название нажатой кнопки в списке категорий
async def answer(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    catigori = call.data  # Сохраняем название кнопки
    await state.update_data(
        {"answer1": catigori}  # Сохраняем catigori в answer1
    )
    await bot.send_message(id_, "Теперь отправьте фотку для хранения")
    await States.next()


@dp.message_handler(content_types=['photo'], state=States.state2)
async def save_photo(msg: types.Message, state: FSMContext):
    """Запрашиваем фото и получаем айди фото"""

    data = await state.get_data()
    answer1 = data.get("answer1")  # Получаем данные из answer1
    answer2 = msg.photo[0].file_id  # Получаем айди фотки
    keyid = id_ - 10000 * 10  # Создаём ключ для расшифровки
    hash_id_photo = hashlib.md5(answer2.encode('utf-8'))  # Хэшируем айди фоток, используя md5
    await bot.send_message(id_,
                           database.add_id_photo(id_, answer1, keyid, hash_id_photo.hexdigest(),
                                                 answer2))  # Сохраняем айди,категорию и айди фотки
    await state.finish()  # Заканчиваем состояние


@dp.callback_query_handler(text="buttton", state=None)
async def choice(call: types.CallbackQuery, state: FSMContext):
    """Проверяем нажатие второй кнопки и выводим фотографии по выбранным категориям"""

    global ids
    await call.answer(cache_time=60)
    ids = call.from_user.id
    a = database.return_catigories(ids)
    if not a:
        await call.answer(
            """Добавьте одну категорию,чтобы появилась клавиатура,после добавление ещё раз нажмите старт\n
Чтобы посмотреть как создать категорию нажмие на /info""")
        return
    await bot.send_message(call.from_user.id,
                           "Выберите категорею, в которой вы сохраните фото",
                           reply_markup=add_key(ids))
    await State_s.state1.set()


@dp.callback_query_handler(lambda answ: answ.data in database.return_catigories(ids),
                           state=State_s.state1)  # Проверяем название нажатой кнопки в списке категорий
async def answer(call: types.CallbackQuery, state: FSMContext):
    categories = call.data  # Получаем айди категорий
    keyid = ids - 10000 * 10  # Указываем ключ
    list_photos = database.print_photos(ids, categories, keyid)  # Получаем возвращаемый список айди фотографий
    print(list_photos)
    if list_photos == 0:
        await bot.send_message(id_, "Такой категории не существует")  # Если вместо списка получили ложный вызов
    else:
        try:
            """Выводим все фотки с категории в альбомном виде"""
            media = []
            for photo_id in list_photos:
                media.append(InputMediaPhoto(photo_id))
            await bot.send_media_group(ids, media)
        except ValidationError:
            await bot.send_message(ids, "Чтобы вывести фоток в категории должно быть более 1 фото")
    await state.finish()


@dp.callback_query_handler(text_contains='del', state=None)
async def choice_butt(call: types.CallbackQuery):
    """Проверяем нажатие второй кнопки и удаляем выбранную категорию"""

    global id_s
    await call.answer(cache_time=60)
    id_s = call.from_user.id
    await bot.send_message(id_s, "Выберите категорию для удаления", reply_markup=add_key(id_s))
    await State_del.state1.set()


@dp.callback_query_handler(lambda answ: answ.data in database.return_catigories(id_s), state=State_del.state1)
async def cati_del(call: types.CallbackQuery, state: FSMContext):
    categori = call.data
    await call.answer(text=database.del_categories(id_s, categori), show_alert=True)
    await state.finish()


@dp.message_handler(commands=['info'])
async def info_func(msg: types.Message):
    await msg.answer(info)


@dp.message_handler()
async def hash_check(msg: types.Message):
    """Создаём новую категорию"""
    id_user = msg.from_user.id
    message = msg.text
    if message.startswith('#'):
        message = message.replace('#', '')
        await msg.answer(database.add_catigories(message, id_user))
    else:
        await msg.answer('Попробуйте /info')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
