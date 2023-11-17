IBM Watsonx LLM
===============

The goal of this notebook is to demonstrate how to chain meta-llama/llama-2-70b-chat models to generate an answer to that question from the indexed vector database.

**IBM Watsonx Setup:**

Before you use the sample code in this notebook, you must perform the following setup tasks:

- Create a `Watson Machine Learning (WML) Service <https://console.ng.bluemix.net/catalog/services/ibm-watson-machine-learning/>`_ instance (a free plan is offered and information about how to create the instance can be found `here <https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/ml-service-instance.html?context=analytics>`_).

**Defining the Credentials:**

.. code-block:: python

    URL = "<ibm_url>" # https://us-south.ml.cloud.ibm.com
    API_KEY="<api_key>"
    PROJECT_ID="<project_id>"

**List of available models:**

.. code-block:: python

    from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
    print([model.value for model in ModelTypes])

.. code-block:: shell

    ['google/flan-t5-xxl', 'google/flan-ul2', 'bigscience/mt0-xxl', 'eleutherai/gpt-neox-20b', 'ibm/mpt-7b-instruct2', 'bigcode/starcoder', 'meta-llama/llama-2-70b-chat', 'ibm/granite-13b-instruct-v1', 'ibm/granite-13b-chat-v1']

**Defining the model parameters:**

.. code-block:: python

    parameters = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MAX_NEW_TOKENS: 500
    }

**Import Semantic AI:**

.. code-block:: python

    from semantic_ai.llm import Ibm

    model_type = "meta-llama/llama-2-70b-chat"
    ibm_llm  = await Ibm(
            url=URL,
            api_key=API_KEY,
            project_id=PROJECT_ID,
            model_type=model_type,
            parameters=parameters
    ).llm_model()

Once IBM Watsonx llm instance initiated, next we initiate the indexed vector database. We choose the indexed vector db and index name.

**Vector Database:**

Now we are going to use :ref:`elastic-search` vector database.

.. code-block:: python

    from semantic_ai.indexer import ElasticsearchIndexer
    from semantic_ai.embeddings.huggingface import HFEmbeddings

    embeddings = await HFEmbeddings().embed()
    elastic_search = await ElasticsearchIndexer(
            url="http://localhost:9200",
            index_name="test_index",
            embedding=embeddings
    ).create()

**Search:**

.. code-block:: python

    from semantic_ai.search.semantic_search import Search
    search_obj = Search(
                model=ibm_llm,
                load_vector_db=elastic_search
    )
    query = "What is an AI"
    search = await search_obj.generate(query)

We can change the top_k value and prompt using `top_k` and 'prompt' params respectively

.. code-block:: python

    search_obj = Search(
                model=ibm_llm,
                load_vector_db=elastic_search,
                top_k=5,
                prompt=prompt
    )
    query = "What is an AI"
    search = await search_obj.generate(query)