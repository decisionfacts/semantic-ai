MYSQL
======

.. figure:: https://github.com/decisionfacts/semantic-ai/blob/master/docs/source/_static/images/logo/mysql.png?raw=true
   :alt: Logo
   :align: left
   :width: 100px
   :target: https://www.office.com/

This documents covers how to interact with Mysql database using our library.

**Pre-requisites:**

    Please make sure the credentials of Mysql DB.

**Setup:**

**To create a mysql connection using credentials**

    Please setup the value to the following environment object

.. code-block:: python

    MYSQL_HOST='<host>'
    MYSQL_USER='<user>'
    MYSQL_PASSWORD='<password>'
    MYSQL_DATABASE='<database>'
    MYSQL_PORT='<port>'

.. code-block:: python

    from semantic_ai.connectors import Mysql

    conn = Mysql(
        host='<host>',
        user='<user_name>',
        password='<password>',
        database='<database>',
        port="<6033>" # it's default port
    )
    cursor = await conn.connect_db()

**To generate the sql query from NLP text**

.. code-block:: python

    from semantic_ai.nlp.prompt import Prompt

    prompt = Prompt()
    prompt_res = await prompt.nlp_to_sql(data_base=cursor, normal_text="query")

**To get answer from NLP**

.. code-block:: python

    data = json.loads(prompt_res)
    result = sql.execution(data)
