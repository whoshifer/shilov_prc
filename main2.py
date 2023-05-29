import vk_api
import config
import logging

import aiohttp
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor
from aiogram.types import CallbackQuery
from aiogram.types import InputMediaPhoto

import os
import pandas as pd
import textwrap
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from courses import courses

course1 = [
  types.InlineKeyboardButton(text=group, callback_data=group)
  for group in courses["1 курс"]
]
course2 = [
  types.InlineKeyboardButton(text=group, callback_data=group)
  for group in courses["2 курс"]
]
course3 = [
  types.InlineKeyboardButton(text=group, callback_data=group)
  for group in courses["3 курс"]
]
course4 = [
  types.InlineKeyboardButton(text=group, callback_data=group)
  for group in courses["4 курс"]
]

TGTOKEN = config.settings["TGTOKEN"]
VKTOKEN = config.settings["VKTOKEN"]

# Инициализация ВК-апи
vk_session = vk_api.VkApi(token=VKTOKEN)
vk = vk_session.get_api()
group_id = config.settings["GROUP_ID"]
topic_id = config.settings["TOPIC_ID"]

# Инициализация Телеграм бота
bot = Bot(token=TGTOKEN)
dp = Dispatcher(bot)

users = []
autoposting_statuses = {}
feedback_enabled = False

# создаем объект логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# создаем объект для записи логов в файл
handler = logging.FileHandler('log.txt', encoding='utf-8')
handler.setLevel(logging.INFO)
# создаем объект форматирования логов
formatter = logging.Formatter(
  '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# добавляем объект для записи логов в логгер
logger.addHandler(handler)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
  user_id = message.from_user.id
  users.append(user_id)
  autoposting_statuses[user_id] = False
  start_buttons = ["Начать"]
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  markup.add(*start_buttons)
  logger.info(
    f"Пользователь {message.from_user.username} (id={user_id}) запустил бота.")
  await message.reply('Здравствуйте, Вас приветствует чат-бот ПРК.',
                      reply_markup=markup)


@dp.message_handler(commands=['feedback'])
async def handle_feedback_command(message: types.Message):
  global feedback_enabled
  if not feedback_enabled:
    feedback_enabled = True
    await message.reply('Введите вашу обратную связь:')
  else:
    await message.reply('Обратная связь уже включена. Введите ваше сообщение.')


@dp.message_handler(filters.Regexp('^Начать'))
async def student_command(message: types.Message):
  stud_buttons = [
    "Заказать справку", "Расписание", "График консультаций", "Помощь",
    "Автопостинг из группы ВК", "Графики уч.процесса",
    "Полезные материалы для ВКР", "Полезные материалы для реферата"
  ]
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  markup.add(*stud_buttons)
  await message.reply(
    'Выберите то, что вам необходимо. \nДля ознакомления с командами, нажмите кнопку Помощь.',
    reply_markup=markup)


@dp.message_handler(filters.Regexp('^Заказать справку'))
async def docs_command(message: types.Message):
  docs_text = "https://forms.office.com/Pages/ResponsePage.aspx?id=GkRvy7iA_ky0GECEIL4hdYn2GbOUROZJn7z-vE97vYJUOFA3R1JLOFQxS1RERk1EUzAwMlkyUFNXUCQlQCN0PWcu&embed=true"
  await bot.send_message(message.chat.id, docs_text)


@dp.message_handler(filters.Regexp('^График консультаций'))
async def consultation(message: types.Message):
  with open('/home/runner/prc-news/prc_news/res/graphic.jpg', 'rb') as photo:
    await bot.send_photo(message.chat.id, photo)


@dp.message_handler(filters.Regexp('^Графики уч.процесса'))
async def learn_process(message: types.Message):
  files = [
    '/home/runner/prc-news/prc_news/res/Уч. Процесс/Уч. процесс (очное).pdf',
    '/home/runner/prc-news/prc_news/res/Уч. Процесс/Уч.процесс (очно-заочное).pdf',
    '/home/runner/prc-news/prc_news/res/Уч. Процесс/Уч.процесс (заочное).pdf'
  ]  # список файлов

  media = [types.InputMediaDocument(types.InputFile(file))
           for file in files]  # создать список медиафайлов

  await bot.send_media_group(message.chat.id,
                             media=media)  # отправить группу файлов


@dp.message_handler(filters.Regexp('^Полезные материалы для ВКР'))
async def vkr(message: types.Message):
  files = [
    '/home/runner/prc-news/prc_news/res/ВКР/Методические указания по ВКР.pdf',
    '/home/runner/prc-news/prc_news/res/ВКР/Нормоконтроль 2023.pdf',
    '/home/runner/prc-news/prc_news/res/ВКР/Требования к презентации ВКР.pdf',
    '/home/runner/prc-news/prc_news/res/ВКР/Рамка для дипломного проекта.pdf',
    '/home/runner/prc-news/prc_news/res/ВКР/Рамка для дипломной работы.pdf'
  ]
  media = [types.InputMediaDocument(types.InputFile(file)) for file in files]

  await bot.send_media_group(message.chat.id,
                             media=media)  # отправить группу файлов


@dp.message_handler(filters.Regexp('^Полезные материалы для реферата'))
async def referat(message: types.Message):
  files = [
    '/home/runner/prc-news/prc_news/res/Реферат/Методические рекомендации по выполнению реферативных работ.pdf',
    '/home/runner/prc-news/prc_news/res/Реферат/Нормоконтроль. Новый Реферат.pdf',
    '/home/runner/prc-news/prc_news/res/Реферат/Пример оформления реферата. Новый.pdf'
  ]
  media = [types.InputMediaDocument(types.InputFile(file)) for file in files]

  await bot.send_media_group(message.chat.id,
                             media=media)  # отправить группу файлов


@dp.message_handler(filters.Regexp('^Помощь'))
async def help_command(message: types.Message):
  help_text = (
    f"🤖 КОМАНДЫ ДЛЯ ЧАТ-БОТА: 🤖\n\n"
    f"❗ Заказать справку ❗\n"
    f"-- отправит ссылку для заказа справки из учебной части.\n\n"
    f"❗ Расписание ❗\n"
    f"-- вышлет расписание на всю неделю, по вашей группе. \n\n"
    f"❗ График консультаций ❗\n"
    f"-- вышлет фото графика консультаций преподавателей на 2022-23 год. \n\n "
    f"❗ Автопостинг из группы ВК ❗\n"
    f"-- Включит или выключит авто-отправку новостей из группы ПРК во Вконтакте. \n\n"
    f"❗ Графики уч.процесса ❗\n"
    f"-- вышлет 3 файла в формате PDF для очного, очно-заочного и заочного отделений на 2022-23 год. \n\n "
    f"❗ Полезные материалы для ВКР ❗\n"
    f"-- вышлет полезные файлы в формате PDF для правильного оформления выпускной квалификационной работы. \n\n "
    f"❗ Полезные материалы для реферата ❗\n"
    f"-- вышлет полезные файлы в формате PDF для правильного оформления реферата. \n\n "
  )

  await bot.send_message(message.chat.id, help_text)


@dp.message_handler(filters.Regexp('^Расписание'))
async def shedule(message: types.Message):
  keyboard = types.InlineKeyboardMarkup(row_width=2)
  keyboard.add(types.InlineKeyboardButton(text="1 курс", callback_data="1"),
               types.InlineKeyboardButton(text="2 курс", callback_data="2"),
               types.InlineKeyboardButton(text="3 курс", callback_data="3"),
               types.InlineKeyboardButton(text="4 курс", callback_data="4"))
  await message.reply("Выберите ваш курс:", reply_markup=keyboard)


@dp.callback_query_handler(
  lambda callback_query: callback_query.data in ['1', '2', '3', '4'])
async def course(callback_query: types.CallbackQuery):
  course_num = int(callback_query.data)
  keyboard = types.InlineKeyboardMarkup(row_width=3)
  keyboard.add(*globals()[f'course{course_num}'])
  keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="back"))
  await bot.edit_message_reply_markup(callback_query.message.chat.id,
                                      callback_query.message.message_id,
                                      reply_markup=keyboard)


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'back'
                           )
async def back(callback_query: types.CallbackQuery):
  keyboard = types.InlineKeyboardMarkup(row_width=2)
  keyboard.add(types.InlineKeyboardButton(text="1 курс", callback_data="1"),
               types.InlineKeyboardButton(text="2 курс", callback_data="2"),
               types.InlineKeyboardButton(text="3 курс", callback_data="3"),
               types.InlineKeyboardButton(text="4 курс", callback_data="4"))
  await bot.edit_message_reply_markup(callback_query.message.chat.id,
                                      callback_query.message.message_id,
                                      reply_markup=keyboard)


@dp.callback_query_handler(lambda callback_query: True)
async def group_name_input(callback_query: CallbackQuery):
  df = pd.read_excel('files/file.xlsx', header=None)
  group_name = callback_query.data
  group_column = df.loc[6].eq(group_name).idxmax()

  data = [[], [], [], [], [], []]

  for day, rows in enumerate([(9, 26), (27, 44), (45, 62), (63, 80), (81, 98),
                              (99, 116)]):
    for row in range(rows[0], rows[1] + 1):
      dataday = str(df.loc[row, 0])
      time = str(df.loc[row, 2])
      classroom = str(df.loc[row, group_column + 1])
      subject = str(df.loc[row, group_column])
      if isinstance(subject, float):
        subject = ''

      wrapped_subject = textwrap.fill(subject, width=25).split('\n')

      data[day].append([
        time[:11] if not pd.isnull(time) else '',
        wrapped_subject[0][:25] if wrapped_subject else '',
        classroom[:10] if not pd.isnull(classroom) else ''
      ])
      for line in wrapped_subject[1:]:
        data[day].append(['', line[:25], ''])

  days_of_week = [
    'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'
  ]
  dfs = []
  for table_data in data:
    df_day = pd.DataFrame(table_data,
                          columns=['Время', 'Дисциплина',
                                   'Кабинет']).replace(pd.NA,
                                                       '').replace('nan', '')
    dfs.append(df_day.dropna(how='all'))

  photos = []

  for day, df_day in enumerate(dfs):
    img = Image.new('RGB', (800, 1400), color='white')
    d = ImageDraw.Draw(img)
    d.rectangle([(0, 120), (800, 200)], fill=(106, 147, 176))

    font = ImageFont.truetype('arial.ttf', size=30)

    rows = [(9, 26), (27, 44), (45, 62), (63, 80), (81, 98), (99, 116)][day]
    dataday = str(df.loc[rows[0], 0])

    d.text((300, 10), 'Расписание на:', font=font, fill=(0, 0, 0))
    d.text((275, 50), dataday, font=font, fill=(0, 0, 0))

    start_y = 200
    row_height = 40
    d.text((10, start_y - 80), 'Время', font=font, fill=(0, 0, 0))
    d.text((250, start_y - 80), 'Дисциплина', font=font, fill=(0, 0, 0))
    d.text((650, start_y - 80), 'Кабинет', font=font, fill=(0, 0, 0))

    d.line([(240, start_y - 80), (240, start_y + len(df_day) * row_height)],
           fill=(0, 0, 0),
           width=2)
    d.line([(640, start_y - 80), (640, start_y + len(df_day) * row_height)],
           fill=(0, 0, 0),
           width=2)

    for i, row in df_day.iterrows():
      if row[0] != '':
        d.line([(0, start_y + i * row_height),
                (800, start_y + i * row_height)],
               fill=(0, 0, 0),
               width=2)

      d.line([(0, start_y - 80), (800, start_y - 80)], fill=(0, 0, 0),
             width=2)  # над таблицей
      d.line([(0, start_y + len(df_day) * row_height),
              (800, start_y + len(df_day) * row_height)],
             fill=(0, 0, 0),
             width=2)  # под таблицей

      d.text((10, start_y + i * row_height),
             str(row[0]),
             font=font,
             fill=(0, 0, 0))
      d.text((250, start_y + i * row_height),
             str(row[1]),
             font=font,
             fill=(0, 0, 0))
      d.text((650, start_y + i * row_height),
             str(row[2]),
             font=font,
             fill=(0, 0, 0))

    buf = BytesIO()
    img.save(buf, format='jpeg')
    buf.seek(0)

    photos.append(types.InputMediaPhoto(buf, caption=days_of_week[day]))

  await bot.send_message(chat_id=callback_query.message.chat.id,
                         text=f"Расписание для группы {group_name}:",
                         reply_to_message_id=callback_query.message.message_id)
  await bot.send_media_group(chat_id=callback_query.message.chat.id,
                             media=photos)


@dp.message_handler(filters.Regexp('^Автопостинг из группы ВК'))
async def autopost(message: types.Message):
  user_id = message.from_user.id
  if autoposting_statuses.get(user_id, True):
    autoposting_statuses[user_id] = False
    await message.reply("Автопостинг выключен.")
  else:
    autoposting_statuses[user_id] = True
    await message.reply("Автопостинг включен.")


last_news_id = None
last_file_id = None

@dp.message_handler()
async def handle_feedback_message(message: types.Message):
    global feedback_enabled
    if feedback_enabled:
        logger.info(f'Пользователь {message.from_user.username} (id={message.from_user.id}) оставил обратную связь : "{message.text}"')
        feedback_enabled = False
        await message.reply('Спасибо за вашу обратную связь!')

#parser news in group
async def check_new():
    global last_news_id

    while True:
        new_post = vk.wall.get(owner_id=-217559086, count=1)  # Получаем только одну новость

        post_id = new_post['items'][0]['id']
        if post_id == last_news_id:
            await asyncio.sleep(10)
            continue

        last_news_id = post_id
        post_text = new_post['items'][0]['text']
        post_link = f"https://vk.com/perm_college_radio?w=wall-{new_post['items'][0]['owner_id']}_{last_news_id}"
        # post_short_link = vk_session.method('utils.getShortLink', {'url': post_link})['short_url'] 

        media_group = []
        photo_urls = []
        attachments = new_post['items'][0].get('attachments', [])
        for attachment in attachments:
            if attachment['type'] == 'photo':
                photo_url = attachment['photo']['sizes'][-1]['url']
                photo_urls.append(photo_url)
                media_group.append(InputMediaPhoto(photo_url))

        message = f"Новый пост в группе ВК!\n\n{post_text}\n\n{post_link}"
        # Отправляем фотографии и текст в одном сообщении
        for user_id in users:
            if autoposting_statuses.get(user_id, True):
                if len(media_group) > 0:
                    if len(media_group) > 1:
                        await bot.send_media_group(chat_id=user_id, media=media_group)
                    else:
                        await bot.send_photo(chat_id=user_id, photo=media_group[0].media)
                await bot.send_message(chat_id=user_id, text=message)
        await asyncio.sleep(10) 

#parser tables

async def download_file(url, file_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            file_data = await response.read()
            with open(file_path, "wb") as f:
                f.write(file_data)

async def vk_parse():
    global last_file_id

    vk_session = vk_api.VkApi(token=VKTOKEN)
    vk = vk_session.get_api()
    last_comment_id = 0
    if not os.path.exists("files"):
        os.makedirs("files")
    while True:
        response = vk.board.getComments(group_id=group_id, topic_id=topic_id, count=100)
        new_comments = [comment for comment in response["items"] if comment["id"] > last_comment_id]
        if new_comments:
            last_comment = max(new_comments, key=lambda c: c["id"])
            last_comment_id = last_comment["id"]
            if "attachments" in last_comment:
                attachments = last_comment["attachments"]
                doc_attachments = [a for a in attachments if a["type"] == "doc" and a["doc"]["ext"] == "xlsx"]
                if doc_attachments:
                    file_id = doc_attachments[0]["doc"]["id"]
                    if file_id == last_file_id:
                        await asyncio.sleep(10)
                        continue

                    last_file_id = file_id
                    url = doc_attachments[0]["doc"]["url"]
                    title = "file.xlsx"
                    file_path = os.path.join("files", title)
                    await download_file(url, file_path)
                    message = f"Файл с расписанием обновлен, можете проверить свое расписание!"
                    for user in users:
                        await bot.send_message(chat_id=user, text=message)
                else:
                    print("Last comment without attachments.")
            else:
                print("Last comment without attachments.")
        else:
            print("No new comments.")
        await asyncio.sleep(10)

async def main():
    while True:
        try:
            await asyncio.gather(check_new(), vk_parse())
        except Exception as e:
            print(f"An error occurred: {e}")
            await asyncio.sleep(10)

if __name__ == '__main__':
  asyncio.get_event_loop().create_task(check_new())
  asyncio.get_event_loop().create_task(main())
  executor.start_polling(dp, skip_updates=True)
