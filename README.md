# TMS. Homework. Gitflow.
## Homework 26
* Добавить в ваше приложение URI /api/v1/<имя сервиса>/health_check которое просто отдаёт 200 на любой GET запрос
* С помощью docker-compose настроить связку nginx -> наш сервис
  • nginx должен быть доступен на 80 порту сервера и проксировать все запросы на наш сервис
  • при запросе на /api/v1/<имя сервиса>/health_check nginx не должен писать никаких логов
* Логи  nginx надо писать в json формате. Со следующей информацией
  *  host
  * ip address с которого послали запрос
  * статус запроса (200,400,500....)
  * размер тела запроса
  * user agent
  * cам запрос (GET / HTTP/1.1)
  * cколько всего запрос занял времени
  * сколько отвечал на запрос наш сервис