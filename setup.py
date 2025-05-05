# setup.py – Package definition for `pip install .`

from setuptools import setup, find_packages

setup(
    name='scraper_gui',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'selenium',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'scraper-gui=main:main',
        ],
    },
    author='Your Name',
    description='A desktop GUI tool to scrape AI product data with Selenium and Chrome',
)