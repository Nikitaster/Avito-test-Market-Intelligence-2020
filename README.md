# Тестовое задание для стажера в Market Intelligence.

## Задача:

Необходимо реализовать сервис, позволяющий следить за изменением количества объявлений в Авито по определённому поисковому запросу и региону.

Если совсем не получается парсить Авито, можно использовать как основу сервиса любой другой классифайд (на Ваш выбор, но лучше всё-таки Авито).

UI не нужен, достаточно сделать JSON API сервис.

Для написание сервиса можно использовать [FastAPI](https://github.com/tiangolo/fastapi) или любой другой фреймворк.

- [x] Метод `/add` Должен **принимать** поисковую фразу и регион, регистрировать их в системе. **Возвращать** id этой пары.
- [x] Метод `/stat` **Принимает** на вход id связки поисковая фраза + регион и интервал, за который нужно вывести счётчики. **Возвращает** счётчики и соответствующие им временные метки (timestamp).

- [x] Частота опроса = 1 раз в час  для каждого id

### Требования:

- [x] Язык программирования: Python 3.7/3.8
- [x] Использование [Docker](https://www.docker.com), сервис должен запускаться с помощью [`docker-compose up`](https://docs.docker.com/compose/reference/up/).
- [x] Требований к используемым технологиям нет.
- [ ] Код должен соответствовать PEP, необходимо использование type hints, к публичным методам должна быть написана документация.
- [x] Чтобы получить число объявлений, можно:
    - [ ] парсить web-страницу объявления (xpath, css-селекторы)
    - [x] самостоятельно проанализировать трафик на мобильных приложениях или мобильном сайте и выяснить какой там API для получения информации об объявлении (это будет круто!)

### Усложнения:

- [ ] Написаны тесты (постарайтесь достичь покрытия в 70% и больше). Вы можете использовать [pytest](https://docs.pytest.org/en/latest/) или любую другую библиотеку для тестирования.
- [x] Сервис асинхронно обрабатывает запросы.
- [x] Данные сервиса хранятся во внешнем хранилище, запуск которого также описан в `docker-compose`. Мы рекомендуем использовать [MongoDB](https://www.mongodb.com) или [Postgres](https://www.postgresql.org/), но Вы можете использовать любую подходящую базу.
- [x] По каждому id также собираются топ 5 объявлений. На их получение есть отдельная ручка, архитектуру продумайте самостоятельно: ```/stats/top/{search_id}```

