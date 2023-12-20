import logging
import argparse
import uvicorn

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from semantic_ai import search
from semantic_ai.config import Settings

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Semantic AI",
              docs_url=f"/semantic-ai/docs")


class DocSearch(BaseModel):
    query: str


@app.on_event("startup")
async def on_startup():
    settings = getattr(app, 'settings', None)


@app.get("/semantic-ai")
async def info():
    return {'name': app.title}


@app.post("/semantic-ai/search")
async def semantic_search(doc_search: DocSearch):
    try:
        if doc_search.query:
            search_obj = await search(settings=getattr(app, 'settings', None))
            return await search_obj.generate(query=doc_search.query)
    except Exception as ex:
        logger.error('Search exception => ', exc_info=ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sorry! Internal server error while fetching search."
        )


def main():
    parser = argparse.ArgumentParser(description='Creating semantic ai')
    parser.add_argument('serve', help='Serve the inference', type=str)
    parser.add_argument('--file', '-f', help='Env file', required=True, type=str)
    parser.add_argument('--host', help='Host', default='127.0.0.1', type=str)
    parser.add_argument('--port', '-p', help='Port', default=8000, type=int)
    args = parser.parse_args()
    settings = Settings(_env_file=args.file)
    app.settings = settings
    uvicorn.run(app, host=args.host, port=args.port, env_file=args.file)


if __name__ == "__main__":
    main()
