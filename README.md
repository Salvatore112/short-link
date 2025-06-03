# URL Shortener Service

[![CI](https://github.com/Salvatore112/short-link/actions/workflows/ci.yml/badge.svg)](https://github.com/Salvatore112/short-link/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Простой сервис для создания коротких ссылок. Было минимальное отклонение от опционального требования по Makefile: вместо него вся инфраструктура была обернута в Docker, что обеспечивает изоляцию и кроссплатформенность. Кроме того, Docker (а точнее, контейнеризация) всё же более распространён и ожидаем в задачах подобного рода.

## Требования
- **Docker** версии 20.10.0+
- **Docker Compose** версии 1.29.0+

## Быстрый старт

### Сборка проекта
```bash
docker-compose build
```

### Запусок сервиса
```bash
docker-compose up app
```
Сервис будет доступен на http://localhost:8000

### Работа с CLI

#### Создать пользователя
```bash
docker-compose run cli create <username> <password>
```
#### Показать всех пользователей
```bash
docker-compose run cli list
```
#### Удалить пользователя
```bash
docker-compose run cli delete <username>
```

### Запуск тестов
```bash
docker-compose run tests
```

### Документация API

После запуска сервиса:

- Swagger UI: http://localhost:8000/docs

- ReDoc: http://localhost:8000/redoc
