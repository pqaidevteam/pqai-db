import os
import dotenv
import uvicorn
import crud
from fastapi import FastAPI

dotenv.load_dotenv()

PORT = int(os.environ['PORT'])

app = FastAPI()

@app.get('/docs/{doc_id}')
async def get_doc(doc_id):
    pass

@app.get('/docs/{doc_id}/drawings')
async def list_drawings(doc_id):
    pass

@app.get('/docs/{doc_id}/drawings/{n}')
async def get_drawing(doc_id, n):
    pass

@app.get('/docs/{doc_id}/thumbnails')
async def list_thumbnails(doc_id):
    pass

@app.get('/docs/{doc_id}/thumbnails/{n}')
async def get_thumbnail(doc_id, n):
    pass

@app.post('/docs/{doc_id}')
async def add_doc(doc_id):
    pass

@app.post('/docs/{doc_id}/drawings/{n}')
async def add_drawing(doc_id, n):
    pass

@app.delete('/docs/{doc_id}')
async def delete_doc(doc_id):
    pass

@app.delete('/docs/{doc_id}/drawings')
async def delete_all_drawings(doc_id):
    pass

@app.delete('/docs/{doc_id}/drawings/{n}')
async def delete_drawing(doc_id, n):
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)