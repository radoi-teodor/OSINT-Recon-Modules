# Recon NG module to convert a web domain to an IP address

import socket

from recon.core.module import BaseModule

class Module(BaseModule):
    meta = {
        'author': 'John Doe',
        'version': '1.0',
        'dependencies': ['socket'],
        'options': (
            ('domain', 'google.com', True, 'Web domain to convert to an IP address'),
        )
    }

    def run(self):
        # get the domain from the options
        domain = self.options['domain']

        # convert the domain to an IP address
        ip_address = socket.gethostbyname(domain)

        # add the IP address to the report
        self.output(ip_address)


