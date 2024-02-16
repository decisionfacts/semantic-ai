.. _sqlite:

SQLITE
======

.. figure:: https://github.com/decisionfacts/semantic-ai/blob/master/docs/source/_static/images/logo/Sqlite.jpeg?raw=true
   :alt: Logo
   :align: left
   :width: 100px

SQLite is an in-process library that implements a self-contained, serverless, zero-configuration, transactional SQL database engine.
SQLite is an embedded SQL database engine. Unlike most other SQL databases, SQLite does not have a separate server process. SQLite reads and writes directly to ordinary disk files.

This documents covers how to interact with SQLITE database using our library.

**Pre-requisites:**

    Please make sure the accessible Sqlite DB path.

**Setup:**

**To create a sqlite connection using path**

.. code-block:: python

    SQLITE_SQL_PATH = '<DB_PATH>'

.. code-block:: python

    from semantic_ai.connectors import Sqlite

    file_path = f'<DB_PATH>'
    sqlite = Sqlite(sql_path=file_path)
    conn = await sqlite.connect_db()

**To create natural language processing for normal text**

.. code-block:: python

    from semantic_ai.nlp.prompt import Prompt

    prompt = Prompt()
    prompt_res = await prompt.nlp_to_sql(data_base=conn, normal_text="query")

**To get answer from NLP**

.. code-block:: python

    data = json.loads(prompt_res)
    result = sql.execution(data)
