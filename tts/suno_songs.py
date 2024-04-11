import requests
import asyncio
from datetime import datetime
import os

base_url = 'https://suno-api-sigma-liart.vercel.app/'


class AudioLoadException(Exception):
    pass


def custom_generate_audio(payload):
    url = f"{base_url}/api/custom_generate"
    response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
    return response.json()


def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = requests.get(url)
    return response.json()


def load_song(url: str, need_path: bool = False):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if not os.path.isdir('AudioFiles'):
        os.mkdir('AudioFiles')
        os.mkdir('AudioFiles/suno')
        os.mkdir('AudioFiles/tts')

    filename = 'AudioFiles/suno/' + timestamp + '.mp3'
    with open(filename, 'wb') as f:
        f.write(requests.get(url).content)
        if need_path:
            return filename


async def generate_audio(song, genre, need_path: bool = False):
    data = custom_generate_audio({
        "prompt": song,
        "tags": genre,
        "title": "Test",
        "make_instrumental": False,
        "wait_audio": False
    })

    if data:
        if not isinstance(data, dict):
            ids = f"{data[0]['id']},{data[1]['id']}"

            for i in range(3):
                data = get_audio_information(ids)

                if data[0]["status"] == 'streaming':
                    fn = load_song(data[0]['audio_url'], True)
                    if need_path:
                        return fn
                    return data[0]['audio_url']

                # На первой итерации ждём 75 секунд
                if i == 0:
                    await asyncio.sleep(75)
                else:
                    await asyncio.sleep(30)
        elif 'error' in data.keys():
            raise AudioLoadException('Не удалось сгенерировать песню 😭')

        if isinstance(data, list):
            return data[0]['audio_url']
