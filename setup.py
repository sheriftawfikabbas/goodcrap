from setuptools import setup, find_packages

setup(
    name='goodcrap',
    packages=['goodcrap',
              ] + find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    entry_points={
        "console_scripts": ["goodcrap=goodcrap.cli:execute_cli"],
    },
    version='0.1.0',
    license='gpl-3.0',
    description='goodcrap generates controlled random data.',
    author='Sherif Abdulkader Tawfik Abbas',
    author_email='sherif.tawfic@gmail.com',
    url='https://github.com/goodcrap/goodcrap',
    keywords=['ai', 'data engineering', 'fake data',
              'data science'],
    install_requires=['sqlalchemy','faker'],

)
