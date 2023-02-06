from aiogram import Bot, Dispatcher, types
import asyncio
from PyEasyQiwi import QiwiConnection
import time
from datetime import datetime,timedelta
import sqlite3
from db import select_key,select_day,first_time,create_user,select_referal,create_user_ref,delete_platej,create_platej,chek_platej,cupon_payment,create_referal
from clients_ru import id_key,create_one,data_limit

api_key = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjJ0dDUyaS0wMCIsInVzZXJfaWQiOiI3OTgxMDE3ODcwNiIsInNlY3JldCI6ImY0Mzc4MDBhZDdlM2E3ZGUwYTcxNmEwN2QyY2JlZGFlYzE3NzIwMmFhYTU5NjI1NGM3MjQwZWVjN2Y5MThiMjQifX0="
qiwi_pay = QiwiConnection(api_key)

con = sqlite3.connect("ru_vpn.db")
cur = con.cursor()

bot = Bot(token="6027205910:AAG-81FtRDPP3Kd6zALlWNw9Ksr_h6A-Fls")
dp = Dispatcher(bot)



@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    if first_time(message.from_user.id):
        if ' ' in message.text:
            flag ,tuple = select_referal(message.text.split()[1])
            if flag == True:
                create_user_ref(message.from_user.id,tuple[0],tuple[1],tuple[2],tuple[3])

        builder = types.InlineKeyboardMarkup()
        builder.add(types.InlineKeyboardButton(
            text="Да!",
            callback_data="try_yes")
        )
        builder.add(types.InlineKeyboardButton(
            text='Нет-хочу сразу купить тариф. 🇷🇺',
            callback_data='tariffs'))
        await message.answer(
            text="Здравствуйте!\nРад что Вы обратились ко мне. Вам доступен бесплатный тестовый доступ на 2 дня,\nхотите попробовать?",reply_markup=builder
        )
    else:
        builder = types.ReplyKeyboardMarkup(resize_keyboard=True)
        builder.row(types.KeyboardButton(
            text="Тарифы",
            callback_data="tariffs")
        )
        builder.insert(types.KeyboardButton(
            text="Мой ключ\n",
            callback_data="mytarif")
        )
        builder.row(types.KeyboardButton(
            text="Поддержка\n",
            callback_data="support")
        )
        builder.insert(types.KeyboardButton(
            text="FAQ\n",
            callback_data="FAQ")
        )
        builder.insert(types.KeyboardButton(
            text="Инструкция\n",
            callback_data="instruction")
        )
        await message.answer("Вы в главном меню", reply_markup=builder)


@dp.message_handler(text="Создать рефералку")
async def cmd_start(message: types.Message):
    if message.from_user.id == 1890767310 or message.from_user.id==3727766:
        await message.answer('Введи  в формате \nreferal_nickname/percent_referal/kolichestvo_platejei/user_percent')



@dp.callback_query_handler(text='try_yes')
async def cmd_start(callback: types.CallbackQuery):
    builder = types.InlineKeyboardMarkup(resize_keyboard=True)
    builder.row(types.InlineKeyboardMarkup(
        text="App Store",
        url='https://apps.apple.com/us/app/outline-app/id1356177741'
    ),types.InlineKeyboardButton(
        text="Play Market",
        url='https://play.google.com/store/apps/details?id=org.outline.android.client&hl=en&gl=US')
    )
    builder.add(types.KeyboardButton(
        text="Что дальше?",
        callback_data="what_next")
    )
    await callback.message.answer(text="Супер, мой ВПН работает внутри приложения 'Outline'\nВам нужно его скачать, вот ссылки :",reply_markup=builder)






@dp.callback_query_handler(text='what_next')
async def cmd_start(callback: types.CallbackQuery):
    if first_time(callback.from_user.id):
        day_from_start=(datetime.strptime(str(callback.message.date).split()[0],"%Y-%m-%d")+timedelta(days=2)).strftime("%Y-%m-%d")
        id, key = id_key(create_one())
        data_limit(id, 40000000000)
        create_user(callback.from_user.id, key, id, day_from_start)
        key=select_key(callback.from_user.id)
        builder = types.InlineKeyboardMarkup()
        builder.add(types.InlineKeyboardButton(
            text="Супер",
            callback_data="main_menu")
        )
        await callback.message.answer('Ваш пробный период активирован, осталось 48 часов\n'+ "`"+str(key)+"`",parse_mode='MarkdownV2')
        await asyncio.sleep(3)
        await callback.message.answer("Инструкция для подключения.\n1)Скопируйте этот ключ (можно клацнуть на него)\n2) Откройте приложение Outline\n3)Вам предложит вставить скопированный\nтекст из телеграма, соглашайтесь!\n4) Нажимайте 'Connect'\n5) Поздравляем, вы в интернете!",reply_markup=builder)




@dp.callback_query_handler(text='tariffs')
async def cmd_start(callback: types.CallbackQuery):
    if first_time(callback.from_user.id):
        day_from_start=(datetime.strptime(str(callback.message.date).split()[0],"%Y-%m-%d")+timedelta(days=2)).strftime("%Y-%m-%d")
        id, key = id_key(create_one())
        data_limit(id, 40000000000)
        create_user(callback.from_user.id, key, id, day_from_start)
        await callback.message.answer('Ваш пробный период активирован, осталось 48 часов\nКлюч можно получить в Главном меню / Мой ключ')
    builder = types.ReplyKeyboardMarkup(resize_keyboard=True)
    builder.row(types.InlineKeyboardButton(
        text="Месяц  - 149 рублей 🇷🇺",
        callback_data="first")
    )
    builder.insert(types.InlineKeyboardButton(
        text="3 Месяца - 349 рублей 🇷🇺",
        callback_data="second")
    )
    builder.row(types.InlineKeyboardButton(
        text="Целый год - 999 рублей 🇷🇺",
        callback_data="third")
    )
    builder.add(types.KeyboardButton(
        text="Главное меню",
        callback_data="what_next")
    )
    await callback.message.answer("Выбирайте любой удобный вариант:",reply_markup=builder)





@dp.message_handler(text='Тарифы')
async def cmd_start(message: types.Message):
    builder = types.ReplyKeyboardMarkup(resize_keyboard=True)
    builder.row(types.InlineKeyboardButton(
        text="Месяц  - 149 рублей 🇷🇺",
        callback_data="first")
    )
    builder.insert(types.InlineKeyboardButton(
        text="3 Месяца - 349 рублей 🇷🇺",
        callback_data="second")
    )
    builder.row(types.InlineKeyboardButton(
        text="Целый год - 999 рублей 🇷🇺",
        callback_data="third")
    )
    builder.add(types.KeyboardButton(
        text="Главное меню",
        callback_data="what_next")
    )
    await message.answer("Выбирайте любой удобный вариант:",reply_markup=builder)






@dp.message_handler(text='Мой ключ')
async def cmd_start(message: types.Message):
    if first_time(message.from_user.id):
        day_from_start=(datetime.strptime(str(message.date).split()[0],"%Y-%m-%d")+timedelta(days=2)).strftime("%Y-%m-%d")
        id, key = id_key(create_one())
        data_limit(id, 40000000000)
        create_user(message.from_user.id, key, id, day_from_start)
        await message.answer('Ваш пробный период активирован, осталось 48 часов\n')
    key = select_key(message.from_user.id)
    day = select_day(message.from_user.id)
    await message.answer("Ваш ключ:"+"`"+str(key)+"`"+'\nПодписка активна до  : '+day,parse_mode='MarkdownV2')




@dp.callback_query_handler(text='main_menu')
async def cmd_start(callback: types.CallbackQuery):
    builder = types.ReplyKeyboardMarkup(resize_keyboard=True)
    builder.row(types.KeyboardButton(
        text="Тарифы",
        callback_data="tariffs")
    )
    builder.insert(types.KeyboardButton(
        text="Мой ключ",
        callback_data="mytarif")
    )
    builder.row(types.KeyboardButton(
        text="Поддержка",
        callback_data="support")
    )
    builder.insert(types.KeyboardButton(
        text="FAQ",
        callback_data="FAQ")
    )
    builder.insert(types.KeyboardButton(
        text="Инструкция\n",
        callback_data="instruction")
    )
    if callback.from_user.id == 1890767310:
        builder.insert(types.KeyboardButton(text="Создать рефералку"))
    await callback.message.answer("Вы в главном меню", reply_markup=builder)






@dp.message_handler(text='Главное меню')
async def cmd_start(message: types.Message):
    builder = types.ReplyKeyboardMarkup(resize_keyboard=True)
    builder.row(types.KeyboardButton(
        text="Тарифы",
        callback_data="tariffs")
    )
    builder.insert(types.KeyboardButton(
        text="Мой ключ\n",
        callback_data="mytarif")
    )
    builder.row(types.KeyboardButton(
        text="Поддержка\n",
        callback_data="support")
    )
    builder.insert(types.KeyboardButton(
        text="FAQ\n",
        callback_data="FAQ")
    )
    builder.insert(types.KeyboardButton(
        text="Инструкция\n",
        callback_data="instruction")
    )
    if message.from_user.id == 1890767310:
        builder.insert(types.KeyboardButton(text="Создать рефералку"))
    await message.answer("Вы в главном меню", reply_markup=builder)






@dp.message_handler(text="Месяц  - 149 рублей 🇷🇺")
async def cmd_start(message: types.Message):
    uid=message.from_user.id
    if   chek_platej(uid):
        cupon=cupon_payment(message.from_user.id)
        value=round(149*0.98*(100-cupon)/100)
        pay_url, bill_id, response = qiwi_pay.create_bill(value=value, description=str(message.from_user.id),theme_code='Egor-ChYZVzq4Ixq')
        create_platej(uid,bill_id.split(':')[1],1)
        print('create_first',uid)
    else:
        qiwi_pay.remove_bill(delete_platej(uid))
        cupon = cupon_payment(message.from_user.id)
        value = round(149 * 0.98 * (100-cupon)/ 100)
        pay_url, bill_id, response = qiwi_pay.create_bill(value=value, description=str(message.from_user.id),theme_code='Egor-ChYZVzq4Ixq')
        create_platej(uid, bill_id.split(':')[1], 1)
        print('create_second',uid)
    builder = types.InlineKeyboardMarkup(resize_keyboard=True)
    builder.add(types.InlineKeyboardButton(
        text="Ссылка на оплату ",
        url=pay_url
    )
    )
    await message.answer('Оплатите с помощью qiwi\n\n',reply_markup=builder)
    builder = types.ReplyKeyboardMarkup(resize_keyboard=True)
    builder.insert(types.KeyboardButton(
        text="Мой ключ\n",
        callback_data="mytarif")
    )
    builder.add(types.KeyboardButton(
        text="Главное меню",
        callback_data="what_next")
    )
    await asyncio.sleep(3)
    await message.answer('Как только вы оплатите счёт, vpn автоматически продлится',reply_markup=builder)






@dp.message_handler(text="3 Месяца - 349 рублей 🇷🇺")
async def cmd_start(message: types.Message):
    uid = message.from_user.id
    if chek_platej(uid):
        cupon = cupon_payment(message.from_user.id)
        value = round(349 * 0.98 * (100-cupon)/ 100)
        pay_url, bill_id, response = qiwi_pay.create_bill(value=value, description=str(message.from_user.id),
                                                          theme_code='Egor-ChYZVzq4Ixq')
        create_platej(uid, bill_id.split(':')[1], 3)
        print('create_first',uid)
    else:
        qiwi_pay.remove_bill(delete_platej(uid))
        cupon = cupon_payment(message.from_user.id)
        value = round(349 * 0.98 * (100-cupon)/ 100)
        pay_url, bill_id, response = qiwi_pay.create_bill(value=value, description=str(message.from_user.id),
                                                          theme_code='Egor-ChYZVzq4Ixq')
        create_platej(uid, bill_id.split(':')[1], 3)
        print('create_second',uid)
    builder = types.InlineKeyboardMarkup(resize_keyboard=True)
    builder.add(types.InlineKeyboardButton(
        text="Ссылка на оплату ",
        url=pay_url
    )
    )
    await message.answer('Оплатите с помощью qiwi\n\n',reply_markup=builder)
    builder = types.ReplyKeyboardMarkup(resize_keyboard=True)
    builder.insert(types.KeyboardButton(
        text="Мой ключ\n",
        callback_data="mytarif")
    )
    builder.add(types.KeyboardButton(
        text="Главное меню",
        callback_data="what_next")
    )
    await asyncio.sleep(5)
    await message.answer('Как только вы оплатите счёт, vpn автоматически продлится', reply_markup=builder)






@dp.message_handler(text="Целый год - 999 рублей 🇷🇺")
async def cmd_start(message: types.Message):
    uid = message.from_user.id
    if chek_platej(uid):
        cupon = cupon_payment(message.from_user.id)
        value = round(999 * 0.98 * (100 - cupon) / 100)
        pay_url, bill_id, response = qiwi_pay.create_bill(value=value, description=str(message.from_user.id),
                                                          theme_code='Egor-ChYZVzq4Ixq')
        create_platej(uid, bill_id.split(':')[1], 12)
        print('create_first',uid)
    else:
        qiwi_pay.remove_bill(delete_platej(uid))
        cupon = cupon_payment(message.from_user.id)
        value = round(999 * 0.98 * (100 - cupon) / 100)
        pay_url, bill_id, response = qiwi_pay.create_bill(value=value, description=str(message.from_user.id),
                                                          theme_code='Egor-ChYZVzq4Ixq')
        create_platej(uid, bill_id.split(':')[1], 12)
        print('create_second',uid)
    builder = types.InlineKeyboardMarkup(resize_keyboard=True)
    builder.add(types.InlineKeyboardButton(
        text="Ссылка на оплату ",
        url=pay_url
    )
    )
    await message.answer('Оплатите с помощью qiwi\n\n',reply_markup=builder)
    builder = types.ReplyKeyboardMarkup(resize_keyboard=True)
    builder.insert(types.KeyboardButton(
        text="Мой ключ\n",
        callback_data="mytarif")
    )
    builder.add(types.KeyboardButton(
        text="Главное меню",
        callback_data="what_next")
    )
    await asyncio.sleep(5)
    await message.answer('Как только вы оплатите счёт, vpn автоматически продлится', reply_markup=builder)




@dp.message_handler(text='FAQ')
async def cmd_start(message: types.Message):
    await message.answer("""Что такое VPN и зачем оно мне?

VPN это виртуальная частная сеть которая, используя цифровой туннель, «переносит» вас в ту страну, где находится сервер VPN. В нашем случае это Россия. Нужно это бывает в случаях когда внутри вашей страны некоторые сайты не работают.


Получил ссылку. Дальше что?

Ссылка это и есть ваш персональный ключ, который подключает вас к нашему серверу  RU VPN. Если вы сделали всё по инструкции то включение и выключение RU VPN будет происходить через приложение Outline нажатием одной кнопки подключить / отключить.

Как проверить работает ли VPN?

Можете открыть сайт 2ip.ru и посмотреть в какой стране вас видит сайт. Должно быть написано Россия.

Если у вас остались вопросы пишите сюда: @gkorkots""")

@dp.message_handler(text='Поддержка')
async def cmd_start(message: types.Message):
    await message.answer("""Перед тем как задать вопрос, обязательно прочитайте подробную инструкцию и раздел FAQ.
Для ускорения решения технических вопросов, можете сразу прислать скриншот с открытым приложением Outline и сообщение от бота из раздела "Мой ключ".
Ваши вопросы и обращения направлять сюда @gkorkots """)

@dp.message_handler(text='Инструкция')
async def cmd_start(message: types.Message):
    await message.answer("""1. Скачайте и установите на устройство приложение Outline:

iOS: https://itunes.apple.com/app/outline-app/id1356177741
macOS: https://itunes.apple.com/app/outline-app/id1356178125
Windows: https://s3.amazonaws.com/outline-releases/client/windows/stable/Outline-Client.exe
Linux: https://s3.amazonaws.com/outline-releases/client/linux/stable/Outline-Client.AppImage
Android: https://play.google.com/store/apps/details?id=org.outline.android.client
Дополнительная ссылка для Android: https://s3.amazonaws.com/outline-releases/client/android/stable/Outline-Client.apk

2. Получите ключ доступа, который начинается с ss://, а затем скопируйте его.

3. Откройте клиент Outline. Если ваш ключ доступа определился автоматически, нажмите "Подключиться". Если этого не произошло, вставьте ключ в поле и нажмите "Подключиться".

Теперь у вас есть доступ к свободному интернету. Чтобы убедиться, что вы подключились к серверу, введите в Google Поиске фразу "Какой у меня IP-адрес". IP-адрес, указанный в Google, должен совпадать с IP-адресом в клиенте Outline.

Дополнительные сведения можно найти на странице https://getoutline.org/.""")




@dp.message_handler()
async def cmd_start(message: types.Message):
    if message.from_user.id==1890767310 or message.from_user.id==3727766:
        try:
            referal_nickname,percent_referal,kolichestvo_platejei,user_percent=map(str,message.text.split('/'))
            kolichestvo_platejei,user_percent,percent_referal=int(kolichestvo_platejei),int(user_percent),int(percent_referal)
            create_referal(referal_nickname,percent_referal,kolichestvo_platejei,user_percent)
            await message.answer(text='Всё круто')
        except:
            await message.answer(text='Ты где-то допустил ошибку или опечатку')
    elif message.from_user.id==5695880736:
        builder=types.InlineKeyboardMarkup()
        builder.add(types.InlineKeyboardButton(
            text='Продлить  пользование vpn',
            callback_data='tariffs'))
        await bot.send_message(chat_id=int(message.text),text='Остался один денёк vpn . Вы можете продлить пользование vpn',reply_markup=builder)
        await message.answer(f"done {message.text}")
    else:
        await message.answer("У нас удобный интерфейс , ты можешь все сделать с помощью кнопок )")







async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
