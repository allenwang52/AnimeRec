# MyAnimeList API
import json
import requests
import secrets

CLIENT_ID = ""
CLIENT_SECRET = ""

def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]

def print_new_authorization_url(code_challenge: str):
    global CLIENT_ID

    url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={CLIENT_ID}&code_challenge={code_challenge}'
    print(f'Authorize your application by clicken here: {url}\n')

def generate_new_token(authorization_code: str, code_verifier: str) -> dict:
    global CLIENT_ID, CLIENT_SECRET

    url = 'https://myanimelist.net/v1/oauth2/token'
