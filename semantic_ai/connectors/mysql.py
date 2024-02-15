import logging

import mysql.connector
from langchain.utilities import SQLDatabase
from mysql.connector import errorcode
from openai import AsyncOpenAI
from sqlalchemy.exc import OperationalError

from semantic_ai.connectors.base import BaseSqlConnector
from semantic_ai.constants import DEFAULT_LLM_MODEL
from semantic_ai.exceptions import ConnectorError
from semantic_ai.utils import sync_to_async

logger = logging.getLogger(__name__)

SQL_RESPONSE_TEMPLATE = """Generate natural language information based {question} and {response}."""


class Mysql(BaseSqlConnector):
    def __init__(
            self,
            host: str,
            user: str,
            password: str,
            database: str,
            port: int
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port or 3306
        self.client = AsyncOpenAI()

    async def connect(self):
        try:
            mysql_uri = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            return await sync_to_async(SQLDatabase.from_uri, mysql_uri)

        except OperationalError as ex:
            logger.error("`mysql` database error!", exc_info=ex)
            raise ConnectorError(f"`mysql` database error!\n{ex}")
        except Exception as ex:
            logger.error('`mysql` connector error!', exc_info=ex)
            raise ConnectorError(f'`mysql` connector error!\n{ex}')

    async def mysql_client(self):
        try:
            return await sync_to_async(
                mysql.connector.connect,
                user=self.user,
                password=self.password,
                host=self.host,
                database=self.database
            )

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.error("Something is wrong with your user name or password")
                raise ConnectorError("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.error("Database does not exist")
                raise ConnectorError("Database does not exist")
            else:
                logger.error(err)
                raise ConnectorError(err)

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
            resp['result'] = f'{llm_result.choices[0].message.content}'
            resp['ref_type'] = 'table'
            resp['reference'] = response
            return resp

        except Exception as ex:
            logger.error('Search query exception => ', exc_info=ex)
            raise ConnectorError(f"Error search query exception")

