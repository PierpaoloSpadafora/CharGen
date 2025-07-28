import requests
import json
from typing import Dict, List, Generator, Any


class OpenAIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def chat_completions_create(self, model: str, messages: List[Dict[str, str]], temperature: float = 0.7,
                                stream: bool = True) -> Generator[Dict[str, Any], None, None]:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream
        }

        try:
            with requests.post(f"{self.base_url}/chat/completions", headers=headers,
                               data=json.dumps(data), stream=stream) as response:
                response.raise_for_status()
                if stream:
                    for line in response.iter_lines():
                        if line:
                            decoded_line = line.decode('utf-8').lstrip('data: ')
                            if decoded_line == '[DONE]':
                                break
                            yield json.loads(decoded_line)
                else:
                    yield response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
