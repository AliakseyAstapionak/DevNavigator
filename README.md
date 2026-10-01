# DevNavigator

Backend-сервис для IT-специалистов и тех, кто хочет войти в IT. Помогает:

- найти актуальные вакансии через открытые данные портала «Работа России» (trudvsem.ru);
- получить план обучения и стек технологий под выбранную профессию;
- сгенерировать вопросы для технического собеседования по заданному стеку.

AI-функции работают на базе Google Gemini (через OpenAI-совместимый эндпоинт). История всех запросов и ответов сохраняется в PostgreSQL отдельно для каждого пользователя.

## Возможности

- Регистрация и авторизация (JWT в `httpOnly`-cookie)
- Поиск вакансий с фильтрами: текст, регион, минимальная зарплата, пагинация
- Подбор стека и советов по обучению (`role`, `stack`, `learning_advice`, `difficulty`, `estimated_time_months`)
- Генерация 7–12 вопросов для собеседования по стеку (`questions`, `difficulty`)
- Сохранение истории запросов пользователя (JSONB)
- Асинхронная архитектура: от HTTP-клиентов до работы с БД
- Статическая страница на `/` и автодокументация Swagger на `/docs`

## Технологии

| Область | Инструменты |
| Веб-фреймворк | FastAPI, Uvicorn |
| База данных | PostgreSQL, SQLAlchemy 2.0 (async), asyncpg |
| Валидация | Pydantic v2 |
| Авторизация | PyJWT, cookie `access_token` |
| HTTP-клиент | httpx (общий пул соединений) |
| Внешние API | Gemini API, trudvsem.ru Open Data |
| Конфигурация | python-dotenv |

## Быстрый старт

### 1. Требования

- Python 3.10+
- PostgreSQL
- Ключ Gemini API (Google AI Studio)

### 2. Установка

```bash
git clone <url-репозитория>
cd <папка-проекта>

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install fastapi uvicorn sqlalchemy asyncpg pydantic \
            python-dotenv httpx pyjwt bcrypt
```

### 3. Настройка .env

Создайте файл `.env` в корне проекта:

```env
# База данных — вариант 1: по частям
DB_USER=postgres
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=devnavigator

# DATABASE_URL=postgresql://user:password@host:5432/dbname // можно не указывать потому что это для Render

# Авторизация
JWT_SECRET_KEY=change_me_to_a_long_random_string
ACCESS_TOKEN_EXPIRE_SECONDS=3600

# AI
GEMINI_API_KEY=your_gemini_api_key
```

Если задан `DATABASE_URL`, префикс `postgresql://` автоматически заменяется на `postgresql+asyncpg://`.

### 4. Запуск

```bash
python main.py
# или
uvicorn main:app --host 0.0.0.0 --port 8000
```

При старте таблицы `users` и `requests` создаются автоматически (`Base.metadata.create_all`). После запуска доступны:

- приложение: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- health-check: http://localhost:8000/ping

## API

### Авторизация

| Метод | Путь | Описание |
| `POST` | `/registration` | Регистрация нового пользователя |
| `POST` | `/login` | Вход; JWT устанавливается в cookie `access_token` |
| `POST` | `/logout` | Выход; cookie удаляется |

Требования к данным при регистрации:

- `username`: 3–50 символов, только буквы, цифры и `_`
- `password`: 6–20 символов, минимум одна буква и один спецсимвол

### Поиск вакансий

`POST /vacancy_search` — требуется авторизация.

| Поле | Тип | Описание |
| `text` | string (≥2) | Должность или стек |
| `region_code` | string, опц. | Код региона trudvsem (напр. `7700000000000` — Москва) |
| `salary_min` | int, опц. | Минимальная зарплата |
| `limit` | int, 1–100 | Размер страницы (по умолчанию 20) |
| `offset` | int, ≥0 | Смещение для пагинации |

### Стек и советы по обучению

`POST /ai/profession_advice` — требуется авторизация.

```bash
curl -b cookies.txt -X POST http://localhost:8000/ai/profession_advice \
  -H "Content-Type: application/json" \
  -d '{"profession": "Python разработчик на FastAPI"}'
```

Результат (в поле `results.response`):

```json
{
  "role": "Python-разработчик (FastAPI)",
  "stack": ["Python", "FastAPI", "PostgreSQL", "..."],
  "learning_advice": ["..."],
  "difficulty": "средняя",
  "estimated_time_months": 8
}
```

### Вопросы для собеседования

`POST /ai/interview_advice` — требуется авторизация.

```bash
curl -b cookies.txt -X POST http://localhost:8000/ai/interview_advice \
  -H "Content-Type: application/json" \
  -d '{"profession_with_stack": "Python разработчик: FastAPI, Pydantic, PostgreSQL"}'
```

Результат (в поле `results.response`):

```json
{
  "questions": ["...", "..."],
  "difficulty": "средняя"
}
```

### Формат ответа защищённых эндпоинтов

```json
{
  "user": { "id": 1, "username": "john_dev" },
  "results": {
    "id": 42,
    "user_id": 1,
    "request": { "...": "..." },
    "response": { "...": "..." },
    "created_at": "2026-10-01T12:00:00Z"
  }
}
```

## Модель данных

**users**

| Поле | Тип |
| `id` | int, PK |
| `username` | varchar(50), unique |
| `hashed_password` | varchar(255) |
| `registrated_at` | timestamptz |

**requests**

| Поле | Тип |
| `id` | int, PK |
| `user_id` | FK → `users.id` (`ON DELETE CASCADE`) |
| `request` | JSONB |
| `response` | JSONB, nullable |
| `created_at` | timestamptz |
