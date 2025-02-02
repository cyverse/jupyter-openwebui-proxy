import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel('INFO')

HERE = os.path.dirname(os.path.abspath(__file__))

def setup_openwebui():
    """ Setup commands and and return a dictionary compatible
        with jupyter-server-proxy.
    """

    # create command
    cmd = ["open-webui","serve"]

    return {
        # 'environment': {
        #     'SOME_ENV_VAR': 'somevalue',
        # },
        'command': cmd,
        'timeout': 20,
        # 'new_browser_tab': True,
        'launcher_entry': {
            'enabled': True,
            "absolute_url": False,
            'icon_path': os.path.join(HERE, 'icons', 'openwebui.svg'),
            'title': 'Open WebUI',
        },
        'progressive': True,
    }
