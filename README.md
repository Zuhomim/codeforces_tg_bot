# Telegram_Bot для вывода набора задач с ресурса codeforces

## Используемый framework: Docker, Django, Redis, PostgreSQL.

# Инструкция по установке и запуску

## PostgreSQL
https://www.postgresql.org/download/

## Redis
https://redis.io/download/

### 1. Fork репозитория 
#### https://github.com/Zuhomim/codeforces_tg_bot
### 2. Установка зависимостей из файла requirements
```pip install -r requirements.txt```
### 3. Создайте файл .env в корневой директории (согласно шаблону .env.template)
### 4. Установите redis:
#### https://redis.io/docs/install/install-redis/
### 5. Перейдите в telegram - [BotFather](https://t.me/BotFather)
### 6. Создайте бота командой /newbot и следуйте указаниям
### 7. Скопируйте TOKEN в файл .env в переменную TELEGRAM_TOKEN

## Запуск:
### 1. Выполняем команду в терминале (redis должен быть запущен)
```python manage.py runserver```
### 2. Запускаем celery для периодических задач
```celery -A my_project worker —loglevel=info```
```celery -A my_project beat —loglevel=info```
### . Запускаем telegram_bot
```python manage.py bot```