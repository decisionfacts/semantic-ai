DF Extraction
=============

DecisionFacts Extraction Library extracts content from PDF, PPTX, Docx, png, jpg., and convert as structured JSON data.

Prerequisites
-------------

.. code-block:: bash


    pip install df-extract

To extract content from PDF
---------------------------

.. code-block:: python

    from df_extract.pdf import ExtractPDF

    path = "/home/test/ABC.pdf"
    extract_pdf = ExtractPDF(file_path=path)

    # By default, output as text
    await extract_pdf.extract()  # Output will be located `/home/test/ABC.pdf.txt`

    # Output as json
    await extract_pdf.extract(as_json=True)  # Output will be located `/home/test/ABC.pdf.json`

You can change the output directory with simply pass ```output_dir``` param

.. code-block:: python

    from df_extract.pdf import ExtractPDF

    path = "/home/test/ABC.pdf"

    extract_pdf = ExtractPDF(file_path=path, output_dir="/home/test/output")
    await extract_pdf.extract()


Extract content from PDF with image data
----------------------------------------

This requires ```easyocr```

.. code-block:: python

    from df_extract.base import ImageExtract
    from df_extract.pdf import ExtractPDF

    path = "/home/test/ABC.pdf"

    image_extract = ImageExtract(model_download_enabled=True)
    extract_pdf = ExtractPDF(file_path=path, image_extract=image_extract)
    await extract_pdf.extract()
