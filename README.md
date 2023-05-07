# TMS. Homework. Gitflow.
## Homework 18
* Создать класс Permissions
  * cоздать boolean свойства на чтение запись - create,read,update,delete
* Cоздать класс Role
  * создать свойство только на чтение строку name
  * cоздать свойство role которое является словарём где ключ
    имена наших классов выполняющие бизнес логику (Credit,Deposit,DebitAccount,CreditAccount,User,Organisation,Identity)
    а значение объекты Permissions
  ** Либо класс Role должен принемать как ключ имена выше указанных классов и выдовать 
     в качестве значений объекты Permissions
     >> a = Role("default",**dict_with_permissions)
     >> a.name
     default
     >> a["Credit].create
     False
     >> a["DebitAccount"].update
     False
* Создать класс Entity
  * Создать свойство только на чтение - entity_id (оно должно быть int)
  * Cоздать свойcтво на чтение/запись - role с типом Role.
* Создать класс User
  * Унаследоваться от Entity
  * добавить свойства только на чтение first_name, last_name, fathers_name, date_of_birth
  * добавить свойство только на чтение age, которое высчитывается из date_of_birth
* Создать класс Organisation
  * Унаследоваться от Entity
  * добавить свойства creation_date, unp, name
* Создать класс App
  * Унаследоваться от Entity
  * добавить свойства name
* Прочитать данные из файлов users.json, apps.yaml, roles.yaml и создать на основании их объекты
* В функции сreate_user из предыдущего задания создаём не словарь а объект

