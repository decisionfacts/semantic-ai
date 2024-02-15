Introduction
=============

**Retrieval Augumented Generation** (RAG) is a type of model framework that integrates aspects of both information retrieval and natural language generation.
This approach aims to enhance the performance of language generation tasks by incorporating relevant information retrieved from a knowledge base or a large corpus of text.

The basic idea behind Retrieval-Augmented Generation is to first retrieve relevant information from a knowledge base using a retrieval model, and then use this retrieved information to augment the generation process of a language model. By leveraging external knowledge in this way, the model can produce more accurate, contextually relevant, and informative responses to natural language input.

RAG architectures have been applied to various tasks in natural language processing, such as question answering, dialogue generation, summarization, and more. They have shown promising results in improving the quality and relevance of generated text by integrating external knowledge during the generation process.

`DecisionFacts <https://decisionfacts.ai>`_ open-sourced RAG library - `Semantic AI <https://github.com/decisionfacts/semantic-ai>`_ is asynchronous framework to construct a knowledge base by indexing content into a Vector Database. The vector search APIs retrieve vector indexes from the database using cosine similarities/relevancy. The Large Language Model (LLM) then synthesizes summaries of the vector retrievals, presenting them as responses.

**Semantic AI - Indexer Architecture**

.. image:: https://github.com/decisionfacts/semantic-ai/blob/master/docs/source/_static/images/DF-Semantic-Indexer.png?raw=true
    :alt: Semantic AI - Indexer
   :align: center
   :width: 700px
   :height: 500px

Semantic AI indexer engine currently supports both unstructured and structured data sources such as SharePoint, S3, GCP Storage, Azure Datalake, MySQL, MS-SQL, SQLite, and more.

#. DF Connector connects to various data sources and pull documents

#. DF Extract model captures text from content, SQL databases, images, graphs, and other graphical objects

#. Extracted content converts as vector embeddings using HuggingFace’s vector embeddings or OpenAI’s vector embeddings

#. Create vector indexes and store it into vector databases


**Semantic AI - Search Architecture**

.. image:: https://github.com/decisionfacts/semantic-ai/blob/master/docs/source/_static/images/DF-Semantic-Search.png?raw=true
    :alt: Semantic AI - Search
   :align: center
   :width: 450px
   :height: 450px


Vector indexes stores in ElasticSearch, AWS OpenSearch, Qdrant and ChromaDB

#. Search Input query hits Inference API.

#. Inference service converts question as vectors using LLAMA 2 or OpenAI LLM and hits vector database to fetch results using KNN similarity search.

#. Fetches top K similarity search results and submits to LLM model to generate response along with document(s) / source(s)references.

#. Backend prompts gives instructions to LLM to generate response based on the search results from vector database.

#. Search results send as response for the search API request.






