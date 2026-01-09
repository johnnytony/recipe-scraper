import requests
from bs4 import BeautifulSoup

from src.utils import get_headers

class RecipeInfoExporter():
    def __init__(self, recipes_links):
        self.recipes_links = recipes_links
        self.headers = get_headers()

    def export_recipes_info(self):
        for link in self.recipes_links:
            response = requests.get(link['url'], headers=self.headers)
            response.raise_for_status

            # Parse the HTML
            soup = BeautifulSoup(response.content, 'lxml')

            recipe_info = soup.find('div', class_='topico')

            name = recipe_info.find('b').find('font').get_text()[20:]

            ingredients = recipe_info.find('ul').find_all('li')
            ingridients_description = [ingredient.get_text() for ingredient in ingredients]

            # preparation = 


            import pdb
            pdb.set_trace()