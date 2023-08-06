import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

requires = [
    "requests",
]


setup(
    name="distlock-client",
    version="0.1.1",
    description="Distribute lock system's client.",
    long_description=long_description,
    url="https://github.com/appstore-zencore/distlock-client",
    author="zencore",
    author_email="appstore@zencore.cn",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords=['distlock-client', 'distlock'],
    requires=requires,
    install_requires=requires,
    packages=find_packages("."),
    py_modules=["distlock_client"],
)