[![Python](https://img.shields.io/badge/python-v3.8-blue)](https://www.python.org/)
[![Linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![Docker build: automated](https://img.shields.io/badge/docker%20build-automated-066da5)](https://www.docker.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub license](https://img.shields.io/github/license/pqaidevteam/pqai?style=plastic)](https://github.com/pqaidevteam/pqai/blob/master/LICENSE)

# PQAI Data Storage Service

REST API for storing and retrieving documents. Documents can belong to patent or non-patent literature. The default format of data is JSON but other formats are supported. Drawings & figures are also supported.

## Routes

|      | Method   | Endpoint                          | Comments                                         |
| ---- | -------- | --------------------------------- | ------------------------------------------------ |
|      | `GET`    | `/patents/[docId]`                | Returns a document’s JSON data                   |
|      | `GET`    | `/patents/[docId]/drawings`       | Returns a list of document’s drawing identifiers |
|      | `GET`    | `/patents/[docId]/drawings/[n]`   | Returns a single patent drawing                  |
| *    | `GET`    | `/patents/[docId]/thumbnails/[n]` | Returns a single patent thumbnail                |

*Yet to be implemented

## How to run?

### From command line

1. Clone this repository
2. Create a `.env` file using `/env` template and set environment variable values
3. Create a virtual environment and install dependencies: `pip install -r requirements.txt`
4. Run the service: `python3 main.py`

### As docker container

1. Clone this repository
1. Create a `.env` file using `/env` template and set environment variable values
1. Give execution permission to the deployment script: `chmod +x deploy.sh`
1. Run deployment script: `bash deploy.sh`


## License

The project is open-source under the MIT license.

## Contribute

We welcome contributions.

To make a contribution, please follow these steps:

1. Fork this repository.
2. Create a new branch with a descriptive name
3. Make the changes you want and add new tests, if needed
4. Make sure all tests are passing
5. Commit your changes
6. Submit a pull request

## Support

Please create an issue if you need help.
