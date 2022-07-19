from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.executor import start_webhook
from database.databaseimages import DatabaseImages
from database.databaseusers import DatabaseUsers
import os

TOKEN = '5593476084:AAFU3w39l1_gexGaS5A4thkmwTskahS38-E'
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot)

WEBHOOK_HOST = 'https://businessbot1.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT', default=5000))

db_images = DatabaseImages()
db_users = DatabaseUsers()

def keyboard(like, dislike):
    inline_keyboard = InlineKeyboardMarkup(row_width=2).row(
        InlineKeyboardButton(text=f'\U0001F44D {like}', callback_data='like_photo', one_time_keyboard=True),
        InlineKeyboardButton(text=f'\U0001F44E {dislike}', callback_data='dislike_photo', one_time_keyboard=True)
    )
    return inline_keyboard

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    if not db_users.get_user(message.from_user.id):
        db_users.add_user(telegram_id=message.from_user.id, min_count=db_images.get_min_count()[0][0])
        await message.answer(text=f'<b>Привет, {message.from_user.username}, пиши /show и смотри мемы</b>')
    else:
        await message.answer(text='Вы уже есть в базе данных')

@dp.message_handler(commands='show')
async def cmd_show(message: types.Message):
    sub = await bot.get_chat_member(chat_id='@memabotchannel', user_id=message.from_user.id)
    if sub['status'] != 'left':
        try:
            image_count = db_users.get_user_count(message.from_user.id)[0][0]
            image = types.InputFile(path_or_bytesio=db_images.get_path(image_count)[0][0])
            await message.answer_photo(photo=image, reply_markup=keyboard(db_images.get_likes(image_count)[0][0], db_images.get_dislikes(image_count)[0][0]))
            db_users.update_user_count(message.from_user.id)
        except IndexError:
            await message.answer(text='<b>Упс... кажется мемы закончились.</b>\n\n'
                                      'Напиши /show через некоторое время.\n'
                                      'Может к тому времен они появятся.')
    else:
        await message.answer(text='Подпишись на этот телеграмм канал\n\nt.me/memabotchannel')

@dp.callback_query_handler(text='like_photo')
async def cmd_like_photo(call: types.CallbackQuery):
    sub = await bot.get_chat_member(chat_id='@memabotchannel', user_id=call.message.chat.id)
    if sub['status'] != 'left':
        try:
            await call.message.edit_reply_markup(reply_markup=types.InlineKeyboardMarkup())
            image_count = db_users.get_user_count(call.message.chat.id)[0][0]
            db_images.update_likes(image_count - 1)
            image = types.InputFile(path_or_bytesio=db_images.get_path(image_count)[0][0])
            await call.message.answer_photo(photo=image, reply_markup=keyboard(db_images.get_likes(image_count)[0][0], db_images.get_dislikes(image_count)[0][0]))
            db_users.update_user_count(call.message.chat.id)
        except IndexError:
            await call.message.answer(text='<b>Упс... кажется мемы закончились.</b>\n\n'
                                            'Напиши /show через некоторое время.\n'
                                            'Может к тому времен они появятся.')
    else:
        await call.message.answer(text='Подпишись на этот телеграмм канал\n\nt.me/memabotchannel')

@dp.callback_query_handler(text='dislike_photo')
async def cmd_like_photo(call: types.CallbackQuery):
    sub = await bot.get_chat_member(chat_id='@memabotchannel', user_id=call.message.chat.id)
    if sub['status'] != 'left':
        try:
            await call.message.edit_reply_markup(reply_markup=types.InlineKeyboardMarkup())
            image_count = db_users.get_user_count(call.message.chat.id)[0][0]
            db_images.update_dislikes(image_count - 1)
            image = types.InputFile(path_or_bytesio=db_images.get_path(image_count)[0][0])
            await call.message.answer_photo(photo=image, reply_markup=keyboard(db_images.get_likes(image_count)[0][0], db_images.get_dislikes(image_count)[0][0]))
            db_users.update_user_count(call.message.chat.id)
        except IndexError:
            await call.message.answer(text='<b>Упс... кажется мемы закончились.</b>\n\n'
                                            'Напиши /show через некоторое время.\n'
                                            'Может к тому времен они появятся.')
    else:
        await call.message.answer(text='Подпишись на этот телеграмм канал\n\nt.me/memabotchannel')

async def on_startup(dp):
    await bot.set_webhook(url=WEBHOOK_URL)

async def on_shutdown(dp):
    await bot.delete_webhook()

def main_memabot():
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )
