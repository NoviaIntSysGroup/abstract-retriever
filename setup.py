from setuptools import setup, find_packages

setup(
    name='abstract_retriever',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4==4.10.0',
        'requests==2.26.0',
        'pytest',
        'python-dotenv',
        'pyppeteer',
        'pyppeteer_stealth',
        'pytest-asyncio'
    ],
)