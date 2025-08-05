# Лог-парсер с отчётами

Простой скрипт для анализа логов в формате JSON. 
Позволяет считать среднее время ответа по эндпоинтам с фильтрацией по дате.

## Установка

1. Клонируйте репозиторий.
2. Создайте и активируйте виртуальное окружение (рекомендуется):
   
   python -m venv venv

4. Установите зависимости
   
  pip install -r requirements.txt


## Использование

python workmate_test2.py --file path/to/log1.log path/to/log2.log --report average --date YYYY-MM-DD
python workmate_test2.py --file logs.log --report average
python workmate_test2.py --file logs1.log logs2.log --report average --date 2025-06-25

--file — один или несколько файлов с логами в формате JSON (по одной записи на строку)
--report — тип отчёта
--date — (необязательно) фильтр по дате

## Тесты

pytest test.py -v 
