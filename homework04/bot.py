import requests
import telebot
import datetime
from bs4 import BeautifulSoup

domain = 'http://www.ifmo.ru/ru/schedule/0'
access_token = '1033633823:AAFzt0MqsY392L644yWw88ohAK2p6ICxlwg'
bot = telebot.TeleBot(access_token)


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule(web_page, dayNumber):
    soup = BeautifulSoup(web_page, "html5lib")

    # Проверка существования группы
    page = soup.find("article", attrs={"class": "content_block"})
    try: 
        str(page).index("Расписание не найдено")
        return None
    except ValueError:
        try:
            # Получаем таблицу с расписанием на понедельник
            schedule_table = soup.find("table", attrs={"id": f"{dayNumber}day"})
    
            # Время проведения занятий
            times_list = schedule_table.find_all("td", attrs={"class": "time"})
            times_list = [time.span.text for time in times_list]

            # Место проведения занятий
            locations_list = schedule_table.find_all("td", attrs={"class": "room"})
            room_list = [room.dd.text for room in locations_list]
            locations_list = [room.span.text for room in locations_list]

            # Название дисциплин и имена преподавателей
            lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
            lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
            lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

            return times_list, locations_list, lessons_list, room_list
        except AttributeError:
            return 1


def get_week(week):
    if week == 'uneven':
        return '2'
    elif week == 'even':
        return '1'
    elif week == 'calc':
        return (datetime.datetime.now().isocalendar()[1] + 1) % 2
    return ''


def get_day(command):
    dayDict = {
        'monday' : 1,
        'tuesday' : 2,
        'wednesday' : 3,
        'thursday' : 4,
        'friday' : 5,
        'saturday' : 6,
        'sunday' : 7
        }
    return dayDict[command]


def split_message(message):
    message_list = message.text.split()
    if len(message_list) == 1:
        message_list[0] = "Error request"
        message_list.append('Ты забыл про группу.')
    elif len(message_list) == 2:
        message_list.append(message_list[1].upper())
        message_list.append('')
        message_list[1] = message_list[0]
        message_list[0] = 'Good request'
    elif len(message_list) == 3:
        message_list.append(message_list[2].lower())
        message_list[2] = message_list[1].upper()
        message_list[1] = message_list[0]
        message_list[0] = 'Good request'
    else:
        message_list[0] = "Error request"
        message_list[1] = "слишком много слов."
    return message_list
    

@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на понедельник """
    requestInfo = split_message(message)
    if requestInfo[0] == 'Error request':
        bot.send_message(message.chat.id, requestInfo[1])
        return
    day, group, week = requestInfo[1], requestInfo[2], requestInfo[3]
    if week and week != 'uneven' and week != 'even':
        bot.send_message(message.chat.id, 'PLZ, use even or uneven for specify week.')
        return
    web_page = get_page(group, get_week(week))
    if parse_schedule(web_page, get_day(day[1:])) == None:
        bot.send_message(message.chat.id, "Такой группы не существует.")
        return
    elif parse_schedule(web_page, get_day(day[1:])) == 1:
        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        bot.send_message(message.chat.id, "%s выходной." % days[int(get_day(day[1:])) - 1])
        return
    times_lst, locations_lst, lessons_lst, room_list = \
    parse_schedule(web_page, get_day(day[1:]))
    resp = ''
    for time, location, lession, room in zip(times_lst, locations_lst, lessons_lst, room_list):
        resp += '<b>{}</b>, {}, {} {}\n'.format(time, location, room, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    requestInfo = split_message(message)
    if requestInfo[0] == 'Error request':
        bot.send_message(message.chat.id, requestInfo[1])
        return
    now = datetime.datetime.now()
    group = requestInfo[2]
    week = get_week('calc')
    today = datetime.datetime.now().isoweekday()
    timeNow = tuple([now.hour, now.minute])
    countMinuteNow = (timeNow[0] * 60) + timeNow[1]
    web_page = get_page(group, week)
    if parse_schedule(web_page, today) == None:
        bot.send_message(message.chat.id, "Такой группы не существует.")
        return
    elif parse_schedule(web_page, today) == 1:
        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        bot.send_message(message.chat.id, "%s выходной." % days[today - 1])
        return
    times_lst, locations_lst, lessons_lst, room_list = \
    parse_schedule(web_page, today)
    for item in range(len(times_lst)):
        time = times_lst[item].split('-')
        time = datetime.datetime.strptime(time[0], '%H:%M')
        time = tuple([time.hour, time.minute])
        countMinuteLes = (time[0] * 60) + time[1]
        if countMinuteNow < countMinuteLes:
            resp = '<b>{}</b>, {}, {} {}\n'.format(times_lst[item], locations_lst[item], lessons_lst[item], room_list[item])
            return bot.send_message(message.chat.id, resp, parse_mode='HTML')
    bot.send_message(message.chat.id, 'Lets go home, dude.')


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    today = datetime.datetime.now().isoweekday()
    nextday = today + 1 if today < 7 else 1
    week = get_week('calc') if nextday != 1 else (get_week('calc') + 1) % 2
    requestInfo = split_message(message)
    if requestInfo[0] == 'Error request':
        bot.send_message(message.chat.id, requestInfo[1])
        return
    group = requestInfo[2]
    get_page(group, week)
    web_page = get_page(group)
    if parse_schedule(web_page, nextday) == None:
        bot.send_message(message.chat.id, "Такой группы не существует.")
        return
    elif parse_schedule(web_page, nextday) == 1:
        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        bot.send_message(message.chat.id, "%s выходной." % days[nextday - 1])
        return
    times_lst, locations_lst, lessons_lst, room_list = \
    parse_schedule(web_page, nextday)
    resp = ''
    for time, location, lession, room in zip(times_lst, locations_lst, lessons_lst, room_list):
        resp += '<b>{}</b>, {}, {} {}\n'.format(time, location, room, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    requestInfo = split_message(message)
    if requestInfo[0] == 'Error request':
        bot.send_message(message.chat.id, requestInfo[1])
        return
    group = requestInfo[2]
    for day in range (1,8):
        web_page = get_page(group)

        if parse_schedule(web_page, day) == None:
            bot.send_message(message.chat.id, "Такой группы не существует.")
            return
        elif parse_schedule(web_page, day) == 1:
            days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
            bot.send_message(message.chat.id, "%s выходной." % days[day - 1])
            return

        times_lst, locations_lst, lessons_lst, room_list = \
        parse_schedule(web_page, day)
        resp = ''
        for time, location, lession, room in zip(times_lst, locations_lst, lessons_lst, room_list):
            resp += '<b>{}</b>, {}, {} {}\n'.format(time, location, room, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['help'])
def get_help(message):
    resp = "*Список команд:* \n\n" \
               "/*weekday* - Получить расписание на указанный день\n" \
               "/near - Получить ближайшее занятие\n" \
               "/tommorow - Получить расписание на следующий день\n" \
               "/all - Получить расписание на всю неделю для указанной группы\n" \
               "/help - Получить список доступных комманд"
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
    
pkg_resources.get_distribution("DateTime").version
