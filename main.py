# Lesson 16
#База данных отдаёт 3 массива cтрок с информацией о пользователях. Все строки имеют вид - "<id>_<атрибут пользователя>".
#Нужно обработать эти данные и создать массив из словарей
#[ {id: "<some_id>", first_name: "<some_first_name>", last_name: "<some_last_name>", date_of_birth:<some_age>}
#{id: "<some_id_2>", first_name: "<some_first_name_2>", last_name: "<some_last_name_2>", date_of_birth: <some_age_2>}]
#и вывести на экран
#Вводные данные заносим в список
surname_list = ["2_Комарова","5_Леонова","10_Фадеева","6_Соколова","4_Назаров","7_Дроздова","8_Гордеева","3_Смирнов","9_Николаев","1_Калашников"]
name_list = ["2_Варвара","6_Алина","9_Владислав","4_Владислав","5_Анастасия","3_Антон","1_Марк","8_Амелия","7_Василиса","10_София"]
middle_name_list = ["2_Олеговна","1_Анатольевич","3_Эдуардович","5_Валерьевна","7_Игоревна","6_Васильевна","9_Иосифович","8_Александровна","10_Игоревна","4_Владимирович"]
year_of_birth_list = ['1_1985','3_1978','4_2001','10_1982','5_1970','6_1990','8_1963','7_2004','2_1996','9_1966']

#Объявляем пустой список под финальный вывод
final_list = []

#Сортируем каждый список по возрастанию
surname_list.sort(key=lambda x: int(x.split("_")[0]))
name_list.sort(key=lambda x: int(x.split("_")[0]))
middle_name_list.sort(key=lambda x: int(x.split("_")[0]))
year_of_birth_list.sort(key=lambda x: int(x.split("_")[0]))

#В цикле разбиваем данные каждый ячейки списка на 2 два значения (убирая "_") и присваеваем значение переменной.
for i in range(len(surname_list)):
    id, first_name = name_list[i].split("_")
    id, middle_name = middle_name_list[i].split("_")
    id, last_name = surname_list[i].split("_")
    id, year_of_birth = year_of_birth_list[i].split("_")
    #Заполняем временный словарь
    temp_list = {"id": id, "last_name": last_name, "first_name": first_name, "middle_name": middle_name, "date_of_birth": year_of_birth}
    #Заполняем финальный список
    final_list.append(temp_list)
print(final_list)