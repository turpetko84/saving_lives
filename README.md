# Сохраняя жизни

Сайт приюта для собак — платформа для展示 питомцев, ищущих новый дом.

## О проекте

Мы — команда волонтёров, которые каждый день спасают собак с улицы и ищут им любящих хозяев. Сайт предоставляет:

- **Карусель** с фотографиями собак на главном экране
- **Карточки питомцев** с описанием и кнопкой «Узнать больше»
- **Страница питомца** — подробная информация, форма связи, интеграция с Asana и Jira
- **Админ-панель** — управление питомцями и заявками на усыновление
- **API** — REST API для работы с данными питомцев и заявок
- **Интеграции** — автоматическая задача в Asana или Jira при отправке заявки

## Технологии

| Компонент | Технология |
|-----------|-----------|
| Бэкенд | FastAPI + Uvicorn |
| БД | Firebird SQL |
| Фронтенд | HTML/CSS/JS + Jinja2 (админка) |
| Прокси | Nginx Alpine |
| Контейнеризация | Docker Compose |
| Интеграции | Asana REST API, Jira REST API v3 |

## Запуск

### Через Docker

```bash
docker compose up --build
```

| Сервис | Адрес |
|--------|-------|
| Сайт | http://localhost:8080 |
| API | http://localhost:8000 |
| Админка | http://localhost:8080/admin/dashboard |

### Вход в админку

- Логин: `admin`
- Пароль: `admin123`

### Переменные окружения

Файл `backend/.env`:

```env
# Firebird
FIREBIRD_DSN=localhost:/firebird/data/shelter.fdb
FIREBIRD_USER=SYSDBA
FIREBIRD_PASSWORD=masterkey

# Приложение
SECRET_KEY=change-me-in-production
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Asana (опционально)
ASANA_TOKEN=
ASANA_PROJECT_GID=

# Jira Cloud (опционально)
JIRA_URL=https://your-domain.atlassian.net
JIRA_USER_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token
JIRA_PROJECT_KEY=PROJ
```

## API эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/pets` | Список всех питомцев |
| GET | `/api/pets/random?count=N` | N случайных питомцев |
| GET | `/api/pets/{id}` | Один питомец по ID |
| POST | `/api/applications` | Создать заявку на усыновление |
| POST | `/api/asana/task` | Создать задачу в Asana |
| POST | `/api/jira/task` | Создать задачу в Jira |
| GET | `/api/stats` | Статистика |

## Админ-панель

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/admin/dashboard` | Панель управления |
| POST | `/admin/pets` | Добавить питомца |
| GET | `/admin/pets/{id}/edit` | Редактировать питомца |
| POST | `/admin/pets/{id}/edit` | Сохранить изменения |
| POST | `/admin/pets/{id}/delete` | Удалить питомца |
| POST | `/admin/applications/{id}/status` | Изменить статус заявки |

## Питомцы

| Имя | Порода | Возраст | Пол |
|-----|--------|---------|-----|
| Бобик | Лабрадор-ретривер | 2 года | Мальчик |
| Рекс | Немецкая овчарка | 3 года | Мальчик |
| Мушка | Такса | 5 лет | Девочка |
| Тузик | Беспородный | 1 год | Мальчик |
| Шарик | Кавказская овчарка | 4 года | Мальчик |
| Дружок | Бордер-колли | 2 года | Мальчик |

## Структура проекта

```
saving_lives/
├── index.html                    # Главная страница
├── favicon.svg                   # Favicon (лапка)
├── css/
│   ├── common.css                # Общие стили, модалки
│   └── pet-page.css              # Стили страницы питомца
├── js/
│   ├── modal.js                  # Модалка «Написать нам»
│   ├── asana.js                  # Модалка «Записать в Asana»
│   └── jira.js                   # Модалка «Записать в Jira»
├── images/                       # Фотографии
│   ├── carousel_*.jpg            # Слайды карусели
│   └── pet_*.jpg                 # Фото питомцев
├── nginx.conf                    # Конфигурация Nginx
├── Dockerfile                    # Контейнер Nginx
├── docker-compose.yml            # Оркестрация сервисов
├── backend/
│   ├── .env                      # Переменные окружения
│   ├── requirements.txt          # Python-зависимости
│   ├── Dockerfile                # Контейнер FastAPI
│   └── app/
│       ├── main.py               # FastAPI app
│       ├── config.py             # Настройки
│       ├── database.py           # Firebird: схема + seed
│       ├── routers/
│       │   ├── pets.py           # API питомцев
│       │   ├── applications.py   # API заявок
│       │   ├── admin.py          # Админ-панель
│       │   ├── asana.py          # Интеграция Asana
│       │   └── jira.py           # Интеграция Jira
│       └── templates/
│           ├── base.html         # Базовый шаблон админки
│           ├── dashboard.html    # Дашборд
│           ├── login.html        # Вход
│           ├── edit_pet.html     # Редактирование питомца
│           └── pet.html          # Страница питомца
└── README.md
```

## Лицензия

© 2025 Сохраняя жизни. Все права защищены.
