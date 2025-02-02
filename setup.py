from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.md'), 'r', encoding = 'utf-8') as fh:
    long_description = fh.read()

version='0.0.1'
setup(
    name = 'cyverse-jupyter-openwebui-proxy',
    version = version,
    packages = find_packages(),

    url = 'https://github.com/cyverse/jupyter-openwebui-proxy',
    download_url = 'https://github.com/cyverse/jupyter-openwebui-proxy/archive/refs/heads/main.zip'.format(version),

    author = 'Edwin Skidmore',
    author_email = 'edwins@arizona.edu',

    description = 'CyVerse extension for Open WebUI for Jupyter',
    long_description = long_description,
    long_description_content_type = 'text/markdown',

    keywords = ['cyverse','jupyter', 'openwebui', 'jupyterhub', 'jupyter-server-proxy'],
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Framework :: Jupyter',
    ],

    entry_points = {
        'jupyter_serverproxy_servers': [
            'openwebui = jupyter_openwebui_proxy:setup_openwebui',
        ]
    },
    python_requires = '>=3.6',
    install_requires=[
        'jupyter-server-proxy>=4.0.0',
        'tornado>=6.3'
    ],
    include_package_data = True,
    zip_safe = False
)
