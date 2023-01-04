from recon.core.module import BaseModule

import requests
from bs4 import BeautifulSoup

class Module(BaseModule):
    name = "Company Article Search"
    description = "Searches for articles about a given company on the internet."
    meta = {
        'author': 'John Doe',
        'version': '1.0',
        'dependencies': ['requests', 'bs4'],
        'options': (
            ('company_name', 'acme inc', True, 'Name of the company to search for articles'),
            ('max_results', '10', True, 'Maximum number of articles to retrieve'),
        )
    }

    def run(self):
        # get the company name and max_results from the options
        company_name = self.options['company_name']
        max_results = int(self.options['max_results'])

        # search for articles about the company
        google_url = f"https://www.google.com/search?q={company_name}&tbm=nws"
        response = requests.get(google_url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # retrieve the title and URL of each article
        for h3 in soup.find_all('h3', {'class': 'r'})[:max_results]:
            title = h3.text
            url = h3.find('a')['href']

            # add the title and URL to the report
            self.output('title', title)
            self.output('url', url)
