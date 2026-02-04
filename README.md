# Game Deals Tracker

Small project to track game deals across stores and send notifications to Telegram based on user subscriptions.

It has:
- Django REST API (stores, deals, subscriptions)
- periodic deal refresh + notification generation
- Telegram bot that talks to the API

## Features

- Stores and deals API
- Filters, search and ordering for deals
- Subscriptions per Telegram chat:
  - optional store filter
  - minimum discount
  - optional maximum price
  - optional text query
- Notification flow:
  - generate notification logs (based on subscriptions)
  - dispatch pending notifications and mark them as sent

## Tech stack

- Python 3.12
- Django + Django REST Framework
- PostgreSQL
- django-filter
- drf-spectacular (schema/docs)
- pyTelegramBotAPI (telebot)
- pytest

## API

Base prefix: `/api/`

### Deals

`GET /api/deals/`

Query params:
- `store` (store id)
- `min_discount` (discount_percent >=)
- `max_price` (sale_price <=)
- `search` (by title)
- `ordering` (example: `-discount_percent`, `sale_price`, `-last_seen_at`)

### Subscriptions (per chat)

`GET /api/subscriptions/?chat_id=<telegram_chat_id>`
`POST /api/subscriptions/?chat_id=<telegram_chat_id>`

The chat_id is used to link subscriptions to a Subscriber record.

### Notifications

Generate logs (creates NotificationLog entries for matched deals):
`POST /api/notification/generate/?chat_id=<telegram_chat_id>`

Dispatch pending notifications (returns items and marks them as sent):
`POST /api/notification/dispatch/?chat_id=<telegram_chat_id>`

## Telegram bot commands

- `/start` show basic info + chat id
- `/subs` list subscriptions for this chat
- `/add` create subscription (bot will ask for input)
- `/check` generate notification logs
- `/notify` dispatch and print new deals (if any)

## Environment variables

The project uses `.env` locally. Example variables:

Backend (Django):
- `SECRET_KEY`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

Bot:
- `TBOT_API_TOKEN`
- `API_URL` (example: `http://127.0.0.1:8000`)

## Run locally (without Docker)

1) Create and activate venv
2) Install requirements
3) Configure `.env`
4) Run migrations
5) Seed demo deals (optional)
6) Run server

## Run with Docker

There is a Dockerfile + docker-compose.yml in the root.

Basic flow:
- `docker compose up --build`
- open API docs: `/api/docs/`

## Tests

Run tests from the backend directory (where pytest.ini is located):

- `pytest -v`

## Notes

- The demo data seeding is meant for development/testing.
- Notification dispatch marks logs as sent, so running it twice will not resend the same deal.
