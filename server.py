import os
import dotenv
import uvicorn
from fastapi import FastAPI, Response
from core import crud

dotenv.load_dotenv()

PORT = int(os.environ['PORT'])

app = FastAPI()

@app.get('/docs/{doc_id}')
async def get_doc(doc_id):
    return crud.get_doc(doc_id)

@app.get('/docs/{doc_id}/drawings')
async def list_drawings(doc_id):
    return crud.list_drawings(doc_id)

@app.get('/docs/{doc_id}/drawings/{n}')
async def get_drawing(doc_id, n):
    image = crud.get_drawing(doc_id, n)
    return Response(content=image, media_type='image/tiff')

@app.get('/docs/{doc_id}/thumbnails/{n}')
async def get_thumbnail(doc_id, n):
    image = crud.get_thumbnail(doc_id, n)
    return Response(content=image, media_type='image/tiff')

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