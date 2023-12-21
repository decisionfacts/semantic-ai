import asyncio
import json

from semantic_ai.connectors import Mysql

from semantic_ai.nlp.prompt import Prompt

sql = Mysql(
    host='',
    user='',
    password='',
    database='',
    port=""  # 3306 is default port
)
cur = asyncio.run(sql.connect_db())
nlp_to_sql = asyncio.run(Prompt().nlp_to_sql(data_base=cur,
                                             normal_text=""))
data = json.loads(nlp_to_sql)
result = asyncio.run(sql.execution(data))
print(result)
