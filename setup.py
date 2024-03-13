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
        "langchain==0.0.336",
        "sentence-transformers==2.2.2",
        "df-extract==0.0.2.1",
        "elasticsearch==8.8.2",
        "qdrant-client==1.4.0",
        "jq==1.4.0",
        "httpx==0.25.0",
        "pydantic==1.10.11",
        "fastapi==0.95.1",
        "auto-gptq==0.5.0",
        "openai==1.2.0",
        "uvicorn==0.22.0",
        "tiktoken==0.4.0",
        "ibm-watson-machine-learning==1.0.327",
        "langchain-experimental==0.0.24",
        "python-dotenv==1.0.0",
        "mysql-connector-python==8.3.0",
        "pyodbc==5.0.1",
        "SQLAlchemy==2.0.23"
    ]


setup(
    name='semantic_ai',
    version='v0.0.5.1',
    description='Sematic AI RAG System',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='DecisionFacts',
    author_email='info@decisionfacts.io',
    maintainer='DecisionFacts',
    maintainer_email='info@decisionfacts.io',
    license='Apache License 2.0',
    url='https://github.com/decisionfacts/semantic-ai',
    download_url='https://github.com/decisionfacts/semantic-ai.git',
    keywords=['pdf machine-learning ocr deep-neural-networks openai docx approximate-nearest-neighbor-search '
              'semantic-search document-parser rag fastapi vector-database inference-api openai-api llm'
              ' retrieval-augmented-generation llama2 '],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements(),
    entry_points={
            "console_scripts": [
                "semantic_ai=semantic_ai.main:main",
            ],
        },
)
