
import re

import setuptools


def read_file(path):
    with open(path, 'r') as handle:
        return handle.read()


def read_version():
    try:
        s = read_file('VERSION')
        m = re.match(r'v(\d+\.\d+\.\d+)', s)
        return m.group(1)
    except FileNotFoundError:
        return "0.0.0"


long_description = read_file('README.md')
version = read_version()

setuptools.setup(
    name='oxomo',
    description="""
    Python logging handler that sends messages to HTTPS endpoints.""",
    keywords="logging handler https",
    long_description=long_description,
    include_package_data=True,
    version=version,
    url='https://gitlab.com/greenhousegroup/ai/libraries/oxomo/',
    author='Greenhouse AI team',
    author_email='ai@greenhousegroup.com',
    package_dir={'oxomo': 'src/oxomo'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ],
    install_requires=["requests-futures >= 0.9.9"],
    data_files=[('.', ['VERSION'])],
    setup_requires=['pytest-runner'],
    tests_require=["pytest>=4", "mock>=2.0.0"],
    packages=setuptools.find_packages('src'))

# #!/usr/bin/env python

# from setuptools import setup, find_packages

# setup(
#     name="oxomo",
#     version='0.1.0',
#     description=""""""
#     author="gerard.witvliet",
#     url="https://gitlab.com/gerard.witvliet/https-python-handler/",
#     license="MIT",
#     packages=find_packages(),
#     install_requires=[
#     ],
#     include_package_data=True,
#     platform='any',
#     classifiers=[
#         'Development Status :: 4 - Beta', 'Intended Audience :: Developers'
#     ])
