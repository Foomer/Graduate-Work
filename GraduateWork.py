import requests
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
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
    
    await message.reply("привет чтобы узнать  напишы свой никнейм игрока")
    

    

    

@dp.message_handler()
async def userName(message: types.Message):
    
    username = message.text
    url = f"https://fortniteapi.io/v1/stats?username={username}"
    
    headers = {
        "Authorization": api_key
    }

    response = requests.get(url, headers=headers).json()
    
    answer = (f"Player Name: {response['name']}\n"
            f"Account Level: {response['account']['level']}\n"
            f"Account Progress: {response['account']['progress_pct']}%\n"
            "Seasonal Stats:\n")

    for season in response['accountLevelHistory']:
        answer += (f"  Season {season['season']}: "
                f"Level {season['level']}, "
                f"Progress {season['process_pct']}%\n")

    answer += "\nGlobal Stats:\n"

    for mode, stats in response['global_stats'].items():
        answer += (f"  {mode.title()} - "
                f"Placetop1: {stats['placetop1']}, "
                f"K/D: {stats['kd']}, "
                f"Winrate: {stats['winrate']}%\n")

    await message.answer(answer)
        

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
