import requests

def process_get(server_url):
    r = requests.get(server_url)
    return r.json()

def process_post(content, server_url):
    r = requests.post(
        server_url,
        data=content,
        timeout=8000
    )

    return r.json()