# Note: Needs to be in this directory for the proper asgi import

# ==============================================================================
# Logging Setup
# ==============================================================================

import logging
import os
import sys

# Ensure tabbycat directory is on Python path
tabbycat_dir = os.path.dirname(os.path.abspath(__file__))
if tabbycat_dir not in sys.path:
    sys.path.insert(0, tabbycat_dir)

root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

import asgi # noqa: E402
from daphne.endpoints import build_endpoint_description_strings # noqa: E402
from daphne.server import Server # noqa: E402

# Docker/Heroku environments use NGINX and must bind to a socket; others bind to address
if 'USING_NGINX' in os.environ and bool(int(os.environ['USING_NGINX'])):
    root.info('TC_DEPLOY: Initialising Daphne with NGINX')
    Server(
        application=asgi.application,
        endpoints=build_endpoint_description_strings(
            unix_socket="/tmp/asgi.socket",
        ),
        ping_interval=15,
        ping_timeout=30,
        websocket_timeout=10800, # 3 hours maximum length
        websocket_connect_timeout=10,
        application_close_timeout=10,
        verbosity=2,
        proxy_forwarded_address_header="X-Forwarded-For",
        proxy_forwarded_port_header="X-Forwarded-Port",
        proxy_forwarded_proto_header="X-Forwarded-Proto",
    ).run()
else:
    port = os.environ.get('PORT', '8000')
    root.info(f'TC_DEPLOY: Initialising Daphne on 0.0.0.0:{port}')
    Server(
        application=asgi.application,
        endpoints=build_endpoint_description_strings(
            host="0.0.0.0",
            port=str(port),
        ),
        ping_interval=15,
        ping_timeout=30,
        websocket_timeout=10800, # 3 hours maximum length
        websocket_connect_timeout=10,
        application_close_timeout=10,
        verbosity=2,
        proxy_forwarded_address_header="X-Forwarded-For",
        proxy_forwarded_port_header="X-Forwarded-Port",
        proxy_forwarded_proto_header="X-Forwarded-Proto",
    ).run()
