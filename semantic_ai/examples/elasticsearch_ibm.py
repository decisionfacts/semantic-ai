import asyncio

from semantic_ai.indexer import ElasticsearchIndexer
from semantic_ai.llm import Ibm
from semantic_ai.search.semantic_search import Search


async def main(_query):
    vector_db = await ElasticsearchIndexer(url="http://localhost:9200",
                                           index_name="demo").create()
    llm = await Ibm(url="<url>",
                    api_key="<api_key>",
                    project_id="<project_id>"
                    ).llm_model()

    search = Search(
        model=llm,
        load_vector_db=vector_db
    )

    response = await search.generate(_query)
    return response


if __name__ == "__main__":
    query = input("Ask question: ")
    print(asyncio.run(main(query)))
