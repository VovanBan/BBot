from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.executor import start_webhook
from BusinessBot.database.databaseimages import DatabaseImages
from BusinessBot.database.databaseusers import DatabaseUsers
import os

TOKEN = '5513862581:AAHl3vNM44QbJITmWIv3vZ7t9Se5XjkfCzE'
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot)

WEBHOOK_HOST = 'https://businessbot1.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT', default=5000))

db_images = DatabaseImages()
db_users = DatabaseUsers()
list_of_admins = ['1136649586']

keyboard = InlineKeyboardMarkup(row_width=2).row(
    InlineKeyboardButton(text='Добавить', callback_data='yes_photo', one_time_keyboard=True),
    InlineKeyboardButton(text='Откланить', callback_data='no_photo', one_time_keyboard=True)
)

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.answer(text=f'<b>Привет, {message.from_user.username}, присылай сюда свои мемы, чтобы добавить их в MemaBot</b>')

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def cmd_post_photo(message: types.Message):
    sub = await bot.get_chat_member(chat_id='@memabotchannel', user_id=message.from_user.id)
    if sub['status'] != 'left':
        await message.answer(text='Фото отправлено на праверку\nОжидайте...')
        await bot.send_photo(chat_id=1136649586, photo=message.photo[0].file_id, reply_markup=keyboard)
    else:
        await message.answer(text='Подпишись на этот телеграмм канал\n\nt.me/memabotchannel')

@dp.callback_query_handler(text='no_photo', chat_id=list_of_admins)
async def cms_no_photo(call: types.CallbackQuery):
    await call.message.delete()

@dp.callback_query_handler(text='yes_photo', chat_id=list_of_admins)
async def cmd_yes_photo(call: types.CallbackQuery):
    await call.message.photo[-1].download(f'BusinessBot/images/{call.message.photo[-1].file_unique_id}.png')
    db_images.add_photo(f'BusinessBot/images/{call.message.photo[-1].file_unique_id}.png')
    await call.message.delete()

# Images DB

@dp.message_handler(commands='show_images', chat_id=list_of_admins)
async def cmd_delete(message: types.Message):
    await message.answer(text=str(db_images.get_db()))

@dp.message_handler(commands='delete_image', chat_id=list_of_admins)
async def cmd_delete(message: types.Message):
    os.remove(db_images.get_path(message.get_args())[0][0])
    db_images.delete_photo(message.get_args())

# Users DB

@dp.message_handler(commands='show_users', chat_id=list_of_admins)
async def cmd_delete(message: types.Message):
    await message.answer(text=str(db_users.get_db()))

@dp.message_handler(commands='delete_user', chat_id=list_of_admins)
async def cmd_delete(message: types.Message):
    db_users.delete_user(message.get_args())

@dp.message_handler(commands='add_admin', chat_id=list_of_admins)
async def cmd_delete(message: types.Message):
    db_users.add_admin()

# Old Images

@dp.message_handler(commands='update_old_images')
async def cmd_images_update(message: types.Message):
    db_images.update_photo_count()
    images_path = db_images.get_path_old_images()
    db_images.delete_old_images()
    if images_path is not []:
        for image_path in images_path:
            os.remove(image_path[0])

async def on_startup():
    await bot.set_webhook(url=WEBHOOK_URL)

async def on_shutdown():
    await bot.delete_webhook()

def main_memabotedit():
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )
