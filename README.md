# Expense Tracker API
Трекер расходов и доходов Expense Tracker API.

REST API для учета личных финансов с возможностью категоризации транзакций и аналитики расходов.

## Стек технологий

- **Python 3.12** - основной язык разработки;
- **aiohttp** - асинхронный веб-фреймворк;
- **asyncpg** - асинхронный драйвер PostgreSQL;
- **PostgreSQL 16** - реляционная база данных;
- **Pydantic** - валидация данных и сериализация;
- **Docker & Docker Compose** - контейнеризация и оркестрация;
- **pytest & pytest-asyncio** - тестирование.

## Архитектура

Проект построен по принципу разделения ответственности (Separation of Concerns):

- **Routes** - HTTP обработчики, принимают запросы и возвращают ответы;
- **Services** - бизнес-логика, валидация правил предметной области;
- **Repositories** - работа с базой данных, инкапсуляция SQL запросов;
- **Models** - Pydantic модели для валидации и сериализации данных.

Внедрение зависимостей (Dependency Injection) реализовано через состояние приложения `aiohttp` с использованием типизированных ключей `web.AppKey`.

## Структура проекта
```bash
expense-tracker/
├── app/
│ ├── models/ # Pydantic модели
│ │ ├── transaction.py
│ │ └── category.py
│ ├── repositories/ # Слои работы с БД
│ │ ├── transaction.py # Абстрактный интерфейс
│ │ ├── category.py # Абстрактный интерфейс
│ │ ├── fake_transaction.py
│ │ ├── fake_category.py
│ │ ├── asyncpg_transaction.py
│ │ ── asyncpg_category.py
│ ├── services/ # Бизнес-логика
│ │ ├── transaction.py
│ │ └── category.py
│ ├── routes/ # HTTP обработчики
│ │ ├── transactions.py
│ │ └── categories.py
│ ├── dependencies.py # DI ключи
│ ── main.py # Точка входа
├── db/
│ └── schema.sql # SQL схема базы данных
├── tests/ # Интеграционные тесты
│ ├── conftest.py
│ ├── test_endpoints_transactions.py
│ └── test_endpoints_category.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```
## Установка и запуск

### Требования

- Docker и Docker Compose
- Python 3.12+

### Быстрый старт

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd expense-tracker
```
2. Создайте файл окружения:
```bash
cp .env.example .env
```
3. Запустите приложение:
```bash
docker-compose up --build -d
```
Приложение будет доступно по адресу http://localhost:8080
База данных инициализируется автоматически при первом запуске.

### Локальная разработка

Для запуска тестов локально:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt
pytest tests/ -v
```

## API Documentation
### +++ Транзакции +++
### Создание транзакции
```http
POST /transactions
Content-Type: application/json

{
  "type_of_transaction": "expense",
  "amount": 1500.00,
  "description": "Покупка продуктов",
  "date_of_transaction": "2026-09-15T12:00:00",
  "category_ids": ["uuid-1", "uuid-2"]
}
```

### Получение транзакции по ID
```http
GET /transactions/{id}
```

### Получение всех транзакций

```http
GET /transactions
```

### Обновление транзакции
```http
PUT /transactions/{id}
Content-Type: application/json

{
  "amount": 2000.00,
  "description": "Обновленное описание"
}
```

### Удаление транзакции
```http
DELETE /transactions/{id}
```

### Фильтрация транзакций
```http
GET /transactions/filter?date_from=2026-09-01&date_to=2026-09-30&category_id=uuid
```

### Статистика по транзакциям
```http
GET /transactions/stats
```
Ответ:
```json
{
  "total_income": "5000.00",
  "total_expense": "3000.00",
  "balance": "2000.00"
}
```

### Расходы по категориям
```http
GET /transactions/expenses
```
Ответ:
```json
{
  "Продукты": "1500.00",
  "Транспорт": "500.00"
}
```
### +++ Категории +++
### Создание категории
```http
POST /categories
Content-Type: application/json

{
  "name": "Продукты",
  "description": "Расходы на еду"
}
```

### Получение категории по ID
```http
GET /categories/{id}
```

### Получение всех категорий
```http
GET /categories
```
### Обновление категории
```http
PUT /categories/{id}
Content-Type: application/json

{
  "name": "Новое название",
  "description": "Новое описание"
}
```

### Удаление категории
```http
DELETE /categories/{id}
```

## Тестирование

Проект покрыт интеграционными тестами, которые проверяют все эндпоинты API через HTTP запросы.
```bash
# Запуск всех тестов
pytest tests/ -v

# Запуск тестов с выводом print
pytest tests/ -v -s

# Запуск конкретного файла тестов
pytest tests/test_endpoints_transactions.py -v
```
Тесты используют FakeRepository для работы в памяти без подключения к реальной базе данных.

## Особенности реализации
- Асинхронность: все операции с БД выполняются асинхронно через asyncpg;
- Пул соединений: используется connection pool для эффективного управления соединениями с PostgreSQL;
- Типизация: строгая типизация через Pydantic модели и web.AppKey;
- Параметризованные запросы: защита от SQL-инъекций через параметризацию;
- UUID: использование UUID для идентификаторов вместо автоинкремента;
- Decimal: точные вычисления с денежными суммами через Decimal.

### Лицензия
MIT