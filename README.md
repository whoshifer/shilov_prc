Дипломный проект на тему : Разработка чат-бота о ПРК


Данный бот умеет:
- парсить обсуждения ВК группы, скачивать файл и оповещать об этом пользователей бота
- парсить ВК группу на наличие новых записей и присылать их в телеграм бота,в том числе фотографии с поста
- парсить скачанный файл с расписанием формата XLSX и отправлять расписание на неделю в виде картинок по выбранной группе
- выслать ссылку для заказа справки из учебной части
- выслать полезные материалы для ВКР, Реферата, а так же графики учебного процесса, все в формате PDF для удобного открытия на любом устройстве
- выслать график консультаций у преподавателей в виде фотографии


Возможные будущие обновления:
- автоматическое оповещение о погоде в 07:00 по ЕКБ
- расписание для преподавателей
- свободные кабинеты для проведения пар для преподавателей
- полезные материалы для абитуриентов
- полезные материалы для родителей


Для запуска бота на своем пк необходимо:
- Python 3.10.X
- установить все необходимые библиотеки из файла requirements.txt (pip install -r requirements.txt)
- в файле config.py ввести свои API-KEY от ВК и Телеграм бота, а так же айди группы ВК и айди обсуждения ВК

Рекомендуемый запуск бота из виртуального окружения:

для Windows - .\venv\Scripts\Activate.ps1

для Linux/MacOs - source /venv/Scripts/activate

После чего уже можно скачивать необходимые библиотеки

Для выхода из виртуального окружения - deactivate


