# TMS. Homework. Gitflow.
## Homework 19

* Переименовываем client_id в client_id во всех классах
* Переименовываем class Client в Client
* Прочитать данные из файлов users.json, apps.yaml, roles.yaml и создать на основании их объекты 
* Устанавливаем Flask через poetry
* Наш сервис должен иметь следующий http интерфейс
  * GET /api/v1/users/<client_id> - получить данные о пользователе
    * Перед тем как получить данные посмотреть есть ли у пользователя права на чтение users
      * Найти заголовок token
        * Если его нет ошибка 400 {"status": "error", "message": f"Token header not found"}
      * В заголовке должен быть json {"client_id": <client_id>}
      * По id найти объект и проверить есть ли у роли такой доступ
    * Если не нашли пользователя с таким client_id то возвращаем {"status": "error", "message": f"No user with id = {client_id}"}
  * GET /api/v1/organisations/<client_id> - получить данные об организации 
    * Перед тем как получить данные посмотреть есть ли у пользователя права на чтение organisations
      * Найти заголовок token
        * Если его нет ошибка 400 {"status": "error", "message": f"Token header not found"}
      * В заголовке должен быть json {"client_id": <client_id>}
      * По id найти объект и проверить есть ли у роли такой доступ
    * Если не нашли организацию с таким client_id то возвращаем {"status": "error", "message": f"No organisation with id = {client_id}"}
  * GET /api/v1/users - получить данные о всех пользователях
    * Перед тем как получить данные посмотреть есть ли у пользователя права на чтение users
      * Найти заголовок token
        * Если его нет ошибка 400 {"status": "error", "message": f"Token header not found"}
      * В заголовке должен быть json {"client_id": <client_id>}
      * По id найти объект и проверить есть ли у роли такой доступ
  * GET /api/v1/organisations - получить данные о всех организациях
    * Перед тем как получить данные посмотреть есть ли у пользователя права на чтение organisations
      * Найти заголовок token
        * Если его нет ошибка 400 {"status": "error", "message": f"Token header not found"}
      * В заголовке должен быть json {"client_id": <client_id>}
      * По id найти объект и проверить есть ли у роли такой доступ
  * PUT /api/v1/users - создать пользователя используя {"first_name": "...", "role": "...", "last_name": "...", "fathers_name": "...", "date_of_birth": "..."}
    * Перед тем как получить данные посмотреть есть ли у пользователя права на запись users
      * Найти заголовок token
        * Если его нет ошибка 400 {"status": "error", "message": f"Token header not found"}
      * В заголовке должен быть json {"client_id": <client_id>}
      * По id найти объект и проверить есть ли у роли такой доступ
    * Пишем в файл users.json
  * PUT /api/v1/organisations - создать организацию используя {"role": "", "creation_date": "", "unp": "", "name": ""}
    * Перед тем как получить данные посмотреть есть ли у пользователя права на запись organisations
      * Найти заголовок token
        * Если его нет ошибка 400 {"status": "error", "message": f"Token header not found"}
      * В заголовке должен быть json {"client_id": <client_id>}
      * По id найти объект и проверить есть ли у роли такой доступ
    * Пишем в файл users.json
  * GET /api/v1/credits/authz/{create,read,update,delete}
  * GET /api/v1/deposits/authz/{create,read,update,delete}
  * GET /api/v1/debitaccounts/authz/{create,read,update,delete}
  * GET /api/v1/creditaccounts/authz/{create,read,update,delete}
  * GET /api/v1/users/authz/{create,read,update,delete}
  * GET /api/v1/organisations/authz/{create,read,update,delete}
  * GET /api/v1/identities/authz/{create,read,update,delete}
    * Для каждого из этих URI
      * Найти заголовок token
        * Если его нет ошибка 400 {"status": "error", "message": f"Token header not found"}
      * В заголовке должен быть json {"client_id": <client_id>}
      * По id найти объект и проверить есть ли у роли такой доступ
      * Если есть 200 и {"status": "success", "message": "authorized"}
        * Если нет или, что то пошло не так то  403 {"status": "error", "message": "not authorized"}