#!/usr/bin/env python3
from setuptools import find_packages, setup


with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
    name='baconify',
    version='0.0.1',
    author='Ivana Kellyerova',
    author_email='ivana.kellyerova@bacon.amarion.net',
    description='Fill your screen with bacon!',
    url='https://gitlab.com/jenx/bacon/',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    keywords=[
        'image',
        'generator',
        'bacon',
    ],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Artistic Software',
        'Topic :: Multimedia :: Graphics',
    ],
    install_requires=[
        'PySide2>=5.12.2',
    ],
)
