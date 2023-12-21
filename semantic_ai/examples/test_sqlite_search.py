import asyncio
import json

from semantic_ai.connectors import get_connectors
from semantic_ai.connectors import Sqlite

from semantic_ai.llm.prompt_nlp import PromptNLP
import semantic_ai

file_path = f''

sql = Sqlite(sql_path=file_path)
conn = asyncio.run(sql.connect_db())
nlp_to_sql = asyncio.run(PromptNLP().nlp_to_sql(data_base=conn,
                                                normal_text="What are the top three regions per net profit?"))
data = json.loads(nlp_to_sql)
result = asyncio.run(sql.execution(data))
print(result)

