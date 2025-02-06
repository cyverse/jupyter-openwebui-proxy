import os
import logging
from urllib.parse import urlparse, urlunparse
import sys

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
    print('rewrite_paths() start', file=sys.stderr)

    # print(response.body, file=sys.stderr)

    for header, v in response.headers.get_all():
        if header == "Content-Type":
            print('rewrite_paths() Content-Type: ' + v, file=sys.stderr)
            # only replace in text/html, text/javascript, etc
            if "text" in v or "json" in v:
                response.body = response.body.replace(b'/_app/', b'/openwebui/_app/')
                response.body = response.body.replace(b'/api/', b'/openwebui/api/')
                response.body = response.body.replace(b'/auth/', b'/openwebui/auth/')
                response.body = response.body.replace(b'/assets/', b'/openwebui/assets/')
                response.body = response.body.replace(b'/favicon/', b'/openwebui/favicon/')
                response.body = response.body.replace(b'/opensearch.xml', b'/openwebui/opensearch.xml')
                response.body = response.body.replace(b'/static/', b'/openwebui/static/')
        if header == "Location":
            print('rewrite_paths() Location: ' + v, file=sys.stderr)

    #         u = urlparse(v)
    #         if u.netloc != request.host:
    #             response.headers[header] = urlunparse(u._replace(netloc=request.host))


    #         if v.startswith("/_app") or v.startswith("/static"):
    #             # Visit the correct page
    #             response.headers[header] = request.uri + v

    print('rewrite_paths() end', file=sys.stderr)

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
            '/api/': '/openwebui/api/',
            '/auth/': '/openwebui/auth/',
            '/assets/': '/openwebui/assets/',
            '/static/': '/openwebui/static/',
            '/favicon/': '/openwebui/favicon/',
            '/opensearch.xml': '/openwebui/opensearch.xml'
        },
        'launcher_entry': {
            'enabled': True,
            'icon_path': os.path.join(HERE, 'icons', 'openwebui.svg'),
            'title': 'Open WebUI',
        },
        # 'progressive': True,
    }
