"""Summary

Attributes:
    app (TYPE): Description
    PORT (TYPE): Description
"""
import os
import dotenv
import uvicorn
from fastapi import FastAPI, Response
import errno
from core import crud
from core.local_storage_wrapper import LocalStorage
dotenv.load_dotenv()

PORT = int(os.environ['PORT'])

app = FastAPI()

@app.get('/docs/{doc_id}')
async def get_doc(doc_id):
    """Return a document's data in JSON format

    Args:
        doc_id (str): Document identifier (e.g. patent number)

    Returns:
        dict: Document data
    """
    return crud.get_doc(doc_id)
    
@app.delete('/docs/{doc_id}')
async def delete_doc(doc_id):

    file_path = os.getcwd()+ f'/tests/test-dir/patents/{doc_id}.json'
    if os.path.exists(file_path):
        os.remove(file_path)
        print("File Sucessfully Deleted")
    else:
        raise FileNotFoundError(errno.ENOENT,
                                    os.strerror(errno.ENOENT),
                                    file_path)

@app.get('/docs/{doc_id}/drawings')
async def list_drawings(doc_id):
    """Return a list of drawings associated with a document (patent).

    Args:
        doc_id (str): Document identifier (e.g. patent number)

    Returns:
        list: Drawing identifiers, e.g. ["1", "2", "3"]
    """
    return crud.list_drawings(doc_id)

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
