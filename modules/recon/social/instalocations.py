from recon.core.module import BaseModule

from bs4 import BeautifulSoup
import requests

class Module(BaseModule):
    name = "Instagram Account Search and Location Retrieval"
    description = "Searches for Instagram accounts based on a full name and retrieves the latest locations of their posts."
    meta = {
        'author': 'John Doe',
        'version': '1.0',
        'dependencies': ['requests', 'bs4'],
        'options': (
            ('SOURCE', 'john doe', True, 'Full name to search for Instagram accounts'),
            ('max_results', '10', True, 'Maximum number of Instagram accounts to retrieve'),
        )
    }

    def run(self):
        # get the full name and max_results from the options
        full_name = self.options['SOURCE']
        max_results = int(self.options['max_results'])

        # search for Instagram accounts based on the full name
        instagram_url = f"https://www.instagram.com/web/search/topsearch/?context=blended&query={full_name}"
        response = requests.get(instagram_url).json()

        if 'users' not in response.keys():
            self.output('Limit exceeded')
            return

        accounts = response['users']

        # retrieve the latest locations of the posts made by each account
        for account in accounts[:max_results]:
            username = account['user']['username']
            user_id = account['user']['pk']

            # get the account's posts
            posts_url = f"https://www.instagram.com/{username}/"
            response = requests.get(posts_url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            # check if the account is private
            private_account = soup.find('div', {'class': '_8-yf5 '})
            if private_account:
                continue

            # find the latest post with a location
            for div in soup.find_all('div', {'class': 'v1Nh3 kIKUG  _bz0w'}):
                if div.find('a', {'class': '_A5uQ'}):
                    location_name = div.find('a', {'class': '_A5uQ'}).text
                    location_id = div.find('a', {'class': '_A5uQ'})['href'].split('/')[-2]

                    # add the username, user_id, location_id, and location_name to the report
                    self.output('username', username)
                    self.output('user_id', user_id)
                    self.output('location_id', location_id)
                   

