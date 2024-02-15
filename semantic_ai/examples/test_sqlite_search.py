import asyncio
import json

from semantic_ai.connectors import Sqlite

from semantic_ai.nlp.prompt import Prompt

file_path = f'<file path>'

sql = Sqlite(sql_path=file_path)
conn = await (sql.connect())
nlp_to_sql = await (Prompt().nlp_to_sql(data_base=conn,
                                        normal_text=""))
data = json.loads(nlp_to_sql)
result = await (sql.execute(conn, data))
print(result)

