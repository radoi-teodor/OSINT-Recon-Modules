from recon.core.module import BaseModule
import requests
from bs4 import BeautifulSoup

class Module(BaseModule):
    # define meta information for the module
    meta = {
        'name': 'Facebook Locations Module',
        'author': 'Your Name',
        'version': '1.0',
        'description': 'This module retrieves the latest locations of a Facebook user based on their posts.',
        'options': (
            ('user_id', None, True, 'the ID of the Facebook user'),
            ('max_results', 10, False, 'the maximum number of locations to retrieve'),
        ),
    }

    def run(self):
        # get the user ID and max_results from the options
        user_id = self.options['user_id']
        max_results = int(self.options['max_results'])

        # set the URL of the user's profile page
        profile_url = f"https://www.facebook.com/{user_id}"

        # send a request to the profile page and retrieve the response
        response = requests.get(profile_url)
        html = response.text

        # parse the HTML of the profile page
        soup = BeautifulSoup(html, 'html.parser')

        # retrieve the latest posts from the profile page
        posts = soup.find_all('div', {'class': '_5pcr userContentWrapper'})[:max_results]

        # loop through the posts
        for post in posts:
            # check if the post has a location
            location_element = post.find('a', {'class': '_5pcq'})
            if location_element:
                # retrieve the location name and URL from the post
                location_name = location_element.text
                location_url = location_element['href']

                # add the location name and URL to the report
                self.output('location_name', location_name)
                self.output('location_url', location_url)
