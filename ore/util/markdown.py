import requests


def compile(text):
    return requests.post('http://localhost:3001/markdown-it', json={'input': text}).text
