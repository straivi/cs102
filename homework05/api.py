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
    access_token = "79e9ef8cdd14d14e26d63e2bff4f190ea2bb2d32610d632226db68d27e151a576d9efa70f8aa026e92f23"
    v = '5.103'

    query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
    response = requests.get(query)
    print(response.json())
    response = response.json()
    return response




def messages_get_history(user_id, offset=0, count=20):
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    # PUT YOUR CODE HERE
