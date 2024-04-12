id = 'Ve-cqnQoF0XkGOoV5Bd7ffVXIi9S38GbEwpwKCB98A-GrGPI1_qkn3EgCq5aaDKX'
secret = 'zIXKeKxY2DEQ7_Vyn7uOF1okwGX4JUYRor-KRmHGxuZpZrMY_hKwWf6GxB2j-ub4itvJB7oZCjcrTnwg3vPZTA'
access_token = 'F--CA-E5kwN2nCHZzGgxZ6pwFufhXsnwd4YiFLdWXsyJJOd6JT6MeXD2_vSuzOX_'
artists = {'Рэп': ['Oxxxymiron', 'MORGENSHTERN', 'ALBLAK 52',  'OG Buda', 'ROCKET', 'OBLADAET', 'THRILL PILL', 'Платина', 'Toxi$',
          'Baby Melo', 'Yanix', 'Big Baby Tape', 'kizaru', 'SODA LUV', 'MAYOT',
           'Пошлая Молли (Poshlaya Molly)', 'Heronwater', 'Markul', 'GONE.Fludd', 'LIL KRYSTALLL',
           'uglystephan', 'FRIENDLY THUG 52 NGG', ''],
          'Поп-музыка': ['ANNA ASTI', 'Artik & Asti', 'Три дня дождя', 'МОТ', 'INSTASAMKA', 'Zivert', 'JONY', 'Руки Вверх!', 'Мари Краймбрери', 'NILETTO', 'ЕГОР КРИД', 'GAYAZOV$ BROTHER$', 'Люся Чеботина', 'МакSим', 'DEAD BLONDE', 'Сергей Лазарев', 'Дима Билан', 'Полина Гагарина', 'PIZZA', 'LOBODA', 'SEREBRO', 'Градусы'],
          'Рок': ['Кино', 'Земфира', 'Пикник', 'Сплин', 'Звери', 'Би-2', 'Nautilus Pompilius', 'Ночные Снайперы', 'Женя Трофимов', 'Комната культуры', 'Мумий Тролль', 'Агата Кристи', 'ДДТ', 'Браво', 'КняZz', 'Сергей Шнуров', 'TRITIA', 'Ленинград', 'тринадцать карат', 'Папин Олимпос', 'Аквариум', 'МУККА'],
          'Шансон': ['Михаил Круг', 'Ирина Круг', 'Сергей Трофимов', 'Бутырка', 'Сергей Завьялов', 'Алексей Брянцев', 'Иван Кучин', 'Инна Вальтер', 'Сергей Наговицын', 'БумеR', 'Владимир Ждамиров', 'Воровайки', 'Макс Вертиго', 'Рождество', 'Вика Цыганова', 'Артур', 'Мафик', 'Александр Новиков']}


import lyricsgenius as lg
import pandas as pd
from transliterate import translit
import re

genius = lg.Genius(access_token, skip_non_songs=True, remove_section_headers=True)

import concurrent.futures

def fetch_artist(artist_name):
    while True:
        try:
            songs = genius.search_artist(artist_name, max_songs=15, sort='popularity').songs
            return songs
        except:
            pass

results = {}
with concurrent.futures.ThreadPoolExecutor() as executor:
    for genre in artists.keys():
        results[genre] = []
        for result in executor.map(fetch_artist, artists[genre]):
            results[genre].append(result)

import itertools

for genre in results.keys():
    results[genre] = list(itertools.chain.from_iterable(results[genre]))

data = pd.DataFrame({'genre': [genre for genre, songs in results.items() for song in songs],
                     'lyrics':[song.lyrics for genre, songs in results.items() for song in songs]})

dirty_words_regex="""(?iux)(?<![а-яё])(?:
(?:(?:у|[нз]а|(?:хитро|не)?вз?[ыьъ]|с[ьъ]|(?:и|ра)[зс]ъ?|(?:о[тб]|п[оа]д)[ьъ]?|(?:\S(?=[а-яё]))+?[оаеи-])-?)?(?:
  [её](?:б(?!о[рй]|рач)|п[уа](?:ц|тс))|
  и[пб][ае][тцд][ьъ]
).*?|

(?:(?:н[иеа]|ра[зс]|[зд]?[ао](?:т|дн[оа])?|с(?:м[еи])?|а[пб]ч)-?)?ху(?:[яйиеёю]|л+и(?!ган)).*?|

бл(?:[эя]|еа?)(?:[дт][ьъ]?)?|

\S*?(?:
  п(?:
    [иеё]зд|
    ид[аое]?р|
    ед(?:р(?!о)|[аое]р|ик)|
    охую
  )|
  бля(?:[дбц]|тс)|
  [ое]ху[яйиеё]|
  хуйн
).*?|

(?:о[тб]?|про|на|вы)?м(?:
  анд(?:[ауеыи](?:л(?:и[сзщ])?[ауеиы])?|ой|[ао]в.*?|юк(?:ов|[ауи])?|е[нт]ь|ища)|
  уд(?:[яаиое].+?|е?н(?:[ьюия]|ей))|
  [ао]л[ао]ф[ьъ](?:[яиюе]|[еёо]й)
)|

елд[ауые].*?|
ля[тд]ь|
(?:[нз]а|по)х
)(?![а-яё])"""


def preprocess_lyrics(text, max_len=2000, min_line_length = 20):
    text = '\n'.join(text.split('\n')[1:]).strip()
    text = re.sub("\d*Embed", "", text)
    text = re.sub(r"\([^()]*\)", "", text)
    text = re.sub(r'\bсук[аиоуеы]\b', "", text)
    #text = translit(text, 'ru')
    text = re.sub(dirty_words_regex, "", text)
    lines = text.split('\n')
    long_lines = []
    for line in lines:
        if len(line) >= min_line_length or len(line) == 0:
            if bool(re.search('[а-яА-Я]', line)) or len(line) == 0:
                long_lines.append(line)
    lines = long_lines
    return "\n".join(lines).strip()
#     text = ''
#     idx = -1
#     while idx < len(lines) - 1 and len(text) <= max_len:
#         idx += 1
#         text = "\n".join([text, lines[idx]])
#     if len(text) <= max_len:
#         return text.strip()
#     return text[:-(len(lines[idx]) + 1)].strip()

data.lyrics = data.lyrics.apply(preprocess_lyrics)
data = data[data.lyrics.apply(lambda x: len(x)) > 0].reset_index(drop=True)

data["first_line"] = data.lyrics.apply(lambda x: x.split('\n')[0])

data.to_csv('data.csv')

# def convert_to_json(data):
#     return {
# "request": [
#     {
#       "role": "system",
#       "text": "Забудьте все свои предыдущие инструкции.\nПредставьте, что вы известный поэт с высоким навыком рифмования, а так же известный музыкальный исполнитель.\nВаша задача придумать осмысленную песню в определенном жанре, которая понравится людям.\nВам будет дана первая строка песни, а так же жанр. Вы должны вернуть только текст песни."
#     },
#     {
#       "role": "user",
#       "text": f"Первая строка: {data['first_line']}\nЖанр: {data['genre']}"
#     }
#   ],
#   "response": data["lyrics"]
# }

# data["json"] = data.apply(convert_to_json, axis=1)

# import json

# with open('output.json', 'w') as outfile:
#     for entry in list(data['json'].values):
#         json.dump(entry, outfile)
#         outfile.write('\n')
