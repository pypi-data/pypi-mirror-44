import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def requirements(fname):
    return [line.strip() for line in open(os.path.join(os.path.dirname(__file__), fname))]


setup(
    name="git-word-blame",
    version="0.0.4",
    author="Damien",
    author_email="damien@dam.io",
    description="word-by-word blame for git",
    url="https://framagit.org/mdamien/git-word-blame/",
    license="GPLv3",
    packages=find_packages(),
    # entry_points={
    #     'console_scripts': [
    #         'git-word-blame=git-word-blame:main'
    #     ],
    # },
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    install_requires=requirements("requirements.txt"),
    setup_requires=[],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    scripts=[
        'bin/git-word-blame',
    ],
)