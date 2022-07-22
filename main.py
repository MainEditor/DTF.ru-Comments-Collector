import requests as re   # Импорт модуля requests для отправки запрососв через DTF api
import json             # Импорт модуля json для работы с возвращаемой api строкой json 
import os.path          # Импорт модуля os.path для проверки существования файла в директории скрипта


# Метод для записи в файл
def work_with_file(raw_data, Author_Name, Author_ID):
    count = 0
    # Список имен в файле
    names_in_file = []
    with open('file.txt', mode='w', encoding='utf-8') as file:
        # Просто гуляем по списку и выводим имена в файл
            for comment_author in raw_data:
                if comment_author in names_in_file:
                    pass #Место для логов на будущее
                else:
                    main_author_string = f'https://dtf.ru/u/{ Author_ID }   -------------    { Author_Name }'
                    if comment_author != main_author_string and comment_author != None:
                        count += 1
                        file.write(f'{ count }  ---  { comment_author }\n')
                        names_in_file.append(comment_author)
    print(f'Автор исключен из списка     ------------------     https://dtf.ru/u/{ Author_ID }  --  { Author_Name }\n')
    print(f'\nВсё!       Всего { count } участников!\n')

# Главный метод
def main():
    DTF_API_VER = 'v1.9'    # Версия апи DTF
    DTFapi = f'https://api.dtf.ru/{ DTF_API_VER }' # Апи дтф куда идут запросы

    _id = input('Введите ID статьи или её URL: ') # Ввод ID статьи на DTF или URL

    # Проверяем является ли введённая информация ссылкой или ID
    if _id[0] == 'h':
        # С помощью запроса вытаскиваем ID статьи
        _id = re.get(f'{ DTFapi }/entry/locate?url={ _id }').json()['result']['id']
        print(f'\nНайденный ID: { _id }')
    else:
        _id = int(_id)
    
    # Название статьи
    Title = re.get(f'{ DTFapi }/entry/{ _id }').json()['result']['title']
    # Никнейм автора статьи
    Author_Name = re.get(f'{ DTFapi }/entry/{ _id }').json()['result']['author']['name']
    # ID автора статьи
    Author_ID = re.get(f'{ DTFapi }/entry/{ _id }').json()['result']['author']['id']

    print(f'\nНазвание и автор публикации: \n\t{ Title }   -----   { Author_Name }')
    
    # С помощью модуля requests через api DTF'а получаем строку json со всеми комментариями
    # Она приведена в питоновский формат словаря с помощью модуля json и выбран второй ключ, а именно "result"
    # т.к. огромный словарь имеет два ключа, один из которых это сообщение от api, которое нам не нужно
    # Поэтому берём ключ "result", в коотором хранятся все комменты и ответы к ним
    comments = re.get(f'https://api.dtf.ru/v1.8/entry/{ _id }/comments/popular').json()["result"]
    
    # Список комментаторов с дублями. Гуляем по списку комментов и с помощью Ф-строки добавляем, то что будет выведено
    # Также отфильтровываем ответы
    raw = []

    # Проходим по всем комментариям
    # И, если он не является ответом, то добавляем его в список, иначе пропускаем
    for i in comments:
        # Если repluTo равняется не равняется нулю, то это ответ, значит берём равные нулю
        if i['replyTo'] == 0:
            raw.append(f'https://dtf.ru/u/{ i["author"]["id"] }   -------------    { i["author"]["name"] }')
        else:
            pass
    
    # Проверка есть ли файл в директории со скриптом
    if os.path.isfile('file.txt'):
        y_or_n = input('\nФайл уже есть. Заменить всё содержимое? Y/N?   ')
        if y_or_n.lower() == 'y':
            print(f'\n{"-"*50}Перезаписываю файл...{"-"*49}\n')
            work_with_file(raw, Author_Name, Author_ID)
        else:
            print()
    else:
        print(f'\n{"-"*50}Создаю файл...{"-"*50}\n')
        work_with_file(raw, Author_Name, Author_ID)

    input('Нажмите ENTER для выхода...')

# Точка входа
if __name__ == '__main__':
    try:
        main()
    except:
        print('\nЧто-то пошло не так :(\n\nСкорее всего неверный ID, или URL скопирован некорректно\n\nПопробуйте ещё раз\n\n')
        input('Нажмите ENTER для выхода...')
