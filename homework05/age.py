import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends
#from api_models import User


def age_predict(user_id = 141614829) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    response = get_friends(user_id)
    usersData = []
    for person in range(response):
        try:
            usersData.append(response[person]['bdate'])
        except Exception:
            pass
    ages = 0
    usersWithAge = 0
    for person in usersData:
        personBDate = person.split('.')
        print(personBDate)
        if len(personBDate) < 3: 
            print('skip')
            continue
        ages += get_age(int(personBDate[2]), int(personBDate[1]), int(personBDate[0]))
        usersWithAge += 1
    return int(ages / usersWithAge)



def get_age(year, month, day):
    today = dt.date.today()
    age = today.year - year
    if today.month < month: age -= 1
    elif today.month == month:
        if today.day < day: age -= 1
    return age
    
#print(age_predict())