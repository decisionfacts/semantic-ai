import json
import logging
import mysql.connector
from mysql.connector import errorcode

from semantic_ai.llm import Openai
from semantic_ai.connectors.base import BaseSqlConnector
from langchain.utilities import SQLDatabase
from fastapi import HTTPException, status

from semantic_ai.utils import sync_to_async

logger = logging.getLogger(__name__)


SQL_RESPONSE_TEMPLATE = """Generate natural language information based {question} and {response}.

Add currency symbol in the prefix if you find for amount, net profit, gross profit or revenue based on this {currency}
"""


class Mysql(BaseSqlConnector):
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port or 3306

    async def connect_db(self):
        try:
            mysql_uri = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            return await sync_to_async(SQLDatabase.from_uri, mysql_uri)
        except HTTPException as ex:
            raise ex
        except Exception as ex:
            logger.error('Search query exception => ', exc_info=ex)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Sorry! Internal server error while executing query."
            )

    async def mysql_client(self):
        try:
            return mysql.connector.connect(user=self.user,
                                           password=self.password,
                                           host=self.host,
                                           database=self.database)

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logger.error("Something is wrong with your user name or password")
                raise "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.error("Database does not exist")
                raise "Database does not exist"
            else:
                logger.error(err)
                raise err

    async def execution(self, data: dict):
        try:
            query = data.get('SQLQuery')
            question = data.get('Question')
            currency = data.get('Currency')
            conn = await self.mysql_client()
            curr = conn.cursor()
            curr.execute(query)
            labels = [description[0] for description in curr.description]
            response = curr.fetchall()
            curr.close()
            resp = {
                'query': question,
                'result': "Sorry, I can't find the answer from the data base"
            }
            if not response:
                return resp

            template = SQL_RESPONSE_TEMPLATE.format(question=question, response=response, currency=currency)
            openai_res = Openai()
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


