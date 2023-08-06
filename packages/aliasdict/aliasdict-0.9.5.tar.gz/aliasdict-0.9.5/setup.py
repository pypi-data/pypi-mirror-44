from setuptools import setup
import os

version = "0.9.5"

def write_version():
    with open(os.path.join("aliasdict", "version.py"), 'w') as fp:
        fp.write("version='{VERSION}'".format(VERSION=version))

write_version()
readme = open('README.rst').read()

setup(
    name="aliasdict",
    version=version,
    author="yokoshin",
    author_email=os.environ.get('PYPI_EMAIL'),
    url='https://bitbucket.org/yokoshin/aliasdict',
    description='a dict that supports alias of KEY',
    long_description=readme,
    packages=['aliasdict', ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

    ],
)
