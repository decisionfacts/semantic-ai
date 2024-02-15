import logging

from langchain.utilities import SQLDatabase
from openai import AsyncOpenAI
from sqlalchemy.exc import OperationalError

from semantic_ai.connectors.base import BaseSqlConnector
from semantic_ai.constants import DEFAULT_LLM_MODEL
from semantic_ai.exceptions import ConnectorError
from semantic_ai.utils import sync_to_async

logger = logging.getLogger(__name__)

SQL_RESPONSE_TEMPLATE = """Generate natural language information based {question} and {response}.
"""


class Sqlite(BaseSqlConnector):

    def __init__(
            self,
            *,
            sql_path
    ):
        self.sql_path = sql_path
        self.client = AsyncOpenAI()

    async def connect(self):
        try:
            db_path = f'sqlite:///{self.sql_path}'
            return await sync_to_async(SQLDatabase.from_uri, db_path)

        except OperationalError as ex:
            logger.error(f"Error connecting to the database:", exc_info=ex)
            raise ConnectorError(f"Error connecting to the database")
        except Exception as ex:
            logger.error('Error connecting to the database => ', exc_info=ex)
            raise ConnectorError(f"Error connecting to the database")

    async def execute(self, connection_obj, data: dict, llm_model: str = DEFAULT_LLM_MODEL):
        try:
            query = data.get('SQLQuery')
            question = data.get('Question')
            curr = await sync_to_async(connection_obj._execute, query)
            response = curr
            resp = {
                'query': question,
                'result': "Sorry, I can't find the answer from the data base"
            }
            if not response:
                return resp

            template = SQL_RESPONSE_TEMPLATE.format(question=question, response=response)
            messages = [
                {
                    "role": "system",
                    "content": template
                }
            ]
            openai_res = await self.client.chat.completions.create(
                model=llm_model,
                messages=messages
            )
            llm_result = openai_res
            if not llm_result:
                return resp
            if llm_result.choices:
                resp['result'] = f'{llm_result.choices[0].message.content}'
                resp['ref_type'] = 'table'
                resp['reference'] = response
                return resp
            else:
                return resp
        except Exception as ex:
            logger.error('Search query exception => ', exc_info=ex)
            raise ConnectorError(f"Error connecting to the database")
