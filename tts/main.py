"""
Пример использования файла

Нужно импортировать класс:
from tts.main import TTS

После в нужном месте инициализировать класс (лучше делать единожды,
чтобы не тратить лишнее время на инициализацию
tts_obj = TTS()

Чтобы создать файл с tts, нужно вызвать функцию generate_audio_by_text,
передав в неё текст:
generate_audio_by_text(text)
Она вернёт новый путь к файлу. Все аудиозаписи находятся в папке media с
именем в формате %Y-%m-%d_%H-%M-%S
"""


from datetime import datetime
import shutil
import torch
import os


class TTS:
    __language = 'ru'
    __model_id = 'v4_ru'
    __put_accent = True
    __put_yo = True
    __destination: str
    sample_rate = 48000
    speaker = 'xenia'

    def __init__(self):
        device = torch.device('cpu')
        self.model, self.text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                               model='silero_tts',
                                               language=self.__language,
                                               speaker=self.__model_id)
        self.model.to(device)

    @staticmethod
    def __format_audio(path: str) -> str:
        # Генерация временной метки для имени файла
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if not os.path.isdir('AudioFiles'):
            os.mkdir('AudioFiles')
            os.mkdir('AudioFiles/tts')

        destination = 'AudioFiles/tts/' + timestamp + '.wav'

        # Перемещение и переименование файла
        shutil.move(path, destination)

        return destination

    def __generate_audio(self) -> str:
        path = self.model.save_wav(text=self.text,
                                   speaker=self.speaker,
                                   sample_rate=self.sample_rate)
        self.__destination = self.__format_audio(path)

        return self.__destination

    def generate_audio_by_text(self, text: str) -> str:
        self.text = text
        self.__generate_audio()

        return self.__destination
