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
Представьте, что вы известный поэт с высоким навыком рифмования, а так же известный музыкальный исполнитель. 
Ваша задача придумать осмысленную песню в определенном жанре, которая понравится людям. 
Вам будет дана первая строка песни, а так же жанр. Вы должны вернуть только текст песни."""
iam_token = 't1.9euelZqYypfPiZqLjsicmJiWm86Liu3rnpWaiZ2VyZTIx8aUkc7MkJqRko7l8_daby5P-e8UFDkJ_t3z9xoeLE_57xQUOQn-zef1656VmsqSxsuJz52azY2Tk4vOmZ6W7_zF656VmsqSxsuJz52azY2Tk4vOmZ6W.tEGyYaegYVVpcAe5Ov2q-wdRN-m68vjRTygvyajHOMxQCtoehWNEZsHaCdNVfl0jGZaCc9XimCIOWhbdHeiNAQ'
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

task = """
Первая строка: Вышка, студкемп, браточки с кайфом
Жанр: Рэп
"""
yandex_request_info = YandexRequestInfo(baseline_prompt, task, folder_id, iam_token, 0.8)
operation_id = ask_gpt_with_prompt(yandex_request_info)
operation_result = await fetch_operation_result(operation_id)