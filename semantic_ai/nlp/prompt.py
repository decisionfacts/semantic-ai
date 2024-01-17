import logging

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

from semantic_ai.llm import Openai
from semantic_ai.utils import sync_to_async

logger = logging.getLogger(__name__)

SQL_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} working query to run,
 then look at the results of the query and return the response from the DATABASE and give me as JSON response.
 Do not generate response from outside of the context.	
Use the following json format:

Question: "Question here",
SQLQuery: "SQL Query to run",
Answer: "Final answer here"


Only use the following tables:

{table_info}

If someone asks for the table, they really mean the table.

Question: {input}

Provide your SQLQuery and Answer in JSON format. Reply with only the answer in JSON format and include no other commentary:"""


class Prompt:

    def __init__(self):
        self.prompt = PromptTemplate(
            input_variables=["input", "table_info", "dialect"],
            template=SQL_DEFAULT_TEMPLATE
        )

    async def get_llm_chain(self, prompt: str = None):
        openai_llm = Openai(model_name_or_path="gpt-4-1106-preview")
        if not prompt:
            prompt = self.prompt
        return LLMChain(llm=await openai_llm.llm_model(), prompt=prompt)

    @staticmethod
    async def get_db_context(query: str, db):
        openai_llm = Openai(model_name_or_path="gpt-4-1106-preview")
        db_chain = SQLDatabaseChain.from_llm(openai_llm, db, verbose=True)
        db_context = await sync_to_async(db_chain, query)
        db_context = db_context['result'].strip()
        return db_context

    async def nlp_to_sql(self, data_base: SQLDatabase, normal_text: str, prompt: str = None):
        try:
            chain = await self.get_llm_chain(prompt)
            params = {
                'input': normal_text,
                'table_info': await sync_to_async(data_base.get_table_info),
                'dialect': data_base.dialect
            }
            return await sync_to_async(chain.run, params)
        except Exception as ex:
            raise f"Error search query exception"
