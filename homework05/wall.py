import copy
import pandas as pd
import pyLDAvis
import pymorphy2
import requests
from dawg_python import Dictionary
from gensim.models import LdaModel
import nltk
from nltk.corpus import stopwords
from gensim.corpora.dictionary import Dictionary
import pyLDAvis.gensim


def get_wall(
    owner_id: str='',
    domain: str='',
    offset: int=0,
    count: int=10,
    filter: str='owner',
    extended: int=0,
    fields: str='',
    v: str='5.103'
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.
    """
    code = {
        "owner_id": owner_id,
        "domain": domain,
        "offset": offset,
        "count": count,
        "filter": filter,
        "extended": extended,
        "fields": fields,
        "v": v
    }
    response = requests.post(
        url="https://api.vk.com/method/execute",
        data={
            "code": f'return API.wall.get({code});',
            "access_token": 'cd65d72d4b868ca790e7132d5883a085241e7e907cb69f35241bbd4f0efe39c98a14eead782879207b86d',
            "v": v
        }
    )
    wall = response.json()
    return wall['response']['items']


def prepare_text(wall, count):
    # собираем все посты в один текст
    text = ''
    for i in range(count):
        try:
            text += wall[i]['text']
            text += ' '
        except IndexError:
            break
    #удаляем ссылки
    text = text.split()
    for word in text:
        if 'http' or '#' or '.ru' or '.com' in word:
            text.remove(word)
    #удаляем символы
    text = ' '.join(text)
    newText = ''
    for word in text:
        if word.isalpha() is True or word == ' ':
            newText += word
        if word == '\n':
            newText += ' '
    text = newText
    # Проведим нормализацию
    morph = pymorphy2.MorphAnalyzer()
    text = text.split()
    for i in range(len(text)):
        text[i] = morph.parse(text[i])[0].normal_form
    # Удаляем стоп слова
    withOutStopWords = copy.copy(text)
    for word in text:
        if word in (stopwords.words('russian') + stopwords.words('english')):
            withOutStopWords.remove(word)
    return  withOutStopWords


def topic_model(clean_txt: list, num_count: int):
    """Визуализация тематической модели"""
    clean_txt = [clean_txt]
    common_dictionary = Dictionary(clean_txt)
    common_corpus = [common_dictionary.doc2bow(text) for text in clean_txt]
    lda = LdaModel(common_corpus, num_topics=num_count)
    vis = pyLDAvis.gensim.prepare(lda, common_corpus, common_dictionary)
    pyLDAvis.save_html(vis, 'LDA.html')
    pyLDAvis.show(data=vis, open_browser=True)

wall1 = get_wall(domain='kislenkoracing', count=500)
wall2 = get_wall(domain='volchok', count=500)
text1 = prepare_text(wall1, 500)
text2 = prepare_text(wall2, 500)
allText = text1 + text2
topicModel(allText, 2)
