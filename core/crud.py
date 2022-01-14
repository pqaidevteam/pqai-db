import os, json, dotenv, re
from core.s3wrapper import S3Bucket

dotenv.load_dotenv()

AWS_S3_BUCKET_NAME = os.environ['AWS_S3_BUCKET_NAME']
s3_bucket = S3Bucket(AWS_S3_BUCKET_NAME)

def get_doc(doc_id):
    key = f'patents/{doc_id}.json'
    contents = s3_bucket.get(key).decode()
    return json.loads(contents)

def list_drawings(doc_id):
    key_prefix = _drawing_prefix(doc_id)
    keys = s3_bucket.list(key_prefix)
    drawings = [re.search(r'-(\d+)', key).group(1) for key in keys]
    return drawings

def get_drawing(doc_id, n):
    key_prefix = _drawing_prefix(doc_id)
    key = f'{key_prefix}{n}.tif'
    tif_data = s3_bucket.get(key)
    return tif_data

def _drawing_prefix(doc_id):
    """
    For US Patent No. 7,654,321 the drawings are stored as follows:
        07654321-1.tif
        07654321-2.tif
        ...
        ...
    For US patent applications, say, for US20080156487A1, they're stored as:
        US20080156487A1-1.tif
        US20080156487A1-2.tif
        ...
        ...
    This function creates the appropriate key prefix on the basis of whether
    the supplied number is a patent or an application.
    """
    if len(doc_id) > 12:
        return f'images/{doc_id}-'
    else:
        num = re.search(r'\d+', doc_id).group(0)
        while len(num) < 8:
            num = '0' + num
        return f'images/{num}-'

def get_thumbnail(doc_id, n, h=200, w=None):
    """TODO: Scale down the image
    """
    key_prefix = _drawing_prefix(doc_id)
    key = f'{key_prefix}{n}.tif'
    tif_data = s3_bucket.get(key)
    return tif_data

def add_doc_json(doc_id, json_data):
    pass

def add_drawing(doc_id, tif_data):
    pass

def delete_doc(doc_id):
    pass

def delete_drawings(doc_id):
    pass
