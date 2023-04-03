# Назначение
Скачивание видео с YouTube и пересылка этого видео в Telegram-чат.

## Инициализация
Установите библиотеки `pytube` `telebot`.
```pip3 install pytube telebot```

В файле `telebot_youtube.py` в значении `TOKEN` подставьте свой токен (после импортов).

Запустите бота командой:
```python3 ./telebot_youtube.py```

В Windows:
```py ./telebot_youtube.py```

### Использование
Пришлите боту сообщение в формате `[ссылка] & [разрешение]`
Например, `https://www.youtube.com/watch?v=fKN6P6xzbPc & 720p`

#### Технологии
С помощью библиотеки `pytube`, программа скачивает видео в директорию `temp-telegram-youtube`, после чего, с помощью модуля `telebot`, она отправляет это видео пользователю.

##### Автор
Единственный автор -> @aloyen07