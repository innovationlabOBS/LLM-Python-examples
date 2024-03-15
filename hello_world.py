import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gpt_api_call_stream(prompt):
    model_params = {
            "model": "gpt-4-0125-preview",
            "messages": [{"role": "system", "content": prompt}],
            "max_tokens": 2048,
            "temperature": 0.0,
            "top_p": 1,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "stream": True
        }
    response = client.chat.completions.create(**model_params)

    for chunk in response:
        token = chunk.choices[0].delta.content or ""
        yield token

if __name__ == "__main__":
    prompt = "Hello, world!"

    gpt_response = ""
    for token in gpt_api_call_stream(prompt):
        gpt_response += token

    print(gpt_response)