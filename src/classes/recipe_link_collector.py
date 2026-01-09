import requests
from bs4 import BeautifulSoup

from src.utils import get_headers

class RecipeLinkCollector:
    def __init__(self):
        self.name = "Sabor Intenso"
        self.headers = get_headers()
        self.accepted_catalogs = [
            {'name': 'caderno-1', 'description': 'Carne'}, 
            {'name': 'caderno-9', 'description': 'Peixe'}, 
        ]

        # Retrieve all existing links
        self.exported_links = self.export_initial_data()

        # Check if they correspond to the expected format
        # TODO Create a pydantic structure to simplify and validate the expected schema
        self._check_data_integrity(self.exported_links)


    def _check_data_integrity(self, exported_links):
        for catalog in self.accepted_catalogs:
            if catalog['name'] not in [link['catalog'] for link in exported_links]:
                raise Exception(f'There is data differencies. Website might have changed! catalog{self.accepted_catalogs} != {[link['catalog'] for link in exported_links] }')

    def _retrieve_accepted_links(self, exported_links):
        links = []
        for catalog in self.accepted_catalogs:
            for link in exported_links:
                if catalog['name'] == link['catalog']:
                    links.append(link)
        return links

    def export_initial_data(self): 
        # Get the HTML content
        response = requests.get('https://www.saborintenso.com/', headers=self.headers)
        response.raise_for_status()  # Raises an error if request failed
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'lxml')
      
        # Find a div with id="container"
        link_divs = soup.find('div', id='container').find_all('p', class_='micro')
        
        if not link_divs:
            return None

        links_data = []
        for div in link_divs:
            link = div.find('a', href=True)

            if link:
                href = link.get('href')
                catalog = href[:-1].split('/')[-1]

                links_data.append({
                    'href': href,
                    'text': link.get_text(strip=True),
                    'catalog': catalog,
                    'full_link': link
                })
        
        return links_data if links_data else None

    def get_all_recipes_links(self):
        links_list = []
        status_code = 200

        for link in self._retrieve_accepted_links(self.exported_links):
            page = 0
            print(f'Retrieving data for {link}')
            while(status_code == 200):
                page += 1

                url = f'{link['href']}&ver=tudo&page={page}'

                response = requests.get(url, headers=self.headers)
                status_code = response.status_code
                response.raise_for_status()  # Raises an error if request failed

                # Parse the HTML
                soup = BeautifulSoup(response.content, 'lxml')

                recipes = soup.find('div', id='container').find_all('div', class_='sombra_pub sobre')

                current_link_list = []
                
                for recipe_info in recipes:
                    link_info = {}

                    if 'Neuza Costa' in str(recipe_info):
                        recipe_link = recipe_info.find('a', href=True)

                        link_info['url'] = recipe_link.get('href')
                        link_info['metadata'] = link         

                        current_link_list.append(link_info)
                links_list.extend(current_link_list)

                if len(current_link_list) != len(recipes):
                    print('There are recipes that are not from Neuza Costa')
                    print(f'Page -> {page}')
                    break

        return links_list
