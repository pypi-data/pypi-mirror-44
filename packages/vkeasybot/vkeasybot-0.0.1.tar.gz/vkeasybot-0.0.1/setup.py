from setuptools import setup, find_packages
from os.path import join, dirname
import vkeasybot

"""
:author: ilya001
:license: Copyright (c) 2019 The Python Packaging Authority, see LICENSE file
:copyright: (c) 2019 python273
"""

with open('README.MD', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="vkeasybot",
    version=vkeasybot.__version__,
    author="ilya001",
    author_email="ilja.sonin2018@yandex.ru",
    description=(
        "vkeasybot - модуль для работы с api Вконтакте"
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    url='https://github.com/Ilya001/vkeasybot',
    packages = ['vkeasybot'],
    install_requires=['requests'],

    license="Copyright (c) 2019 The Python Packaging Authority, see LICENSE file",
)