Open AI
=======

Setup
-----
Accessing the API requires an API key, which you can get by creating an account and heading `here <https://platform.openai.com/account/api-keys>`_. Once we have a key we'll want to set it as an environment variable by running:

.. code-block:: python

    import os
    os.environ['OPENAI_API_KEY'] = '<openai_api_key>'

If you'd prefer not to set an environment variable you can pass the key in directly via the openai_api_key named parameter when initiating the OpenAI LLM class:

.. code-block:: python

    from semantic_ai.embeddings.openai import OpenAIEmbeddings

    embedding = OpenAIEmbeddings() # By default model name 'text-embedding-ada-002'
    embeddings = await embedding.embed() # OpenAI embedding object creation
