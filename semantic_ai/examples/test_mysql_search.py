import asyncio
import json

from semantic_ai.connectors import Mysql

from semantic_ai.nlp.prompt import Prompt

sql = Mysql(
    host='<host>',
    user='<user_name>',
    password='<password>',
    database='<database_name>',
    port="<port_number>"  # 3306 is default port
)
cur = await sql.connect()
nlp_to_sql = await Prompt().nlp_to_sql(data_base=cur, normal_text="give me the total of on hole orders details")
data = json.loads(nlp_to_sql)
result = await sql.execute(cur, data)
print(result)
