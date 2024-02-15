Introduction
=============

**Retrieval Augumented Generation** (RAG) is a type of model framework that integrates aspects of both information retrieval and natural language generation.
This approach aims to enhance the performance of language generation tasks by incorporating relevant information retrieved from a knowledge base or a large corpus of text.

The basic idea behind Retrieval-Augmented Generation is to first retrieve relevant information from a knowledge base using a retrieval model, and then use this retrieved information to augment the generation process of a language model. By leveraging external knowledge in this way, the model can produce more accurate, contextually relevant, and informative responses to natural language input.

RAG architectures have been applied to various tasks in natural language processing, such as question answering, dialogue generation, summarization, and more. They have shown promising results in improving the quality and relevance of generated text by integrating external knowledge during the generation process.

`DecisionFacts <https://decisionfacts.ai>`_ open-sourced RAG library - `Semantic AI <https://github.com/decisionfacts/semantic-ai>`_ is asynchronous framework to construct a knowledge base by indexing content into a Vector Database. The vector search APIs retrieve vector indexes from the database using cosine similarities/relevancy. The Large Language Model (LLM) then synthesizes summaries of the vector retrievals, presenting them as responses.




