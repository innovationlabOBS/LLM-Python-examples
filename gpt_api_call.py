import os
import sys
import numpy as np
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
        sys.stdout.write(token)
        sys.stdout.flush()
        yield token

def gpt_api_call(prompt):

    full_response = ""
    for token in gpt_api_call_stream(prompt=prompt):
        full_response += token
    
    return full_response

def get_embedding(text, model="text-embedding-3-small"):
    return client.embeddings.create(input = [text], model=model).data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))