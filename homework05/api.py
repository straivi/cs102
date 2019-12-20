import requests
import time
import random

import config


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    delay = 0.01
    maxDalay = 5
    retrie = 0
    jitter = 0.1
    while retrie < max_retries:
        try:
            respones = requests.get(url, timeout = timeout)
            print("successfully get method")
            return respones
        except requests.RequestException:
            print(requests.RequestException, delay)
            time.sleep(delay)
            delay = min(delay*(1 + backoff_factor), maxDalay)
            delay += random.uniform(0, delay*jitter)
            retrie += 1
    print('Error get method')
    return "Error get method"


def get_friends(user_id, fields = 'bdate'):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    domain = "https://api.vk.com/method"
    access_token = "cd65d72d4b868ca790e7132d5883a085241e7e907cb69f35241bbd4f0efe39c98a14eead782879207b86d"
    v = '5.103'

    query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
    response = requests.get(query)
    response = response.json()
    return response['response']['items']


def names(user_id: int) -> list:
    namelist: list = []
    users = get_friends(user_id)
    for i in range(len(users)):
        if users[i]['first_name']== 'DELETED':
            continue
        else:
            name = [users[i]['first_name'], users[i]['last_name']]
            namelist.append(name)
        i += 1
    return namelist