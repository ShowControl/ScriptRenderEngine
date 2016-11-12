try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Script Render Engine',
    'author': 'bapril',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'My email.',
    'version': '0.0.3',
    'install_requires': ['nose'],
    'packages': ['script_render_engine'],
    'scripts': [],
    'name': 'script_render_engine'
}

setup(**config)
