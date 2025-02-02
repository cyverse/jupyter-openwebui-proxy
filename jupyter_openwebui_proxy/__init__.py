import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel('INFO')

HERE = os.path.dirname(os.path.abspath(__file__))

def get_openwebui_bin(prog):
    from shutil import which

    # Find prog in known locations
    other_paths = [
        os.path.join('/opt/conda/bin', prog),
    ]

    for op in other_paths:
        if os.path.exists(op):
            return op

    raise FileNotFoundError(f'Could not find {prog} in PATH')


def setup_openwebui():
    """ Setup commands and and return a dictionary compatible
        with jupyter-server-proxy.
    """

    # create command
    openwebui_bin = get_openwebui_bin('open-webui')
    logger.info('open-webui path: ' + ' '.join(openwebui_bin))

    bash_cmd = "/usr/bin/bash -c \"{} serve\" &".format(openwebui_bin)
    logger.info('bash cmd: ' + ' '.join(bash_cmd))

    cmd = [openwebui_bin, "serve"]
    logger.info('open-webui command: ' + ' '.join(cmd))

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
