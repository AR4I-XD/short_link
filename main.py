import os
import requests
import json
from urllib.parse import urlparse
import argparse


def shorten_link(user_token, url):
    payload = {
        "url": user_url,
        "private": 0,
        "access_token": user_token,
        "v": "5.199"
    }
    url = 'https://api.vk.ru/method/utils.getShortLink'
    response = requests.get(url, params=payload)
    response.raise_for_status()
    short_link = response.json()['response']['short_url']

    return short_link


def count_clicks(user_token, short_link):
    url = 'https://api.vk.ru/method/utils.getLinkStats'
    parsed = urlparse(short_link)
    payload = {
        "key": parsed.path[1:],
        "access_token": user_token,
        "interval" : "forever",
        "extended": 0,
        "v": "5.199"
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    link_info = response.json()['response']['stats']
    return link_info


def is_shorten_link(user_url, user_token, short_link):
    url = 'https://api.vk.ru/method/utils.getLinkStats'
    parsed = urlparse(short_link)
    payload = {
        "key": parsed.path[1:],
        "access_token": user_token,
        "interval" : "forever",
        "extended": 0,
        "v": "5.199"
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    try:
        response.json()['response']['stats']
        return True
    except:
        return False
   

if __name__ == "__main__":
    vk_token = os.getenv["VK_TOKEN"]
    
    parser = argparse.ArgumentParser(description='Сокращает ссылки ')
    parser.add_argument('name', help='Ваша ссылка')
    args = parser.parse_args()
    user_url = args.name
    
    if is_shorten_link(user_url, vk_token, user_url):
        try:
            if len(count_clicks(vk_token, user_url)) == 0:
                print("По ссылке ещё не преходили")
            elif count_clicks(vk_token, user_url)[0]['views'] > 0:
                print(f"Количество переходов по ссылке: {count_clicks(vk_token, user_url)[0]['views']}")
        except:
            print("Не прaвильный ввод или ссылке ещё не преходили")
    else:
        try:
            print(f"Сокращенная ссылка: {shorten_link(vk_token, user_url)}")
        except KeyError:
            print("Не прaвильный ввод ссылки")
        
        

