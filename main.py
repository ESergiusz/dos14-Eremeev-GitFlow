# Подгружаем нужные библиотеки, для работы скрипта.
import csv
import yaml
import json
from datetime import datetime

# Объявляем пустые list-ы, которые понадобятся для работы скрипта.
final_list = []
list_csv = []
list_yaml = []
temp = []

# Функция по расчету возраста нашего пользователя.
def age(birth, year=2023):
    result = year - birth
    return result

# Функция по добавлению нового пользователя в основной список через ввод данный через клавиатуру.
def add_new_client():
    temporary_list=[]
    name=input("Input name: ")
    surname=input("Input surname: ")
    middle_name=input("Input middle name: ")
    while True:  # Блок проверки, что введеный год указан цифрами, а не буквами
        year_of_birth=input("Input year of birth (only int): ")
        try:
            year_of_birth=int(year_of_birth)
            if year_of_birth in range(1900,(datetime.now().year)+1): # Основной блок функции
                for i in range(len(final_list)):  # Вычисляем максимальное id из существующих данных. Заполняем временный словарь из имеющихся данных.
                    user_id = final_list[i]['id']
                    temporary_list.append(user_id)
                    max_id = max(temporary_list)
                    new_dict={"id": max_id+1, "first_name": name, "last_name": surname, "fathers_name": middle_name,
                              "date_of_birth": year_of_birth, "date_of_birth": year_of_birth, 'age': age(year_of_birth)}
                final_list.append(new_dict) # Добавляем временный словарь с новым пользователем в основной список.
                with open('users.json', 'w') as convert_to_json:  # Сохраняем основной список в формате json в файл user.json.
                    json.dump(final_list, convert_to_json, ensure_ascii=False, indent=2)
                with open('users.json','r') as f: # Открываем файл user.json на чтение.
                    read_json = json.loads(f.read())
                print(read_json)
            elif year_of_birth in range((datetime.now().year)+1,9999):
                print("The user has not been born yet")
            else:
                print("Is the user definitely alive? Check and try again")
                break
        except ValueError:
            print("This is not integer. Try again.")
        else:
            break

# Открываем файл users.csv. Достаем данные о пользователях, сортируем и заносим во временный список list_csv.
with open('users.csv', 'r') as csvfile:
    read_csv = csv.reader(csvfile)
    next(csvfile)
    for line in read_csv:
        list_csv.append({"id": int(line[0]), "first_name": line[1], "last_name": line[2], "fathers_name": line[3],
                         "date_of_birth": int(line[4])})

# Открываем файл users.yaml. Достаем данные о пользователях, сортируем и заносим во временный список list_yaml.
with open('users.yaml', 'r') as yamlfile:
    read_yaml = yaml.load(yamlfile, Loader=yaml.FullLoader)
    for line in read_yaml['users']:
        temp.append(line)
        list_yaml = [{'id': int(obj['id']), 'first_name': obj['first_name'],
                      'last_name': obj['last_name'], 'fathers_name': obj['fathers_name'],
                      'date_of_birth': int(obj['date_of_birth'])} for obj in temp]

# Создаем окончательный список из двух временных ранее созданных списков list_csv и list_yaml
final_list = list_csv + list_yaml

# Сортируем по id для красивого вывода
final_list.sort(key=lambda d: int(d['id']))

# Расчитываем возраст пользователя через функцию age и заносим в его карточку.
for i in range(len(final_list)):
    vozrast = final_list[i]['date_of_birth']
    final_list[i]['age'] = age(vozrast)

# Ковертируем наш финальный список в формат json и заносим данные в файл users.json.
with open('users.json', 'w') as convert_to_json:
    json.dump(final_list, convert_to_json, ensure_ascii=False, indent=2)

# Небольшой case по выбору вариантов работы скрипта
command = input("What are you doing next? View user.json (input view) "
                "or add user (input add) and view user.json? For quit input quit: \n")
match command.split():
    case ["quit"]:
        print("Goodbye!")
    case ["view"]:
        with open('users.json','r') as f:
            read_json = json.loads(f.read())
        print(read_json)
    case ["add"]:
        add_new_client()
    case _:
        print(f"Sorry, I couldn't understand {command}. Goodbye")