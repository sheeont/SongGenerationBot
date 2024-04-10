# Общая задача на все файлы
# TODO: Привести названия файлов, папок, классов, функций, переменных к PEP

styles_data = [
    {
        'text': 'Рэп',
        'callback_data': 'rap'
    },
    {
        'text': 'Поп',
        'callback_data': 'pop'
    },
    {
        'text': 'Рок',
        'callback_data': 'rock'
    },
    {
        'text': 'Шансон',
        'callback_data': 'chanson'
    }
]

text_model_temperature = 6

default_style_type = styles_data[0]['callback_data']

max_message_length = 450
