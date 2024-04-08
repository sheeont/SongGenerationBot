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

import torch


class TTS:
    language = 'ru'
    model_id = 'v4_ru'
    sample_rate = 48000
    speaker = 'xenia'
    put_accent = True
    put_yo = True

    def __init__(self):
        device = torch.device('cpu')
        self.model, self.text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                               model='silero_tts',
                                               language=self.language,
                                               speaker=self.model_id)
        self.model.to(device)

    def set_text_to_tts(self, text: str):
        self.text = text

    def get_audio(self):
        return self.model.save_wav(text=self.text,
                                   speaker=self.speaker,
                                   sample_rate=self.sample_rate)
