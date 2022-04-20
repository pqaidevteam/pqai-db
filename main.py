"""Server

Attributes:
    app (fastapi.applications.FastAPI): FastAPI instance
    PORT (int): Port number
"""


import os
import uvicorn
from fastapi import FastAPI, Response

import dotenv
dotenv.load_dotenv()

#pylint: disable=wrong-import-position
from core import crud

PORT = int(os.environ['PORT'])

app = FastAPI()

@app.get('/patents/{doc_id}')
@app.get('/docs/{doc_id}')
async def get_doc(doc_id):
    """Return a document's data in JSON format

    Args:
        doc_id (str): Document identifier (e.g. patent number)

    Returns:
        dict: Document data
    """
    return crud.get_doc(doc_id)

@app.delete('/patents/{doc_id}')
@app.delete('/docs/{doc_id}')
async def delete_doc(doc_id):
    """Delete the document

    Args:
        doc_id (str): Document identifier (e.g. patent number)

    Returns:
       None
    """
    crud.delete_doc(doc_id)

@app.get('/patents/{doc_id}/drawings')
@app.get('/docs/{doc_id}/drawings')
async def list_drawings(doc_id):
    """Return a list of drawings associated with a document (patent).

    Args:
        doc_id (str): Document identifier (e.g. patent number)

    Returns:
        list: Drawing identifiers, e.g. ["1", "2", "3"]
    """
    return crud.list_drawings(doc_id)

@app.get('/patents/{doc_id}/drawings/{drawing_num}')
@app.get('/docs/{doc_id}/drawings/{drawing_num}')
async def get_drawing(doc_id, drawing_num):
    """Return image data of a particular drawing

    Args:
        doc_id (str): Drawing identifier (e.g. patent number)
        drawing_num (str): Drawing number, e.g., "1"

    Returns:
        bytes: Image data
    """
    image = crud.get_drawing(doc_id, drawing_num)
    return Response(content=image, media_type='image/tiff')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
