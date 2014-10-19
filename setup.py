try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Python implementation of osbash',
    'author': 'Pranav Salunke',
    'url': 'https://github.com/dguitarbite/stacktrain',
    'download_url': 'n/a',
    'author_email': 'dguitarbite@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['stacktrain'],
    'scripts': [],
    'name': 'stacktrain'
}

setup(**config)

