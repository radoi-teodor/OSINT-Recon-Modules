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
            ('SOURCE', 'acme inc', True, 'Name of the company to search for articles'),
            ('max_results', '100', True, 'Maximum number of articles to retrieve'),
        )
    }

    def run(self):
        # get the company name and max_results from the options
        company_name = self.options['SOURCE']
        max_results = int(self.options['max_results'])

        # set the user agent to the user agent string of a web browser
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
		   'Cookie':'CONSENT=YES+cb.20210418-17-p0.it+FX+917; '}

        more_results = True
        page_size = 10
        start=0

        while more_results:
            # search for articles about the company using the requests library
            google_url = f"https://www.google.com/search?q={company_name}&tbm=nws&start={start}"
            response = requests.get(google_url, headers=headers)
            html = response.text
            
            # parse the HTML of the search results page
            soup = BeautifulSoup(html, 'html.parser')

            # retrieve the title and URL of each article
            for a in soup.find_all('a', {'class': 'WlydOe'})[:max_results]:
                title = a.find(class_='mCBkyc').text
                url = a.get('href')

                # add the title and URL to the report
                self.output('title: '+str(title))
                self.output('url: '+(url))
            next_button = soup.find('a', {'id': 'pnnext'})
            
            if not next_button or start>max_results:
                more_results = False
            else:
                start+=page_size
