import requests as re   # Импорт модуля requests для отправки запрососв через DTF api
import json             # Импорт модуля json для работы с возвращаемой api строкой json 
import os.path          # Импорт модуля os.path для проверки существования файла в директории скрипта

# Главный метод
def main():
    _id = int(input('Ввод ID статьи: ')) # Ввод индекса статьи на DTF(подчёркивание из-за того, что слово id зарезервировано)
    
    # Название статьи
    Title = re.get(f'https://api.dtf.ru/v1.9/entry/{ _id }').json()['result']['title']

    # Никнейм автора статьи
    Author_Name = re.get(f'https://api.dtf.ru/v1.9/entry/{ _id }').json()['result']['author']['name']
    
    # ID автора статьи
    Author_ID = re.get(f'https://api.dtf.ru/v1.9/entry/{ _id }').json()['result']['author']['id']


    print(f'\nНазвание и автор публикации: \n\t{ Title }   -----   { Author_Name }')
    
    # С помощью модуля requests через api DTF'а получаем строку json со всеми комментариями
    # Она приведена в питоновский формат словаря с помощью модуля json и выбран второй ключ, а именно "result"
    # т.к. огромный словарь имеет два ключа, один из которых это сообщение от api, которое нам не нужно
    # Поэтому берём ключ "result", в коотором хранятся все комменты и ответы к ним
    comments = re.get(f'https://api.dtf.ru/v1.8/entry/{ _id }/comments/popular').json()["result"]
    
    # Список комментаторов с дублями. Гуляем по списку комментов и с помощью Ф-строки добавляем, то что будет выведено
    # В итоговый файл
    result = [f'https://dtf.ru/u/{ i["author"]["id"] }   -------------    { i["author"]["name"] }' for i in comments]             

    # Метод для записи в файл
    def work_with_file(result):
        count = 0

        # Список имен в файле
        # Изначально использовался стандартный метод set()
        # Но из-за него имена не по порядку выводятся, т.к. он(я не совсем уверен, но вроде так),
        # если элемент присутствует как-бы переносит его вперёд
        names_in_file = []
        with open('file.txt', mode='w', encoding='utf-8') as file:
            # Просто гуляем по списку и выводим имена в файл
                for i in result:
                    if i in names_in_file:
                        pass #Место для дебага на будущее
                    else:
                        if i != f'https://dtf.ru/u/{ Author_ID }   -------------    { Author_Name }':
                            count += 1
                            file.write(f'{ count }  ---  { i }\n')
                            names_in_file.append(i)
        print(f'Автор исключен из списка     ------------------     https://dtf.ru/u/{ Author_ID }  --  { Author_Name }\n')
        print(f'\nВсё!       Всего { count } участников!\n')
    
    # Проверка есть ли файл в директории со скриптом
    if os.path.isfile('file.txt'):
        y_or_n = input('\nФайл уже есть. Заменить всё содержимое? Y/N?   ')
        if y_or_n.lower() == 'y':
            print(f'\n{"-"*50}Перезаписываю файл...{"-"*49}\n')
            work_with_file(result)
        else:
            print()
    else:
        print(f'\n{"-"*50}Создаю файл...{"-"*50}\n')
        work_with_file(result)

# Точка входа в программу, хотя она не очень-то и нужна, но это считают хорошим тоном
if __name__ == '__main__':
    main()
    input('Нажмите ENTER для выхода...')
