Semantic Search
===============

Semantic Search is, to retrieve the expected results and generate human-readable conversational responses with the help of LLM (Large Language Model).

First we need to create LLM and vector db object.

**LLM:**

.. code-block:: python

    import os
    os.environ['OPENAI_API_KEY'] = "<openai_api_key>"
    from semantic_ai.llm import Openai

    llm_model = await Openai().llm_model()

**Vector DB:**

.. code-block:: python

    from semantic_ai.indexer import ElasticsearchIndexer
    elastic_search = await ElasticsearchIndexer(
            url="http://localhost:9200",
            index_name="test_index",
            embedding=embeddings
    ).create()

**Search:**

.. code-block:: python

    from semantic_ai.search.semantic_search import Search
    search_obj = Search(
                model=llm_model,
                load_vector_db=elastic_search
    )
    query = "What is an AI"
    search = await search_obj.generate(query)

We can change the top_k value and prompt using `top_k` and 'prompt' params respectively

.. code-block:: python

    search_obj = Search(
                model=llm_model,
                load_vector_db=elastic_search,
                top_k=5,
                prompt=prompt
    )
    query = "What is an AI"
    search = await search_obj.generate(query)