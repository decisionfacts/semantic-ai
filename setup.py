import os
from distutils.core import setup

from setuptools import find_packages


def readme():
    readme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')
    with open(readme_path) as fobj:
        return fobj.read()


def requirements():
    # requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'requirements.txt')
    # with open(requirements_path) as fobj:
    #     return [line.strip('\n') for line in fobj.readlines()]
    return [
        "langchain==0.0.310",
        "sentence-transformers==2.2.2",
        "df-extract==0.0.2.1",
        "boto3~=1.21.20",
        "elasticsearch==8.8.2",
        "qdrant-client==1.3.2",
        "jq==1.6.0",
        "httpx==0.25.0",
        "pydantic==2.4.2",
        "pydantic-settings==2.0.3"
    ]


setup(
    name='semantic_ai',
    version='v0.0.1',
    description='Sematic AI RAG System',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='DecisionFacts',
    author_email='info@decisionfacts.io',
    maintainer='DecisionFacts',
    maintainer_email='info@decisionfacts.io',
    license='MIT',
    url='https://github.com/decisionfacts/semantic-ai',
    download_url='https://github.com/decisionfacts/semantic-ai.git',
    keywords=['pdf machine-learning ocr deep-neural-networks openai docx approximate-nearest-neighbor-search '
              'semantic-search document-parser rag fastapi vector-database inference-api openai-api llm'
              ' retrieval-augmented-generation llama2 '],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements()
)
