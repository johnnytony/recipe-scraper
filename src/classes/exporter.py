import requests
from bs4 import BeautifulSoup

class Exporter:
    def __init__(self):
        self.name = "Sabor Intenso"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.accepted_catalogs = [
            {'name': 'caderno-1', 'description': 'Carne'}, 
            {'name': 'caderno-9', 'description': 'Peixe'}, 
         ]

    def export_data(self):
        # Headers to mimic a browser request (prevents 403 Forbidden errors)
     
        
        # Get the HTML content
        response = requests.get('https://www.saborintenso.com/', headers=self.headers)
        response.raise_for_status()  # Raises an error if request failed
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'lxml')
        
      
        # Find a div with id="container"
        link_divs = soup.find('div', id='container').find_all('p', class_='micro')
        
        if not link_divs:
            return None

        # Extract links and filter by accepted catalogs
        accepted_names = {catalog['name'] for catalog in self.accepted_catalogs}
        links_data = []
        for div in link_divs:
            link = div.find('a', href=True)

            if link:
                href = link.get('href')
                catalog = href[:-1].split('/')[-1]

                if catalog in accepted_names:
                    links_data.append({
                        'href': href,
                        'text': link.get_text(strip=True),
                        'catalog': catalog,
                        'full_link': link
                    })
        
        import pdb
        pdb.set_trace()
        
        return links_data if links_data else None