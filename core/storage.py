from abc import ABC
import os
import json
import errno
from botocore.exceptions import ClientError


class Storage(ABC):
    def get(self, key):
        raise NotImplementedError

    def ls(self, key):
        raise NotImplementedError

    def exists(self, key):
        raise NotImplementedError

    def remove(self, key):
        raise NotImplementedError

    def put(self, key, data):
        raise NotImplementedError


class LocalStorage(Storage):
    def __init__(self, root: str):
        self._root = root

    def get(self, key):
        path = f"{self._root}/{key}"
        with open(path, "rb") as f:
            contents = f.read()
        return contents

    def ls(self, key):
        key = key.rstrip("/")
        local_dir = None
        file_prefix = None
        if not "/" in key:
            local_dir = f"{self._root}/{key}"
        else:
            rel_dirpath = "/".join(key.split("/")[:-1])
            local_dir = f"{self._root}/{rel_dirpath}"
            file_prefix = key.split("/")[-1]
        output = []
        for _, _, files in os.walk(local_dir):
            for file in files:
                if (not file_prefix) or file_prefix in file:
                    output.append(file)
        return output

    def exists(self, key):
        path = f"{self._root}/{key}"
        return os.path.exists(path) and os.path.isfile(path)

    def remove(self, key):
        path = f"{self._root}/{key}"
        if not os.path.exists(path):
            err = os.strerror(errno.ENOENT)
            raise FileNotFoundError(errno.ENOENT, err, path)
        if not os.path.isfile(path):
            raise ValueError("Invalid file specified for deletion")
        os.remove(path)

    def put(self, key, data):
        path = f"{self._root}/{key}"
        with open(path, "wb") as f:
            f.write(data)


class S3Bucket(Storage):
    def __init__(self, botoclient, bucket_name):
        self._botoclient = botoclient
        self._bucket = bucket_name

    def get(self, key):
        obj = self._botoclient.get_object(Bucket=self._bucket, Key=key)
        contents = obj["Body"].read()
        return contents

    def ls(self, key):
        response = self._botoclient.list_objects(Bucket=self._bucket, Prefix=key)
        if not "Contents" in response:
            return []
        items = response["Contents"]
        return [item["Key"] for item in items]

    def exists(self, key):
        try:
            return bool(self.get(key))
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return False
            raise e

    def remove(self, key):
        self._botoclient.delete_object(Key=key, Bucket=self._bucket)

    def put(self, key, data):
        self._botoclient.put_object(Body=data, Key=key, Bucket=self._bucket)


class MongoDB(Storage):
    def __init__(self, client, db, coll, field):
        self._coll = client[db][coll]
        self._field = field

    def get(self, key):
        query = {self._field: key}
        doc = self._coll.find_one(query)
        doc.pop("_id")
        string = json.dumps(doc)
        return bytes(string, "utf-8")

    def ls(self, key):
        query = {self._field: {"$regex": f"^{key}", "$options": "i"}}
        cursor = self._coll.find(query).limit(1000)
        output = []
        while cursor.alive:
            doc = cursor.next()
            output.append(doc[self._field])
        return output

    def exists(self, key):
        query = {self._field: key}
        doc = self._coll.find_one(query)
        return doc is not None

    def remove(self, key):
        self._coll.delete_one({self._field: key})

    def put(self, key, data):
        data = json.loads(data)
        data[self._field] = key
        response = self._coll.insert_one(data)
        assert response.acknowledged
