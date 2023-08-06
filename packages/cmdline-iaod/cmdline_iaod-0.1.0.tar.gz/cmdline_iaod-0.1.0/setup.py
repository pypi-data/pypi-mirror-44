# setup.py

from setuptools import setup

setup(
    name = 'cmdline_iaod',
    version = '0.1.0',
    description = 'Makes database of intron annotation information',
    long_description = open('README.txt', 'r').read(),
    author = 'Devlin Moyer',
    author_email = 'devmoy@gmail.com',
    packages = ['cmdline_iaod'],
    install_requires = ['argparse'],
    license = 'MIT',
    scripts = ['scripts/search_functions.py'],
    keywords = ['U12-dependent introns', 'genomics', 'RNA-splicing']
)
