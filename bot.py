from db.password import host, dbname, user, password
from aiogram.utils.exceptions import ValidationError
from aiogram.dispatcher import FSMContext
from aiogram import types, executor
from aiogram.types import InputMediaPhoto
from dispatchers import bot, dp
from db.main import Database
from states.State import States
from info_file import info

database = Database(host, dbname, user, password)


@dp.message_handler(commands=['start'])
async def add_user_id(msg: types.Message):
    id_user = msg.from_user.id
    await msg.answer(database.add_users_id(id_user))
    await msg.answer("Приветствую, введите /info,чтобы узнать о командах")


@dp.message_handler(commands=['add_photo'], state=None)
async def get_photo_id(msg: types.Message):
    await bot.send_message(msg.from_user.id,
                           "Отправьте категорею, в которой вы сохраните фото\nУкажите категорию по примеру: #котики")
    await States.state1.set()


@dp.message_handler(state=States.state1)
async def answer1(msg: types.Message, state: FSMContext):
    await state.update_data(
        {"answer1": msg.text}
    )
    await bot.send_message(msg.from_user.id,
                           "Отправьте фотографию для хранения")
    await States.next()


@dp.message_handler(content_types=['photo'], state=States.state2)
async def answer2(msg: types.Message, state: FSMContext):
    id_ = msg.from_user.id
    data = await state.get_data()
    answers1 = data.get("answer1")
    answers2 = msg.photo[0].file_id
    if answers1.startswith('#'):
        message = answers1.replace('#', '')
        await bot.send_message(id_, database.add_id_photo(id_, message, answers2))
        await state.finish()
    else:
        await bot.send_message(id_,
                               "Вы должны прописать категорию через хэштег и вместо текста вы должны отправить фотку")
        await state.finish()


@dp.message_handler(commands=['print_photo'])
async def print_photos(msg: types.Message):
    id_ = msg.from_user.id
    categories = msg.text.replace("/print_photo", "").strip()
    list_photos = database.print_photos(id_, categories)
    if list_photos == 0:
        await bot.send_message(id_, "Такой категории не существует")
    else:
        try:
            media = []
            for photo_id in list_photos:
                media.append(InputMediaPhoto(photo_id))
            await bot.send_media_group(id_, media)
        except ValidationError:
            await bot.send_message(id_, "Чтобы вывести фоток в категории должно быть более 1 фото")


@dp.message_handler(commands=['info'])
async def info_func(msg: types.Message):
    await msg.answer(info)


@dp.message_handler(commands=['info_count_users'])
async def info_users(msg: types.Message):
    await msg.answer(database.info_count_users())


@dp.message_handler()
async def hash_check(msg: types.Message):
    id_user = msg.from_user.id
    message = msg.text
    if message.startswith('#'):
        message = message.replace('#', '')
        await msg.answer(database.add_catigories(message, id_user))
    else:
        await msg.answer('Попробуйте /info')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
