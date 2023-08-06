from setuptools import setup

setup(
    name='xlpus',
    packages=['xlpus'],
    author='h.a.h.',
    version='0.0.2',
    install_requires=['pandas', 'xlrd'],
    entry_points={
        'console_scripts': ['xlpus=xlpus:main']
    },
)
