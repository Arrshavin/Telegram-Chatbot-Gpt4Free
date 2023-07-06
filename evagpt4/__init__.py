import aiohttp
import asyncio
import json

class Model:
    def __init__(self):
        self.url = "https://ava-alpha-api.codelink.io/api/chat"
        self.headers = {
            "content-type": "application/json"
        }
        self.payload = {
            "model": "gpt-4",
            "temperature": 0.6,
            "stream": True
        }
        self.accumulated_content = ""

    async def _process_line(self, line):
        line_text = line.decode("utf-8").strip()
        if line_text.startswith("data:"):
            data = line_text[len("data:"):]
        try:
            data_json = json.loads(data)
            choices = data_json.get("choices", [])
            for choice in choices:
                if choice.get("finish_reason") == "stop":
                    break
                delta = choice.get("delta", {})
                content = delta.get("content")
                if content:
                    self.accumulated_content += content
        except json.JSONDecodeError:
            pass

    async def ChatCompletion(self, messages):
        self.payload["messages"] = messages

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, data=json.dumps(self.payload)) as response:
                self.accumulated_content = await response.text()

        return self.accumulated_content
