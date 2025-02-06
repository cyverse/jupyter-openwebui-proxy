import os
import logging
from urllib.parse import urlparse, urlunparse

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

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

def rewrite_paths(response):
    '''
       open-webui doesn't support changing its base url. So, we'll need to rewrite paths
       in the extension itself
    '''
    logger.info('rewrite_paths() start')

    response.body = response.body.replace(b'/_app/', b'/openwebui/_app/')
    response.body = response.body.replace(b'/favicon/', b'/openwebui/favicon/')
    response.body = response.body.replace(b'/opensearch.xml', b'/openwebui/opensearch.xml')
    response.body = response.body.replace(b'/static/', b'/openwebui/static/')

    # for header, v in response.headers.get_all():
    #     if header == "Location":
    #         logger.info('rewrite_paths() Location: ' + v)
    #         u = urlparse(v)
    #         if u.netloc != request.host:
    #             response.headers[header] = urlunparse(u._replace(netloc=request.host))


    #         if v.startswith("/_app") or v.startswith("/static"):
    #             # Visit the correct page
    #             response.headers[header] = request.uri + v

    logger.info('rewrite_paths() end')

def setup_openwebui():
    """ Setup commands and and return a dictionary compatible
        with jupyter-server-proxy.
    """

    # create command
    openwebui_bin = get_openwebui_bin('open-webui')
    logger.info('open-webui path: ' + ' '.join(openwebui_bin))

    bash_cmd = "/usr/bin/bash -c \"{} serve\" &".format(openwebui_bin)
    logger.info('bash cmd: ' + ' '.join(bash_cmd))

    cmd = ["/usr/bin/nohup", openwebui_bin, "serve"]
    logger.info('open-webui command: ' + ' '.join(cmd))

    return {
        'command': cmd,
        'timeout': 30,
        'port': 8080,
        'absolute_url': False,
        'rewrite_response': rewrite_paths,
        'mappath': {
            '/_app/': '/openwebui/_app/',
            '/static/': '/openwebui/static/',
            '/favicon/': '/openwebui/static/',
            '/opensearch.xml': '/openwebui/opensearch.xml'
        },
        'launcher_entry': {
            'enabled': True,
            'icon_path': os.path.join(HERE, 'icons', 'openwebui.svg'),
            'title': 'Open WebUI',
        },
        # 'progressive': True,
    }
