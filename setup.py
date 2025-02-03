# setup.py
from setuptools import setup, find_packages

setup(
    name='git-text-tree',
    version='0.1.0',
    py_modules=['git_text_tree'],
    install_requires=[
        'pathspec'
    ],
    entry_points={
        'console_scripts': [
            'git-text-tree=git_text_tree:main',
        ],
    },
)
