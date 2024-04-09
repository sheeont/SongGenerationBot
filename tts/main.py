"""
Пример использования файла

Нужно импортировать класс:
from tts.main import TTS

После в нужном месте инициализировать класс (лучше делать единожды,
чтобы не тратить лишнее время на инициализацию
tts_obj = TTS()

С помощью set_text_to_tts выставляем текст для озвучивания
tts_obj.set_text_to_tts(example_text)

Вызываем метод get_audio, в списке audio_paths будет находиться путь к файлу
audio_paths = tts_obj.get_audio()
"""

from io import TextIOWrapper
from datetime import datetime
import shutil
import torch


class TTS:
    __language = 'ru'
    __model_id = 'v4_ru'
    __put_accent = True
    __put_yo = True
    sample_rate = 48000
    speaker = 'xenia'
    file_instance: TextIOWrapper

    def __init__(self):
        device = torch.device('cpu')
        self.model, self.text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                               model='silero_tts',
                                               language=self.__language,
                                               speaker=self.__model_id)
        self.model.to(device)

    @staticmethod
    def format_audio(path: str) -> str:
        # Генерация временной метки для имени файла
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        destination = 'media/' + timestamp + '.wav'

        # Перемещение и переименование файла
        shutil.move(path, destination)

        return destination

    def generate_audio(self) -> None:
        path = self.model.save_wav(text=self.text,
                                   speaker=self.speaker,
                                   sample_rate=self.sample_rate)

        self.file_instance = open(self.format_audio(path), 'r')

    def generate_audio_by_text(self, text: str) -> None:
        self.text = text
        self.generate_audio()

    def get_file_instance(self) -> TextIOWrapper:
        return self.file_instance
