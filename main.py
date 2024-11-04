from pprint import pprint
import time
import threading
import asyncio
import tracemalloc

# Включаем трассировку распределения памяти
tracemalloc.start()

# Файлы проекта
import text as txt
import sheets

# Aiogram files
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

data = {
    "CAN_READ": True
}

async def appendFond(msg):
    print("APPENDINGS")
    while True:
        if data["CAN_READ"]:
            data["CAN_READ"] = False
            chat_id = msg.chat.id
            chat_title = msg.chat.title
            fond_ids = await sheets.readRange('Proj', 'C3:DZ3')
            print(fond_ids)
            if fond_ids != []:  # будем проверять наличие фондов
                if not ([str(chat_id)] in fond_ids):  # если конкретный фонд отсутствует, то вписываем его
                    await sheets.writeOne('Proj', 3, 3 + len(fond_ids), f'{chat_id}')  # id
                    await sheets.writeOne('Proj', 2, 3 + len(fond_ids), f'{chat_title}')  # title
            else:  # если фондов вообще нет, вписывааем в первую клетку
                await sheets.writeOne('Proj', 3, 3, f'{chat_id}')  # id
                await sheets.writeOne('Proj', 2, 3, f'{chat_title}')  # title
            data["CAN_READ"] = True
            await asyncio.sleep(1)
            return 0
        await asyncio.sleep(2)


TOKEN = '7477257753:AAFu5lvl0URd4e4ORfbKo2OyxcGEQbdrGfQ'
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["id"])
async def process_id_command(msg: types.Message):
    """On identification"""
    print("HEREE")
    await appendFond(msg)
    

@dp.message_handler(commands=["start"])
async def process_start(msg: types.Message):
    """On start"""
    await bot.send_message(766906778, 'Hi!')


# Асинхронная функция для проверки наличия новых элементов в массиве
async def check_for_updates(interval_seconds):
    # await bot.send_message(766906778, 'hi')
    print('HERE CHECK')
    try:
        while True:
            if data["CAN_READ"]:
                for i in range(4, 6):
                    for j in range(3, 10):
                        value = await sheets.readOne('Proj', i, j)
                        if value == [['1']]:
                            text = (await sheets.readOne('Proj', i, 2))[0][0] # считываем блюрб
                            chat_id = (await sheets.readOne('Proj', 3, j))[0][0] # считываем идентиикатор фонда для отправки блюрба
                            # await sheets.colorCell('Proj', i, j) # задаем цвет ячейке (желтый)
                            await bot.send_message(chat_id, text)
                            # await sheets.colorCell(1, 1, 1)
                            await sheets.writeOne('Proj', i, j, 'Отправлено ✉️')
                            await asyncio.sleep(interval_seconds)   
            await asyncio.sleep(interval_seconds)
    except Exception as e:
        print(e)
    # while True:
    #     print('reading..')
    #     await asyncio.sleep(interval_seconds)


# Создаем функцию для запуска check_new_items в фоновом режиме
async def run_check_for_updates(interval_seconds):
    await check_for_updates(interval_seconds)
    # print('tik')


# Основная асинхронная функция
async def main():   
    print('HERE MAIN')
    # Бот в фоновом режиме
    await dp.start_polling()


# Создаем асинхронную функцию для запуска обоих задач параллельно
async def parallel_main():
    await asyncio.gather(main(), run_check_for_updates(4))

# Запускаем программу, выполняя обе задачи параллельно
asyncio.run(parallel_main())






# # asyncio.run(main())






# # Функция для запуска бота
# async def run_bot():
#     if __name__ == '__main__':
#         # Запуск бота
#         executor.start_polling(dp, skip_updates=True)