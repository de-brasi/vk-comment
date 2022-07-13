# 2020
"""
Комментирование в задаваемое время определяемых пользователем фотографий ВК с одной страницы или группы.
Вывод логов и получение информации для аутентификации в\из папки проекта.
"""
import vk_api, random, datetime, sys, os

DIR_PATH = os.getcwd()

# Вывод логов
def logs(text):
    logpas = open(DIR_PATH + '/logs.txt', 'a')
    logpas.write(text + '\n')
    logpas.close()


# Датировка запуска в файле логов
now = datetime.datetime.now()
logs(' ')
logs(str(datetime.datetime.now().date()) + ' в {} часов '.format(now.hour) + '{} минут '.format(
    now.minute) + '{} секунд'.format(now.second))

# Прикручивание отдельного файла кэша паролей и логинов в директории проекта
logpas = open(DIR_PATH + '/vkEnterResources.txt', 'r')
login = logpas.readline().strip()  # логин и пароль от двух аккаунтов
password = logpas.readline().strip()
login_other = logpas.readline().strip()
password_other = logpas.readline().strip()
logpas.close()

# Переменные
words_list = ['я', 'бронь', 'мне', 'беру', '1', 'ц1', 'выа', '342', 'иав', 'qwe', 'возьму', 'z', '231', 'выф', 'иввап',
              '123']
set_owner_id = set()  # проверка чтобы все фото из стека были из одной группы
photo_stack = list()  # стек комментируемых фото - глобальная переменная
link_list = []  # накапливает получаемые ссылки
hour_input = 17  # стандартные значения переменных,
minute_input = 0  # изменяемых из GUI
second_input = 0
hour = 0
minute = 1
second = 2


def actualTime():
    """
    Возвращяет актуальное время
    Скорость - более 200 вызовов/секунду через ipynb
    indicates an actual time:
    return (hour, minute, second)
    """
    now = datetime.datetime.now()
    hour = now.hour  # на момент вызова!
    minute = now.minute  # на момент вызова!
    second = now.second  # на момент вызова!
    return hour, minute, second


def ownerId(link):
    """
    Получение id хозяина фотографии из ссылки на нее в альбоме
    Один позиционный аргумент - link(type==str)
    Для сообществ возвращяет отрицательное число
    return(owner_id -> int)
    """
    split_symb = ['/', '?z', '%2', '=']  # словарь символов для разбиения адреса фото
    for x in split_symb:  # разбиение строки по разделительным символам - костыль регулярных выражений
        link = link.replace(x, '/')
    link = link.split('/')

    flag = False  # индикатор успеха нахождения подстроки photo-... в строке адреса фотографии
    for string in link:
        if string.startswith('photo'):
            flag = True
            split_photo_string = ['-',
                                  '_']  # словарь символов для разбиения подстроки содержащей photo_id в адресе фото
            for y in split_photo_string:  # разбиение строки по разделительным символам - костыль регулярных выражений
                string = string.replace(y, '/')
            string = string.split('/')
            owner_id = string[
                len(string) - 2]  # на момент написания кода owner_id было предпоследним элементом в подстроке адреса, 
            try:  # начинающейся с photo-...
                owner_id = int(owner_id)
                return -owner_id
            except:
                # print('Подстрока, начинающаяся с photo-... найдена, но не удалось выделить owner_id являющееся int!')
                log_out.insert(INSERT, (
                            '!Подстрока, начинающаяся с photo-... найдена, но не удалось выделить owner_id являющееся int!' + 12 * ' '))
                logs('!Подстрока, начинающаяся с photo-... найдена, но не удалось выделить owner_id являющееся int!')
                # log_out.insert(INSERT, ' ')
            break
    if not flag:
        # print('Не удалось найти подстроку, начинающуюся с (photo-...). Проблемы в функции ownerId()')
        log_out.insert(INSERT,
                       '!Не удалось найти подстроку, начинающуюся с (photo-...). Проблемы в функции ownerId()' + 20 * ' ')
        logs('!Не удалось найти подстроку, начинающуюся с (photo-...). Проблемы в функции ownerId()')


def photoId(link):  # функция обработки ссылок для получения id фото
    """
    Получение id фото из ссылки на фотографию в альбоме
    return(photo_id -> int)
    """
    if link:
        if len(set_owner_id) <= 1:
            split_symb = ['/', '?z', '%2', '=']  # словарь символов для разбиения адреса фото
            for x in split_symb:  # разбиение строки по разделительным символам - костыль регулярных выражений
                link = link.replace(x, '/')
            link = link.split('/')

            flag = False  # индикатор успеха нахождения подстроки photo-... в строке адреса фотографии
            for string in link:
                if string.startswith('photo'):
                    flag = True
                    split_photo_string = ['-',
                                          '_']  # словарь символов для разбиения подстроки содержащей photo_id в адресе фото
                    for y in split_photo_string:  # разбиение строки по разделительным символам - костыль регулярных выражений
                        string = string.replace(y, '/')
                    string = string.split('/')
                    photo_id = string[
                        len(string) - 1]  # на момент написания кода photo_id было последним элементом в подстроке адреса, 
                    try:  # начинающейся с photo-...
                        photo_id = int(photo_id)
                        return photo_id
                    except:
                        # print('Подстрока, начинающаяся с photo-... найдена, но не удалось выделить photo_id являющееся int!')
                        log_out.insert(INSERT, (
                                    '!Подстрока, начинающаяся с photo-... найдена, но не удалось выделить photo_id являющееся int!' + 12 * ' '))
                        logs(
                            '!Подстрока, начинающаяся с photo-... найдена, но не удалось выделить photo_id являющееся int!')
                        # log_out.insert(INSERT, ' ')
                    break
            if not flag:
                # print('Не удалось найти подстроку, начинающуюся с (photo-...). Проблемы в функции photoId()')
                log_out.insert(INSERT,
                               '!Не удалось найти подстроку, начинающуюся с (photo-...). Проблемы в функции photoId()' + 20 * ' ')
                log_out.insert(INSERT, ' ')
                logs('!Не удалось найти подстроку, начинающуюся с (photo-...). Проблемы в функции photoId()')
        else:
            # print("Добавленны фото из нескольких групп. Пожалуйста, добавляйте фото только из одной группы")
            log_out.insert(INSERT,
                           "!Добавленны фото из нескольких групп. Пожалуйста, добавляйте фото только из одной группы" + 17 * ' ')
            log_out.insert(INSERT, ' ')
            logs("!Добавленны фото из нескольких групп. Пожалуйста, добавляйте фото только из одной группы")


# Main
def main(login=login, password=password, login_other=login_other, password_other=password_other):
    '''
    Основная функция, выполняемая параллельно tkinter-части
    в потоке th_main.
    Задействует vk_api, заходит в вк через login-password,
    в случае vk_api.exceptions.Captcha заходит в
    login_other\password_other, переименовывая их
    (a, b = b, a)
    Берет ИД фот из photo_stack
    ИД хозяина группы из set_owner_id, где должен храниться только 1 элемент.
    '''
    # Перенаправление потока ошибок в файл логов
    err = open(DIR_PATH + '/logs.txt', 'a')
    old_err = sys.stderr
    sys.stderr = err

    session = vk_api.VkApi(login=login, password=password, app_id=2685278)
    session.auth()
    # log.append('выполнен вход в {}'.format(login) + (70 - len('выполнен вход в {}'.format(login))) * ' ')
    log_out.insert(INSERT, '-' * 35)
    log_out.insert(INSERT, 'выполнен вход в {}'.format(login) + (70 - len('выполнен вход в {}'.format(login))) * ' ')
    logs('выполнен вход в {}'.format(login))
    # print('-'*20)
    # print('выполнен вход в {}'.format(login))
    # Организация цикла while (список не пустой) с try-except для отправки сообщений
    owner_id = list(set_owner_id)[0]  # -201267535 id группы для комментирования (ТРЕНИРОВОЧНАЯ ГРУППА)

    while True:  # вместо for i in range(10000)
        time = actualTime()
        if time[hour] == hour_input and time[minute] == minute_input and time[second] >= second_input:
            while photo_stack:  # пока фотот стек не пустой !!!не забывать убирать id из стека после комментирования
                print(photo_stack)
                try:
                    for i in range(len(photo_stack)):
                        photo_id = photo_stack[0]
                        # message = ( str(random.randint(0,100))+chr(random.randint(97, 122)) + ' ' + 
                        #                                    chr(random.randint(65, 90)) + str(random.randint(0,100)) )
                        message = (random.choice(words_list))
                        session.method('photos.createComment', {'owner_id': owner_id,
                                                                'photo_id': photo_id,
                                                                'message': message})
                        # log.append('оставлен комментарий с {}'.format(login))
                        log_out.insert(INSERT, 'оставлен комментарий с {}'.format(login) + (
                                    70 - len('оставлен комментарий с {}'.format(login))) * ' ')
                        logs('оставлен комментарий с {}'.format(login))
                        # print('оставлен комментарий с {}'.format(login))
                        photo_stack.remove(photo_id)

                except vk_api.exceptions.Captcha:
                    # log.append('выход из {}'.format(login))
                    # print('-'*20)
                    log_out.insert(INSERT, '-' * 35)
                    # print('выход из {}'.format(login))
                    log_out.insert(INSERT, 'выход из {}'.format(login) + (70 - len('выход из {}'.format(login))) * ' ')
                    logs('выход из {}'.format(login))
                    login, login_other = login_other, login  # меняем логин и пароль, аутентифицируемся
                    password, password_other = password_other, password
                    session = vk_api.VkApi(login=login, password=password, app_id=2685278)
                    session.auth()
                    # log.append('выполнен вход в {}'.format(login))
                    # print('-'*20)
                    log_out.insert(INSERT, '-' * 35)
                    # print('выполнен вход в {}'.format(login))
                    log_out.insert(INSERT, 'выполнен вход в {}'.format(login) + (
                                70 - len('выполнен вход в {}'.format(login))) * ' ')
                    logs('выполнен вход в {}'.format(login))
                except vk_api.exceptions.ApiError:
                    pass
                global empty_for_normal_text
                empty_for_normal_text = Label(window, text=' ', font=font)
                empty_for_normal_text.grid(column=0, row=8)
            grey_else()
            grey_del()

            global enter_lvl_1
            enter_lvl_1 = Button(window, text="ввести", command=click_enter, font=font)
            enter_lvl_1.grid(column=4, row=0)

            break

    # перевод потока ошибок в нормальное состояние        
    sys.stderr = old_err

    # print('Программа закончила выполнение')
    log_out.insert(INSERT, '-' * 35)
    log_out.insert(INSERT, 'Программа закончила выполнение     ')
    logs('Программа закончила выполнение     ')


# Многопоточность
from threading import Thread

th_main = Thread(target=main, args=())

from tkinter import *

'''
Упрощенная версия без формирования основного стека, а только else и del
'''


# Действия конопок первого уровня______________________________________________________________________________________________
def click_enter():  # пусть станет серой при нажатии
    '''
    Действие кнопки верхнего уровня для ввода времени.
    Меняет значения hour_input, minute_input, second_input,
        если они были введены в поля Entry.
    Генерирует при первом нажатии такую же кнопку, как и кнопку вызова, но темную.
    '''
    global hour_input, minute_input, second_input
    if time_hour.get(): hour_input = int(time_hour.get())  # изменение стандартного значения
    if time_minute.get(): minute_input = int(time_minute.get())  # времени в модуле autocomment_work_module
    if time_second.get(): second_input = int(time_second.get())
    enter_lvl_1 = Button(window, text="ввести", command=click_enter,
                         bg='light grey', font=font)
    enter_lvl_1.grid(column=4, row=0)

    logs('Введенное время - {}:{}:{}'.format(hour_input, minute_input, second_input))


# Действия конопок второго уровня_______________________________________________________________________________________________
def else_photo():
    '''
    Действие кнопки второго уровня для добавления ссылки.
    Генерирует поля ввода для ссылки и приглашающую надпись.
    Вызывает функцию вызова кнопки ввода с параметром 'else'.
    "Красит" вызывающую кнопку и меняет геометрию окна window.
    '''
    global link_invintation, link_enter  # !
    link_invintation = Label(window, text='Вставьте ссылку',
                             font=font)
    link_invintation.grid(column=0, row=3)

    link_enter = Entry(window, width=15, font=font)
    link_enter.grid(column=4, row=3)

    enter('else')

    black_grey_else()
    grey_del()
    window.geometry('370x320')


def del_photo():
    '''
    Действие кнопки второго уровня для удаления ссылки.
    Генерирует поля ввода для ссылки и приглашающую надпись.
    Вызывает функцию вызова кнопки ввода с параметром 'delete'.
    "Красит" вызывающую кнопку.
    '''
    global link_invintation, link_enter  # !
    link_invintation = Label(window, text='Вставьте ссылку',
                             font=font)
    link_invintation.grid(column=0, row=3)

    link_enter = Entry(window, width=15, font=font)
    link_enter.grid(column=4, row=3)

    enter('delete')

    black_grey_del()
    grey_else()


def enter(mod):
    '''
    Вызывается из else_photo или del_photo.
    Функция вызова кнопки для ввода с двумя возможными модификациями:
        'else' - создает кнопку с добавлением ссылки на фото в качестве действия нажатия; 
        'delete' - создает кнопку с удалением, если возможно, ссылки на фото в качестве действия нажатия;
    Кнопка с именем enter_lvl_2 - глобальная для объемлющего модуля переменная.
    '''
    global enter_lvl_2
    if mod == 'else':
        enter_lvl_2 = Button(window, text="     Ввод      ",
                             command=pop_link, font=font)
        enter_lvl_2.grid(column=0, row=4)
    if mod == 'delete':
        enter_lvl_2 = Button(window, text="     Ввод      ",
                             command=del_link, font=font)
        enter_lvl_2.grid(column=0, row=4)


def pop_link():  # отсылает полученную ссылку как строковый элемент в функцию для получения id фото?
    finish_button()
    # log_button()

    link = link_enter.get()
    owner_id = ownerId(link)
    photo_id = photoId(link)
    if link and owner_id and (photo_id not in photo_stack):
        if bool(set_owner_id) == False:
            photo_stack.append(photo_id)  # пропихнуть ссылку
            set_owner_id.add(owner_id)  # owner_id в сет хозяев групп
            link_list.append(link)  # добавить введенную ССЫЛКУ в список ссылок
        elif owner_id in set_owner_id:
            photo_stack.append(photo_id)  # пропихнуть ссылку
            link_list.append(link)  # добавить введенную ССЫЛКУ в список ссылок
        elif owner_id not in set_owner_id:
            # print("!Добавленны фото из нескольких групп. Пожалуйста, добавляйте фото только из одной группы") #вывести предупреждение о том                                                                                                          #   что надо из одной группы кидать
            log_out.insert(INSERT,
                           '!Добавленны фото из нескольких групп. Пожалуйста, добавляйте фото только из одной группы' + 17 * ' ')
            logs('!Добавленны фото из нескольких групп. Пожалуйста, добавляйте фото только из одной группы')
    elif not link:
        log_out.insert(INSERT, 'Вставьте ссылку!' + (35 - len('Вставьте ссылку!')) * ' ')
        logs('Вставьте ссылку!')
    link_enter.delete(0, END)

    window.geometry('370x370')

    print('photo_stack is {}'.format(photo_stack))
    log_out.insert(INSERT, 'Добавленно {} фото'.format(len(photo_stack)) + (
                35 - len('Добавленно {} фото'.format(len(photo_stack)))) * ' ')
    logs('Добавленно {} фото'.format(len(photo_stack)))


def del_link():
    link = link_enter.get()
    if link:
        photo_id = photoId(link)
        if photo_id in photo_stack:
            photo_stack.remove(photo_id)
            try:
                link_list.remove(link)  # удалить, если можно, введенную ССЫЛКУ из списка ссылок
            except:
                pass
        else:
            print('!Невозможно удалить из списка - Вы еще не добавляли такого фото.')  # в вывод пользователю
            log_out.insert(INSERT, '!Невозможно удалить из списка - Вы еще не добавляли такого фото.' + (
                        70 - len('!Невозможно удалить из списка - Вы еще не добавляли такого фото.')))
            logs('!Невозможно удалить из списка - Вы еще не добавляли такого фото.')
    else:
        log_out.insert(INSERT, 'Вставьте ссылку!' + (35 - len('Вставьте ссылку!')) * ' ')
        logs('Вставьте ссылку!')

    link_enter.delete(0, END)
    # print('photo_stack is {}'.format(photo_stack))


# Действия конопок третьего уровня______________________________________________________________________________________________
def finish_button():
    global flag, start

    nothing = Label(window, text=' ', font=font)
    nothing.grid(column=0, row=5)

    start = Button(window, text="Начало работы", command=main_start,
                   font=font)
    start.grid(column=0, row=6)


def main_start():
    '''
    Действия кнопки начала работы.
    Сначала запускает поток th_main с выполнением функции main(главная функция программы),
        потом в логи выводит ссылки, которые должен был откомментить.
    '''
    th_main.start()

    logs('-Введенные для комментирования ссылки:-')
    for link in link_list:
        logs(link)
    logs('-Конец списка ссылок-')


# Состояния конопок второго уровня_______________________________________________________________________________________________        

def grey_else():
    global switch_photo_else
    switch_photo_else = Button(window, text="Добавить к списку",
                               command=else_photo, font=font)
    switch_photo_else.grid(column=0, row=2)


def black_grey_else():
    global switch_photo_else
    switch_photo_else = Button(window, text="Добавить к списку",
                               bg='light grey', command=else_photo, font=font)
    switch_photo_else.grid(column=0, row=2)


def grey_del():
    global switch_photo_del
    switch_photo_del = Button(window, text="Удалить из списка",
                              command=del_photo, font=font)
    switch_photo_del.grid(column=4, row=2)  # было column=1


def black_grey_del():
    global switch_photo_del
    switch_photo_del = Button(window, text="Удалить из списка",
                              bg='light grey', command=del_photo, font=font)
    switch_photo_del.grid(column=4, row=2)  # было column=1


# ____________________________________________Main_part______________________________________________________________________#   

font = ('Georgia', 10)  # шрифты Arial Bold
window = Tk()
window.title('ВК-комментарий по таймеру')
window.geometry('370x270')

# Определение нужного времени
time_invintation = Label(window, text='Время (час/мин/сек) - ',
                         font=font)
time_invintation.grid(column=0, row=0)

time_hour = Entry(window, width=2, font=font)
time_hour.grid(column=1, row=0)

time_minute = Entry(window, width=2, font=font)
time_minute.grid(column=2, row=0)

time_second = Entry(window, width=2, font=font)
time_second.grid(column=3, row=0)

enter_lvl_1 = Button(window, text="ввести", command=click_enter, font=font)
enter_lvl_1.grid(column=4, row=0)

nothing0 = Label(window, text=' ', font=font)  # nothing - костыль для пропуска строки
nothing0.grid(column=0, row=1)

nothing1 = Label(window, text=' ', font=font)
nothing1.grid(column=1, row=1)

nothing2 = Label(window, text=' ', font=font)
nothing2.grid(column=2, row=1)

# для одинакового ввода времени
empty_for_normal_time_entry0 = Label(window, text=' ', font=font)
empty_for_normal_time_entry0.grid(column=1, row=2)

empty_for_normal_time_entry1 = Label(window, text=' ', font=font)
empty_for_normal_time_entry1.grid(column=2, row=2)

empty_for_normal_time_entry2 = Label(window, text=' ', font=font)
empty_for_normal_time_entry2.grid(column=3, row=2)
# Ввод кнопок
grey_else()
grey_del()

# Костыль для нормального вывода текста
empty_for_normal_text = Label(window, text=' ', font=font)
empty_for_normal_text.grid(column=0, row=7)

from tkinter import scrolledtext

log_out = scrolledtext.ScrolledText(window, width=35, height=10)
log_out.grid(column=0, row=8, columnspan=6)

log_out.insert(INSERT, 'По умолчанию значение времени(ч\м\с) = 17:0:0' + (
            70 - len('По умолчанию значение времени(ч\м\с) = 17:0:0')) * ' ')

window.mainloop()
