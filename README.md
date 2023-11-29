![Semantic AI Logo](https://github.com/decisionfacts/semantic-ai/blob/master/docs/source/_static/images/createLLM.png?raw=True)
# Semantic AI Lib

[![Python version](https://img.shields.io/badge/python-3.10-green)](https://img.shields.io/badge/python-3.10-green)[![PyPI version](https://badge.fury.io/py/semantic-ai.svg)](https://badge.fury.io/py/semantic-ai)[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

An open-source framework for Retrieval-Augmented System (RAG) uses semantic search to retrieve the expected results and generate human-readable conversational responses with the help of LLM (Large Language Model).

**Semantic AI Library Documentation [Docs here](https://docs-semantic-ai.decisionfacts.ai/)**

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
Set the credentials in .env file. Only give the credential for an one connector, an one indexer and an one llm model config. other fields put as empty
```shell
# Default
FILE_DOWNLOAD_DIR_PATH= # default directory name 'download_file_dir'
EXTRACTED_DIR_PATH= # default directory name 'extracted_dir'

# Connector (SharePoint, S3, GCP Bucket, GDrive, Confluence etc.,)
CONNECTOR_TYPE="connector_name" # sharepoint
SHAREPOINT__CLIENT_ID="client_id"
SHAREPOINT__CLIENT_SECRET="client_secret"
SHAREPOINT__TENANT_ID="tenant_id"
SHAREPOINT__HOST_NAME='<tenant_name>.sharepoint.com'
SHAREPOINT__SCOPE='https://graph.microsoft.com/.default'
SHAREPOINT__SITE_ID="site_id"
SHAREPOINT__DRIVE_ID="drive_id"
SHAREPOINT__FOLDER_URL="folder_url" # /My_folder/child_folder/

# Indexer
INDEXER_TYPE="vector_db_name" # elasticsearch, qdrant
ELASTICSEARCH__URL="elasticsearch_url" # give valid url
ELASTICSEARCH__USER="elasticsearch_user" # give valid user
ELASTICSEARCH__PASSWORD="elasticsearch_password" # give valid password
ELASTICSEARCH__INDEX_NAME="index_name"
ELASTICSEARCH__SSL_VERIFY="ssl_verify" # True or False

# Qdrant
QDRANT__URL="<qdrant_url>"
QDRANT__INDEX_NAME="<index_name>"
QDRANT__API_KEY="<apikey>"

# LLM
LLM__MODEL="<llm_model>" # llama, openai
LLM__MODEL_NAME_OR_PATH="" # model name
OPENAI_API_KEY="<openai_api_key>" # if using openai
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

### 2. To download the files from a given source, extract the content from the downloaded files and index the extracted data in the given vector db.
```python
await semantic_ai.download()
await semantic_ai.extract()
await semantic_ai.index()
```
After completion of download, extract and index, we can generate the answer from indexed vector db. That code given below.
### 3. To generate the answer from indexed vector db using retrieval LLM model.
```python
search_obj = await semantic_ai.search()
query = ""
search = await search_obj.generate(query)
```
Suppose the job is running for a long time, we can watch the number of files processed, the number of files failed, and that filename stored in the text file that is processed and failed in the 'EXTRACTED_DIR_PATH/meta' directory.

### Example
To connect the source and get the connection object. We can see that in the examples folder.
Example: SharePoint connector
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
## Run in the server
```shell
$ semantic_ai serve -f .env

INFO:     Loading environment from '.env'
INFO:     Started server process [43973]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
Open your browser at http://127.0.0.1:8000/semantic-ai

### Interactive API docs
Now go to http://127.0.0.1:8000/docs.
You will see the automatic interactive API documentation (provided by Swagger UI):
![Swagger UI](https://github.com/decisionfacts/semantic-ai/blob/master/docs/source/_static/images/img.png?raw=True)
