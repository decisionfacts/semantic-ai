import asyncio
import json

from semantic_ai.connectors import Sqlite

from semantic_ai.nlp.prompt import Prompt

file_path = f''

sql = Sqlite(sql_path=file_path)
conn = asyncio.run(sql.connect_db())
nlp_to_sql = asyncio.run(Prompt().nlp_to_sql(data_base=conn,
                                             normal_text=""))
data = json.loads(nlp_to_sql)
result = asyncio.run(sql.execution(data))
print(result)

