import json
import requests

from app.constants import TOKEN, TOKEN_URL, LLM_FOLDER, LLM_URL, LLM_SYSTEM_PROMPT


class LLMController:
    def __init__(self, temperature: int = 0.3, max_tokens: int = 1000) -> None:
        self.temperature = temperature
        self.max_tokens = str(max_tokens)
        self.messages: list[dict[str, str]] = [
            {
                "role": "system",
                "text": LLM_SYSTEM_PROMPT
            }
        ]

    @staticmethod
    def get_token() -> str:
        data = json.dumps({"yandexPassportOauthToken": TOKEN})
        headers = {"Content-Type": "application/json"}
        response = requests.post(TOKEN_URL, data=data, headers=headers)
        return response.json()['iamToken']

    def get_answer(self, user_message) -> str:
        self.messages += [
            {
                "role": "user",
                "text": user_message
            }
        ]
        body = {
            "modelUri": f"gpt://{LLM_FOLDER}/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "temperature": self.temperature,
                "maxTokens": self.max_tokens
            },
            "messages": self.messages
        }

        response = requests.post(
            LLM_URL,
            data=json.dumps(body),
            headers={
                "Authorization": f"Bearer {self.get_token()}",
                "Content-Type": "application/json"
            }
        )

        response_text = response.json()['result']['alternatives'][0]['message']['text']

        self.messages += [
            {
                "role": "assistant",
                "text": response_text
            }
        ]

        return response_text
