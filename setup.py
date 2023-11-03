import os
from distutils.core import setup

from setuptools import find_packages


def readme():
    readme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')
    with open(readme_path) as fobj:
        return fobj.read()


def requirements():
    requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')
    with open(requirements_path) as fobj:
        return [line.strip('\n') for line in fobj.readlines()]


setup(
    name='semantic_ai',
    version='1.0.0',
    description='Sematic AI RAG System',
    long_description=readme(),
    author='DecisionFacts',
    author_email='info@decisionfacts.io',
    license='MIT',
    packages=find_packages(exclude=('dhl',)),
    include_package_data=True,
    install_requires=requirements()
)
