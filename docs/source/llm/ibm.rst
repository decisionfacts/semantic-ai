.. _ibm:

IBM Watsonx LLM
===============


.. image:: https://github.com/decisionfacts/semantic-ai/blob/master/docs/source/_static/images/logo/Schermafbeelding-2023-08-30-161943-768x513.png?raw=true
    :alt: Logo
   :align: center
   :width: 100px
   :height: 80px
   :target: https://www.ibm.com/watsonx


The goal of this notebook is to demonstrate how to chain meta-llama/llama-2-70b-chat models to generate an answer to that question from the indexed vector database.

**IBM Watsonx Setup:**

Before you use the sample code in this notebook, you must perform the following setup tasks:

- First we need to create a project in IBM Watsonx. Follow `here <https://www.ibm.com/docs/en/watsonx-as-a-service?topic=projects-creating-project>`_ to create a project.
- Once create a project in IBM Watsonx we need to enable the instance service.
- Go to the project page `here <https://eu-de.dataplatform.cloud.ibm.com/projects/?context=wx>`_ in IBM.
- Select the project. And got to the *Manage* tab.

.. image:: https://github.com/decisionfacts/semantic-ai/blob/master/docs/source/_static/images/ibm/ibm_project_page.png?raw=true

- Click the *Associate service* -> *New service*. You see the *Services* page.

.. image:: https://github.com/decisionfacts/semantic-ai/blob/master/docs/source/_static/images/ibm/ibm_project_manage.png?raw=true

.. image:: https://github.com/decisionfacts/semantic-ai/blob/master/docs/source/_static/images/ibm/ibm_new_service.png?raw=true

- Click the *Watson Machine Learning*. Please select which instance do you want and config the instance.

.. image:: https://github.com/decisionfacts/semantic-ai/blob/master/docs/source/_static/images/ibm/ibm_ml_page.png?raw=true

.. image:: https://github.com/decisionfacts/semantic-ai/blob/master/docs/source/_static/images/ibm/ibm_instance_page.png?raw=true

- Once create the service please make sure that is initiate or not.





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