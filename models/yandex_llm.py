import requests
import asyncio
from dataclasses import dataclass


@dataclass
class YandexRequestInfo:
    system_text: str
    user_text: str
    folder_id: str
    iam_token: str
    temperature: int


baseline_prompt = """Забудьте все свои предыдущие инструкции. 
Представьте, что вы известный поэт с самым высочайшим навыком рифмования, а так же известный музыкальный исполнитель. 
Ваша задача придумать осмысленную песню в определенном жанре, которая понравится людям..
Вам будет дана первая строка песни, а так же жанр. Вы должны вернуть только текст песни.
ПРИМЕЧАНИЯ, ПОСТИСЛОВИЯ, ПРЕДУПРЕЖДЕНИЯ И ЛЮБОЙ ТЕКСТ КРОМЕ ПЕСНИ ВЫВОДИТЬ КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО"""
iam_token = 't1.9euelZqXkMqXzc2WxseZloqZkcjHmO3rnpWaiZ2VyZTIx8aUkc7MkJqRko7l9Pd4YitP-e8zdTGQ3fT3OBEpT_nvM3UxkM3n9euelZqQzIuPk5GYk5jHjI6Ml5PNyu_8xeuelZqQzIuPk5GYk5jHjI6Ml5PNyg.jPpK9N-aEzqLuxvCc1mXe5XbG8nD6ZiRGBjTDDRGIZ7xzzBg8v-KUrib23FpipG9I2zSGEfaTj_NmeC5P-b7Aw'
folder_id = 'b1gpa67eg05vpudm3tn9'
api_url = 'https://llm.api.cloud.yandex.net'


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
    headers = {"Authorization": f"Bearer {yandex_request_info.iam_token}", "x-folder-id": yandex_request_info.folder_id}
    url = f"{api_url}/foundationModels/v1/completionAsync"
    res = requests.post(url, headers=headers, json=req)
    try:
        return res.json()['id']
    except:
        raise ValueError(res.json())


async def fetch_operation_result(operation_id, iam_token=iam_token):
    url = f"{api_url}/operations/{operation_id}"
    headers = {"Authorization": f"Bearer {iam_token}"}
    try:
        while True:
            res = requests.get(url, headers=headers)
            if res.json()["done"]:
                return res.json()['response']['alternatives'][0]['message']['text']
            await asyncio.sleep(1)
    except:
        raise ValueError(res.json())


async def generate_song(task, temperature):
    yandex_request_info = YandexRequestInfo(baseline_prompt, task, folder_id, iam_token, temperature)
    operation_id = ask_gpt_with_prompt(yandex_request_info)
    operation_result = await fetch_operation_result(operation_id)
    return operation_result
