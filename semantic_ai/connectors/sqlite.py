import json
import logging
import sqlite3

from langchain.utilities import SQLDatabase

from semantic_ai.connectors.base import BaseSqlConnector
from semantic_ai.llm import Openai
from semantic_ai.utils import sync_to_async
from sqlalchemy.exc import OperationalError
from semantic_ai.exceptions import ConnectorError

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

    async def execute(self, data: dict):
        try:
            query = data.get('SQLQuery')
            question = data.get('Question')
            conn = await sync_to_async(sqlite3.connect, self.sql_path)
            curr = await sync_to_async(conn.execute, query)
            labels = [description[0] async for description in curr.description]
            response = curr.fetchall()
            resp = {
                'query': question,
                'result': "Sorry, I can't find the answer from the data base"
            }
            if not response:
                return resp

            template = SQL_RESPONSE_TEMPLATE.format(question=question, response=response)
            openai_res = Openai(model_name_or_path="gpt-4-1106-preview")
            llm = await openai_res.llm_model()
            llm_result = await llm.agenerate(prompts=[template])
            if not llm_result or not llm_result.generations:
                return resp

            async for generation in llm_result.generations:
                async for result in generation:
                    if result:
                        resp['result'] = f'{resp.get("result")}\n {result.text}'
                        resp['ref_type'] = 'table'
                        resp['reference'] = json.dumps([dict(zip(labels, items)) for items in response])

            return resp
        except Exception as ex:
            logger.error('Search query exception => ', exc_info=ex)
            raise ConnectorError(f"Error connecting to the database")
