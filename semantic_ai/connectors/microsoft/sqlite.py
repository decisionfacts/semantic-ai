import json
import sqlite3
import logging


from fastapi import HTTPException, status
from langchain.utilities import SQLDatabase

from semantic_ai.llm import Openai
from semantic_ai.utils import sync_to_async
from semantic_ai.connectors.base import BaseSqlConnector

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

    async def connect_db(self):
        try:
            db_path = f'sqlite:///{self.sql_path}'
            return await sync_to_async(SQLDatabase.from_uri, db_path)

        except HTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error('Search query exception => ', exc_info=ex)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Sorry! Internal server error while executing query."
            )

    async def execution(self, data: dict):
        try:
            query = data.get('SQLQuery')
            question = data.get('Question')
            conn = sqlite3.connect(self.sql_path)
            curr = conn.execute(query)
            labels = [description[0] for description in curr.description]
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
            llm_result = await llm._agenerate(prompts=[template])
            if not llm_result or not llm_result.generations:
                return resp

            for generation in llm_result.generations:
                for result in generation:
                    if result:
                        resp['result'] = f'{resp.get("result")}\n {result.text}'
                        resp['ref_type'] = 'table'
                        resp['reference'] = json.dumps([dict(zip(labels, items)) for items in response])

            return resp
        except Exception as ex:
            logger.error('Search query exception => ', exc_info=ex)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Sorry! Internal server error while executing query."
            )
