import logging
import subprocess
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from model import predict_class, get_response,date
from test import  pog
import re
import wikipedia as wk
wk.set_lang('ru')
storage = MemoryStorage()
bot = Bot(token="5210706425:AAE5W2FfcU0joDGd0I7IO-0NmF5YOaNh-_M")

dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('хахахаха ' + message.from_user.first_name)

@dp.message_handler(content_types=['text','photo'])
async def message(message: types.Message):
    if message.text:
        ints = predict_class(message.text)
        if float(ints[0]['probability']) < 0.90:
            print('я тебя не понял')
            await message.answer('К сожеления я еще не все выучил')
        else:
            res = get_response(ints, date)
            await message.answer(str(res))
            b = message.text.lower()
            print(message.text.lower())
            if re.search(r'валера',b):
                print(re.search(r'валера',b))
                a = b.split('валера',1)[1]
                try:
                    await message.answer(wk.summary(a, sentences=1))
                except:
                    await message.answer('К сожаления не чего не нашлось😞 Напиши например пиво, биткойн, виски')
            elif re.search(r'погода', b):
                g = b.split('погода',1)[1]
                print(type(g))
                await message.answer(pog(g))

                # try:
                #     await message.answer(wk.summary(a, sentences=1))
                # except:
                #     await message.answer('К сожаления не чего не нашлось😞 Напиши например пиво, биткойн, виски')

    else:
        await message.answer('Зачем ты мне это прислал')

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
