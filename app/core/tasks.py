from celery import shared_task

import requests
import re
from datetime import datetime
from .models import Recipe
from bs4 import BeautifulSoup

URL = 'https://www.10000recipe.com/recipe'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Whale/3.18.154.7 Safari/537.36'}


@shared_task
def get_recipe_url(urls):
    result = []
    for url in urls:
        response = requests.get(url)
        res = parse_list(response.text)
        result += res

    return {'result': result}


@shared_task
def get_recipe(indexes):
    result = []
    for index in indexes:
        response = requests.get(f"{URL}/{index}", headers=headers)
        res = parse_recipe(response.text)
        if not res:
            continue
        res.update({'index': index})
        result.append(res)
    return {'result': result}


@shared_task
def save_recipe(result):
    results = result['result']
    for res in results:
        recipe = Recipe.objects.create(
            index=res['index'], title=res['title'], ingredients=res['ingredients'])
        recipe.save()


def parse_recipe(html):
    soup = BeautifulSoup(html, "html.parser")
    p = re.compile('[a-zA-Zㄱ-힗]')
    try:
        title = soup.find('div', class_='view2_summary').find('h3').text
        ingredients_html = soup.find(
            'div', class_='ready_ingre3').find_all('li')
        ingredients = []
        for ingredient in ingredients_html:

            tmp = ingredient.get_text().replace('\n', '').replace(
                ' ', '').replace('구매', ',').split(',')
            name = tmp[0]
            if len(tmp) > 1:
                unit = re.sub('[^a-zA-Zㄱ-힗]', '', tmp[1])
                number = re.sub('[^0-9/.]', '', tmp[1])
                ingredients.append(
                    {'name': name, 'number': number, 'unit': unit})
            ingredients.append({'name': name, 'number': '0', 'unit': ''})
        return {'title': title, 'ingredients': ingredients}
    except AttributeError:
        pass


def parse_list(html):
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all('a', class_='common_sp_link')
    indexes = [result.attrs['href'].split('/')[-1] for result in results]

    return indexes
