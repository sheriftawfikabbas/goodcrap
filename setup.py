from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).resolve().parent
README = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='goodcrap',
    packages=['goodcrap',
              ] + find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    entry_points={
        "console_scripts": ["goodcrap=goodcrap.cli:execute_cli"],
    },
    version='0.1.2',
    license='gpl-3.0',
    description='goodcrap generates controlled random data.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Sherif Abdulkader Tawfik Abbas',
    author_email='sherif.tawfic@gmail.com',
    url='https://github.com/goodcrap/goodcrap',
    keywords=['ai', 'data engineering', 'fake data',
              'data science'],
    install_requires=['sqlalchemy','faker','pandas','numpy'],

)
