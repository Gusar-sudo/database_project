# Client Accounting App (Tkinter + SQLite)

Простое GUI-приложение на Python для учета клиентов.  

## Что умеет приложение

- Добавлять клиента через форму
- Сохранять данные в SQLite базу
- Показывать список всех клиентов в таблице
- Проверять, чтобы поля не были пустыми

Поля клиента:

- ФИО
- Телефон
- Группа

## Стек

- Python 3
- Tkinter (GUI)
- SQLite3 (встроенная база данных)

## Структура проекта

```text
database_project/
├─ app.py
├─ clients.db          # создается автоматически при запуске
```

## Архитектура (простая ООП)

В проекте есть 4 основных класса:

- `Client` — модель клиента (`dataclass`)
- `Database` — слой работы с БД (создание таблицы, insert, select)
- `ClientService` — бизнес-логика и простая валидация
- `ClientApp` — графический интерфейс на Tkinter

## Как запустить

1. Убедитесь, что установлен Python 3:

```bash
python --version
```

2. Перейдите в папку проекта:

```bash
cd "c:\Users\User\Desktop\код ide\cursor\database_project"
```

3. Запустите приложение:

```bash
python app.py
```

## Как пользоваться

1. Введите `ФИО`, `Телефон`, `Группа`
2. Нажмите кнопку **Добавить клиента**
3. Клиент появится в таблице ниже
4. Данные сохранятся в файл `clients.db`

## Схема таблицы БД

Таблица `clients`:

- `id` — INTEGER, PK, AUTOINCREMENT
- `full_name` — TEXT, NOT NULL
- `phone` — TEXT, NOT NULL
- `group_name` — TEXT, NOT NULL

## Проверка кода

Можно проверить синтаксис:

```bash
python -m py_compile app.py
```
