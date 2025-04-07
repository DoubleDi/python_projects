from parser import ParserService

from es import ElasticSearchService
from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    parsed = ParserService.parse(await file.read())
    await ElasticSearchService.bulk_insert(parsed)


@app.get("/query/")
async def query(value: str = ''):
    return await ElasticSearchService.query_with_filter(value)


@app.get("/createindex/")
async def create_index():
    return await ElasticSearchService.create_index()


@app.get('/aggregate/')
async def aggregate():
    return await ElasticSearchService.aggregate()
