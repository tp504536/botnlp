import logging
import subprocess
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from model import predict_class, get_response, date
from test import pog
from sql import Database

import re
import wikipedia as wk

wk.set_lang('ru')
storage = MemoryStorage()
bot = Bot(token="5210706425:AAE5W2FfcU0joDGd0I7IO-0NmF5YOaNh-_M")

db = Database('db_file')

dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)


class FSMmain(StatesGroup):
    get_main = State()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('хахахаха ' + message.from_user.first_name)


@dp.message_handler(content_types=['text', 'photo'])
async def message(message: types.Message):
    if message.text:
        ints = predict_class(message.text)
        if float(ints[0]['probability']) < 0.90:
            print('я тебя не понял')
            await message.answer('К сожеления я еще не все выучил')
        else:
            res = get_response(ints, date)
            print(res)
            print(ints[0]['intent'])
            await message.answer(str(res))
            b = message.text.lower()
            if re.search(r'валера', b):
                print(re.search(r'валера', b))
                a = b.split('валера', 1)[1]
                try:
                    await message.answer(wk.summary(a, sentences=1))
                except:
                    await message.answer('К сожаления не чего не нашлось😞 Напиши например пиво, биткойн, виски')
            elif re.search(r'погода', b):
                g = b.split('погода', 1)[1]
                print(type(g))
                await message.answer(pog(g))
            elif ints[0]['intent'] == 'reminder':
                await FSMmain.get_main.set()
            elif ints[0]['intent'] == 'notes':
                notes = types.InlineKeyboardMarkup(row_width=1)
                read = types.InlineKeyboardButton('Прочитать все ', callback_data='read')
                delet = types.InlineKeyboardButton('Удалить все', callback_data='delet')
                notes.add(read).add(delet)
                count = db.count(message.from_user.id)
                print(message.from_user.id)
                await message.answer('У тебя ' + str(count),reply_markup=notes)

            # try:
            #     await message.answer(wk.summary(a, sentences=1))
            # except:
            #     await message.answer('К сожаления не чего не нашлось😞 Напиши например пиво, биткойн, виски')

    else:
        await message.answer('Зачем ты мне это прислал')

@dp.message_handler(content_types='text', state=FSMmain.get_main)
async def final(message: types.Message, state: FSMContext):
    global data
    async with state.proxy() as data:
        data['text'] = message.text
        await state.finish()
        no_key = types.InlineKeyboardMarkup(row_width=1)
        n = types.InlineKeyboardButton('Отменить', callback_data='not')
        s = types.InlineKeyboardButton('Сохранить', callback_data='yes')
        no_key.add(n).add(s)
        await message.answer("Информацию для сохранения\n\n " + str(data['text']) + "\n\nВы уверены?",
                             reply_markup=no_key)
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
@dp.callback_query_handler(text='not')
async def no(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer('Я рад что не запишу этот бред')



@dp.callback_query_handler(text='yes')
async def yes(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    db.add_user(call.from_user.id, data['text'])
    await call.message.answer('Я успешно сохранил вашу мысль ')

@dp.callback_query_handler(text='read')
async def no(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    read = db.read(call.from_user.id)
    for i in read:
        msg = str(i)
        msg.replace(')',' ').replace('(',' ')
        await call.message.answer(msg)

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
