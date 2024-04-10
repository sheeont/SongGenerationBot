import requests
import asyncio
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class YandexRequestInfo:
    system_text: str
    user_text: str
    folder_id: str
    api_key: str
    temperature: int


api_key = os.getenv('API_KEY')
folder_id = 'b1gpa67eg05vpudm3tn9'
api_url = 'https://llm.api.cloud.yandex.net'
baseline_prompt = """Забудьте все свои предыдущие инструкции. 
Представьте, что вы известный поэт с самым высочайшим навыком рифмования, а так же известный музыкальный исполнитель. 
Ваша задача придумать осмысленную песню в определенном жанре, которая понравится людям..
Вам будет дана первая строка песни, а так же жанр. Вы должны вернуть только текст песни.
ПРИМЕЧАНИЯ, ПОСТИСЛОВИЯ, ПРЕДУПРЕЖДЕНИЯ И ЛЮБОЙ ТЕКСТ КРОМЕ ПЕСНИ ВЫВОДИТЬ КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО"""


def ask_gpt_with_prompt(yandex_request_info: YandexRequestInfo):
    req = {
        "modelUri": f"gpt://{yandex_request_info.folder_id}/yandexgpt-pro",
        "completionOptions": {
            "stream": False,
            "temperature": yandex_request_info.temperature,
            "maxTokens": "1000"
        },
        "messages": [
            {
                "role": "system",
                "text": yandex_request_info.system_text
            },
            {
                "role": "user",
                "text": yandex_request_info.user_text
            }
        ]
    }
    headers = {"Authorization": f"Api-key {yandex_request_info.api_key}", "x-folder-id": yandex_request_info.folder_id}
    url = f"{api_url}/foundationModels/v1/completionAsync"
    res = requests.post(url, headers=headers, json=req)
    try:
        return res.json()['id']
    except:
        raise ValueError(res.json())


async def fetch_operation_result(operation_id, api_key=api_key):
    url = f"{api_url}/operations/{operation_id}"
    headers = {"Authorization": f"Api-Key {api_key}"}
    try:
        while True:
            res = requests.get(url, headers=headers)
            if res.json()["done"]:
                return res.json()['response']['alternatives'][0]['message']['text']
            await asyncio.sleep(1)
    except:
        raise ValueError(res.json())


async def generate_song(task, temperature):
    yandex_request_info = YandexRequestInfo(baseline_prompt, task, folder_id, api_key, temperature)
    operation_id = ask_gpt_with_prompt(yandex_request_info)
    operation_result = await fetch_operation_result(operation_id)
    return operation_result
