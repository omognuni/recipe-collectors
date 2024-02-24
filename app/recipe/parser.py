import re

from bs4 import BeautifulSoup


def parse_recipe(html):
    soup = BeautifulSoup(html, "html.parser")
    try:
        title = get_title(soup)
        ingredients = get_ing(soup)
        process = get_process(soup)
        return {"title": title, "process": process, "ingredients": ingredients}
    except AttributeError:
        pass


def parse_list(html):
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all("a", class_="common_sp_link")
    indexes = [result.attrs["href"].split("/")[-1] for result in results]

    return indexes


def get_title(soup):
    return soup.find("div", class_="view2_summary").find("h3").text


def get_ing(soup):
    ingredients_html = soup.find("div", class_="ready_ingre3").find_all("li")
    ingredients = []
    for ingredient in ingredients_html:
        tmp = (
            ingredient.get_text()
            .replace("\n", "")
            .replace(" ", "")
            .replace("구매", ",")
            .split(",")
        )
        name = tmp[0]
        if len(tmp) > 1:
            unit = re.sub("[^a-zA-Zㄱ-힗]", "", tmp[1])
            number = re.sub("[^0-9/.]", "", tmp[1])
            ingredients.append({"name": name, "number": number, "unit": unit})
        ingredients.append({"name": name})

    return ingredients


def get_process(soup):
    process_html = soup.find_all("div", "view_step_cont")
    process = ""
    for n in process_html:
        process += n.get_text().replace("\n", " ").strip(" ")
    return process
