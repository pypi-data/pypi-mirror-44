import setuptools

setuptools.setup(
    name='btrade_api_client',
    version='0.2.6',
    author='Niels Draaisma',
    author_email='ndraaisma@btrade.io',
    description='BTrade API client',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://bitbucket.org/bittradeaustralia/btrade-api-client/src/master/',
    packages=setuptools.find_packages(),
    install_requires=['pygments',"requests"],
    download_url='https://bitbucket.org/bittradeaustralia/btrade-api-client/get/master.zip',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Intended Audience :: Developers'
    ],
    project_urls={
        'API Documentation': 'https://btrade.io/api/',
    },
)
