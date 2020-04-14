# Weatherbot
Weatherbot for Yandex school for future CTO

Умный сервис прогноза погоды
Задача со звездочкой

Для создания проекта использовался Python3, управление базами данных осуществлялось с SQL. Использовались технологии API для VK, OpenWeatherAPI для получения данных о погоде, а также библиотека sqlite3 для работы с базами данных.

Сервис - чат-бот в социальной сети VK в роли FAQ, который по вводным данным о местоположении и управлению кнопками клавиатуры формирует ответ пользователю.

Формат ответа текстовой, сам ответ о погоде вставляется в шаблон "температура - ___ , давление - ____ , скорость ветра - ______", также, в зависимости от температуры выводятся рекомендации по подбору одежды на каждый день.

Видео-демонстрация - 

Python программа получает сообщение от пользователя, полученное через интерфейс мессенджера:
- проверяется сообщение на доступные обрабатываемые сценарии ответа
- при необходимости формируется и отправляется запрос в базу данных
- полученный ответ из базы данных обрабатывается и используется для формирования ответа пользователю
- ответ отправляется пользователю
