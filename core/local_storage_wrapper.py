"""
This is a custom wrapper around the PQAI local storage
"""

import os
import errno

class LocalStorage:

    """A wrapper class to hide the local storage's retrieval details.
    """

    def __init__(self, root):
        """Creates an LocalStorage class

        Args:
            root (str): Path of the local storage
        """
        self.root = root.rstrip('/')

    def get(self, rel_path):
        """Get data of an file from local storage

        Args:
            rel_path (str): file path

        Returns:
            contentts: Raw data of the file
        """
        path = self.root + '/' + rel_path
        with open(path, 'rb') as f:
            contents = f.read()
        return contents

    def put(self, rel_path, data):
        """Put a new data into the file

        Args:
            rel_path (str): file path
            data (bytes): Raw data to written on the file
        """
        path = self.root + '/' + rel_path
        with open(path, 'wb') as f:
            f.write(data)

    def delete(self, rel_path):
        """Remove a file from local storage

        Args:
            rel_path (str): file path
        """
        path = self.root + '/' + rel_path
        if not os.path.exists(path):
            err = os.strerror(errno.ENOENT)
            raise FileNotFoundError(errno.ENOENT, err, path)
        if not os.path.isfile(path):
            raise ValueError('Invalid file specified for deletion')
        os.remove(path)

    def list(self, path_prefix):
        """List the files matching the given prefix

        Args:
            path_prefix (str): desired file path to be searched

        Returns:
            list: Matching files
        """
        rel_dirpath = '/'.join(path_prefix.split('/')[:-1])
        local_dir = self.root + '/' + rel_dirpath
        file_prefix = path_prefix.split('/')[-1]
        output = []
        for _, _, files in os.walk(local_dir):
            for file in files:
                if file_prefix in file:
                    output.append(file)
        return output
