Microsoft SharePoint
====================

.. figure:: https://github.com/decisionfacts/semantic-ai/blob/DFPS-172-Semantic-ai-LLM-IBM/docs/source/_static/images/logo/Microsoft_Office_SharePoint_(2019–present).svg.png?raw=true
    :alt: Logo
   :align: left
   :width: 100px
   :target: https://www.office.com/


This documents covers how to download the documents from Sharepoint.

**Pre-requisites:**

Register an application with the `Microsoft identity platform <https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app>`_ and create the client_id, client_secret and tenant_id.

**Setup:**

Access Microsoft share-point in azure portal:

- Go to Azure Portal `Microsoft Azure <https://portal.azure.com/#home>`_ and Login with username and password

- Go to azure service -> App registrations → New registration Enter the name and fill the details , click registration

- Then Go go certificates and secrets generate secret ids.

- Next provide app permissions (Site Permissions)

.. image:: https://github.com/decisionfacts/semantic-ai/blob/DFPS-172-Semantic-ai-LLM-IBM/docs/source/_static/images/azure_api_permissions.png?raw=true

.. image:: https://github.com/decisionfacts/semantic-ai/blob/DFPS-172-Semantic-ai-LLM-IBM/docs/source/_static/images/azure_openai_creds.png?raw=true

.. image:: https://github.com/decisionfacts/semantic-ai/blob/DFPS-172-Semantic-ai-LLM-IBM/docs/source/_static/images/azure.png?raw=true

To create a sharepoint connection with credentials
--------------------------------------------------

.. code-block:: python

    CLIENT_ID = '<client_id>'
    CLIENT_SECRET = '<client_secret>'
    TENANT_ID = '<tenant_id>'
    SCOPE = 'https://graph.microsoft.com/.default'
    HOST_NAME = "<tenant_name>.sharepoint.com"

.. code-block:: python

    from semantic_ai.connectors import Sharepoint
    sharepoint = Sharepoint(
            client_id = CLIENT_ID,
            client_secret = CLIENT_SECRET,
            tenant_id = TENANT_ID,
            scope = SCOPE,
            host_name = HOST_NAME
    )
    # To connect the particular site
    site_obj = await sharepoint.connect(site_name)

**To list the all sites**

.. code-block:: python

    list_sites = await sharepoint.list_sites()

To list the drives in the particular site

.. code-block:: python

    drives = await sharepoint.list_drives(site_id)

To list the root folders and files

.. code-block:: python

    folders = await sharepoint.list_folders(site_id, drive_id)

To download the files from particular folder
--------------------------------------------
We need a folder path 'data/accounts' to make a request for download.

.. code-block:: python

    await sharepoint.download(site_id, drive_id, folder_path)

By default output directory name `download_file_dir`

We can change the output directory with simply pass `output_dir` param

.. code-block:: python

    from semantic_ai.connectors import Sharepoint
    sharepoint = Sharepoint(
            client_id = CLIENT_ID,
            client_secret = CLIENT_SECRET,
            tenant_id = TENANT_ID,
            scope = SCOPE,
            host_name = HOST_NAME,
            output_dir="<path-to-download>"
    )

