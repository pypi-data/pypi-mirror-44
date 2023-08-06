from setuptools import setup

setup(
    name='micropython-display',
    version='1.14',
    packages=['display', 'display.fonts', 'display.examples'],
    #package_dir = {'djangoforandroid': 'djangoforandroid'},

    author='Yeison Cardona',
    author_email='yeisoneng@gmail.com',
    maintainer='Yeison Cardona',
    maintainer_email='yeisoneng@gmail.com',

    url='http://yeisoncardona.com/',
    download_url='https://bitbucket.org/espressoide/micropython-display/downloads/',

    install_requires=[],

    license='GNU GPL',
    description="Micropython scripts for use displays.",
    #    long_description = README,

    classifiers=[
        # 'Environment :: Web Environment',
        # 'Framework :: Django',
    ],

)
