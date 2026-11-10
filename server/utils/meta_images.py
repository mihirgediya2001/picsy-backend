import requests
import json


def generate_image(prompt: str):
    params = {
        "prompt": prompt,
    }
    headers = {
    'accept': 'application/json',
}
    response = requests.post('https://meta-image-generation.vercel.app/generate_image', params=params, headers=headers)
    print(response.text)
    return json.loads(response.text)
