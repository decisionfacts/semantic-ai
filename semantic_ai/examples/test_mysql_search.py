import asyncio
import json

from semantic_ai.connectors import Mysql

from semantic_ai.llm.prompt_nlp import PromptNLP

sql = Mysql(
    host='localhost',
    user='',
    password='',
    database='',
    port=3306
)
cur = asyncio.run(sql.connect_db())
nlp_to_sql = asyncio.run(PromptNLP().nlp_to_sql(data_base=cur,
                                                normal_text="Please provide the count of shipped orders"))
data = json.loads(nlp_to_sql)
result = asyncio.run(sql.execution(data))
print(result)
