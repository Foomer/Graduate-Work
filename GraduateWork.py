import requests
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from decouple import config

API_TOKEN = config('API_TOKEN')
api_key = config('API_KEY')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('/stats'))
    await message.answer("Привет! Я бот, по Fortnite. Как я могу тебе помочь?", reply_markup=keyboard)
    


        
@dp.message_handler(commands=['stats'])
async def stats_command(message: types.Message):
    
    await message.answer("Привет! Для получения статистики Fortnite, напишите никнейм.")
    


@dp.message_handler()
async def userName(message: types.Message):
    
    username = message.text
    url = f"https://fortniteapi.io/v1/stats?username={username}"
    
    headers = {
        "Authorization": api_key
    }

    response = requests.get(url, headers=headers).json()
    
    if response.get('code') == 'PRIVATE_ACCOUNT':
        await message.answer('Ошибка: данный аккаунт является приватным')
        return
    
    print('Hello')
    
    try:
       if not response['result']:
            await message.answer(f"{response['error']}")
            print(response)
            return
    except KeyError:
        await message.answer('Ошибка при получении статистики')
        print(response)
        return
    
    
    
    answer = (f"Имя игрока: {response['name']}\n"
            f"Уровень: {response['account']['level']}\n"
            f"Сезонная статистика:\n")

    for season in response['accountLevelHistory']:
        answer += (f"  Season {season['season']}: "
                f"Уровень {season['level']}\n")

    answer += "\nГлобальная статистика:\n"

    for mode, stats in response['global_stats'].items():
        answer += (f"  {mode.title()} - "
                f"1 Место: {stats['placetop1']}, "
                f"K/D: {stats['kd']}, "
                f"Процент побед: {stats['winrate']}%\n")

    await message.answer(answer, disable_notification=True)
    return
        

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
