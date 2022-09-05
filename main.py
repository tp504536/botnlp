import logging
import subprocess
import datetime
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


class FSMdata_time(StatesGroup):
    data_time_main = State()


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('хахахаха ' + message.from_user.first_name)


@dp.message_handler(commands='help')
async def help(message: types.Message):
    await message.answer(
        'Я бот Валера!\nМогу пообщаться с тобой,подсказать дату и время.\n'
        'Найти что нибудь в википедии "Валера и вопрос".\n'
        'Сделать напоминание напиши "запомни или запиши и тд"')


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
                delet = types.InlineKeyboardButton('Удалить', callback_data='delet')
                notes.add(delet)
                count = db.message(message.from_user.id)
                count = str(count).replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('\'', '')
                await message.answer('Твои заметки\n\n' + count, reply_markup=notes)
            elif ints[0]['intent'] == 'time':
                await message.answer(str(datetime.datetime.today().strftime("%Y-%m-%d-%H:%M")))

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
    if not db.users(call.from_user.id):
        db.add_user(call.from_user.id, data['text'])
        await FSMdata_time.data_time_main.set()
        await call.message.answer('Дату когда напомнить. В формате 2022-06-29 17:08')
        await FSMdata_time.data_time_main.set()
    else:
        await call.message.answer('Я пока могу запоминать только 1 сообщение')
    # await call.message.answer('Я успешно сохранил вашу мысль ')


@dp.callback_query_handler(text='delet')
async def delet(call: types.CallbackQuery):
    db.delet(call.from_user.id)
    await call.message.answer('Запись удалена')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)


@dp.message_handler(content_types='text', state=FSMdata_time.data_time_main.state)
async def data(message: types.Message, state: FSMContext):
    global date_time_obj
    async with state.proxy() as data:
        data['text'] = message.text
        date_key = types.InlineKeyboardMarkup(row_width=1)
        date_n = types.InlineKeyboardButton('Отменить', callback_data='date_no')
        date_s = types.InlineKeyboardButton('Сохранить', callback_data='date_yes')
        date_key.add(date_s).add(date_n)
        try:
            date_time_obj = datetime.datetime.strptime(data['text'], '%Y-%m-%d %H:%M')
            await state.finish()
            await message.answer("Дата \n\n " + str(date_time_obj) + "\n\nВы уверены?", reply_markup=date_key)
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        except:
            await message.answer('Вы ввели не правильно дату. Попробуйте еще раз!!\n\nПример 2022-06-29 17:08')


@dp.callback_query_handler(text='date_no')
async def no_date(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    db.delet(call.from_user.id)
    await call.message.answer('Отлично,что этот бред не будет записан')


@dp.callback_query_handler(text='date_yes')
async def yes_date(call: types.CallbackQuery):
    db.add_date(date_time_obj, call.from_user.id)
    await call.message.answer('Установил напоминание')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    # await call.message.answer('Я успешно сохранил вашу мысль ')


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
