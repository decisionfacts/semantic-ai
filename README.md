# Semantic AI Lib

[![PyPI version](https://badge.fury.io/py/semantic-ai.svg)](https://badge.fury.io/py/semantic-ai)

An open source framework for Retrieval-Augmented  System (RAG) uses semantic search helps to retrieve the expected results and generate human readable conversational response with the help of LLM (Large Language Model).

## Requirements

Python 3.10+ asyncio

## Installation
```shell
# Using pip
$ python -m pip install semantic-ai

# Manual install
$ python -m pip install .
```
# Set the environment variable
Put the all credentials in .env file
```shell
# Default
FILE_DOWNLOAD_DIR_PATH= # default directory name 'download_file_dir'
EXTRACTED_DIR_PATH= # default directory name 'extracted_dir'

# Connector
CONNECTOR_TYPE="connector_name" # sharepoint
SHAREPOINT_CLIENT_ID="client_id"
SHAREPOINT_CLIENT_SECRET="client_secret"
SHAREPOINT_TENANT_ID="tenant_id"
SHAREPOINT_HOST_NAME='<tenant_name>.sharepoint.com'
SHAREPOINT_SCOPE='https://graph.microsoft.com/.default'
SHAREPOINT_SITE_ID="site_id"
SHAREPOINT_DRIVE_ID="drive_id"
SHAREPOINT_FOLDER_URL="folder_url" # /My_folder/child_folder/

# Indexer
INDEXER_TYPE="vector_db_name" # elasticsearch, qdrant
ELASTICSEARCH_URL="elasticsearch_url" # give valid url
ELASTICSEARCH_INDEX_NAME="index_name"
ELASTICSEARCH_SSL_VERIFY="ssl_verify" # True or False 
```
Method 1:
    To load the .env file. Env file should have the credentials
```shell
%load_ext dotenv
%dotenv
%dotenv relative/or/absolute/path/to/.env

(or)

dotenv -f .env run -- python
```
Method 2:
```python
from semantic_ai.config import Settings
settings = Settings()
```

### 1. Import the module
```python
import asyncio
import semantic_ai
```

### 2. To download the files from given source, extract the content from the downloaded files and index the extracted data in the given vector db.
```python
await semantic_ai.download()
await semantic_ai.extract()
await semantic_ai.index()
```
Suppose the job is running in longtime, we can watch the number of file processed, number of file failed and that filename stored in text file which are processed and failed in the 'EXTRACTED_DIR_PATH/meta' directory.
### Example
To connect the source and get the connection object. We can see that in examples folder.
Example: Sharepoint connector
```python
from semantic_ai.connectors import Sharepoint

CLIENT_ID = '<client_id>'  # sharepoint client id
CLIENT_SECRET = '<client_secret>'  # sharepoint client seceret
TENANT_ID = '<tenant_id>'  # sharepoint tenant id
SCOPE = 'https://graph.microsoft.com/.default'  # scope
HOST_NAME = "<tenant_name>.sharepoint.com"  # for example 'contoso.sharepoint.com'

# Sharepoint object creation
connection = Sharepoint(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        tenant_id=TENANT_ID,
                        host_name=HOST_NAME,
                        scope=SCOPE)
```
