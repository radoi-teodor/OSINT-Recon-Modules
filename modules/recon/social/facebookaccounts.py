from recon.core.module import BaseModule
import requests

class Module(BaseModule):
    # define meta information for the module
    meta = {
        'name': 'Facebook Account Search Module',
        'author': 'Your Name',
        'version': '1.0',
        'description': 'This module searches for Facebook accounts based on a person\'s full name.',
        'required_keys': ['facebook_access_token'],
        'options': (
            ('name', None, True, 'the full name of the person to search for'),
        ),
    }

    def run(self):
        # get the name from the options
        name = self.options['name']

        # get the Facebook access token from the keys
        access_token = self.keys['facebook_access_token']

        # set the API endpoint for searching for users
        endpoint = 'https://graph.facebook.com/v9.0/search'

        # set the parameters for the API request
        params = {
            'access_token': access_token,
            'type': 'user',
            'q': name,
            'fields': 'id,name',
            'limit': 10,
        }

        # send the API request and retrieve the response
        response = requests.get(endpoint, params=params)
        data = response.json()

        # loop through the users in the response
        for user in data['data']:
            # retrieve the user's name and ID
            user_name = user['name']
            user_id = user['id']

            # add the user's name and ID to the report
            self.output('name', user_name)
            self.output('id', user_id)
