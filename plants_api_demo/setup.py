from setuptools import setup, find_packages

setup(
    name='plants_api_demo',
    version='1.0.0',
    description='plants for a RESTful API based on Flask-RESTPlus',
    url='https://github.com/postrational/rest_api_demo',
    author='MESRAR mohamed',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.8.5',
    ],

    keywords='rest restful api flask swagger openapi flask-restplus',

    packages=find_packages(),

    install_requires=['flask-restx==0.2.0'],
)
