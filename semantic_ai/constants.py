# Connectors
SHARE_POINT = "sharepoint"

# Indexer
QDRANT = "qdrant"
ELASTIC_SEARCH = "elasticsearch"

# Default
DEFAULT_FOLDER_NAME = "download_file_dir"
JSON_OUTPUT_DIR = "extracted_dir"

# LLM
Llama = 'llama'
OPENAI = "openai"
IBM = 'ibm'

CONNECTORS_LIST = [
    "sharepoint"
]

INDEXER_LIST = [
    "elasticsearch",
    "qdrant"
]

LLM_LIST = [
    "ibm",
    "llama",
    "openai"
]

DEFAULT_PROMPT = '''Context: {context}

Based on Context provide me answer for following question
Question: {question}

Tell me the information about the fact. The answer should be from context only
do not use general knowledge to answer the query'''
