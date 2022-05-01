# PQAI Data Storage Service

REST API for storing and retrieving documents. Documents can belong to patent or non-patent literature. The default format of data is JSON but other formats are supported. Drawings & figures are also supported.

## Routes

|      | Method   | Endpoint                       | Comments                                         |
| ---- | -------- | ------------------------------ | ------------------------------------------------ |
|      | `GET`    | `/docs/[docId]`                | Returns a document’s JSON data                   |
|      | `GET`    | `/docs/[docId]/drawings`       | Returns a list of document’s drawing identifiers |
|      | `GET`    | `/docs/[docId]/drawings/[n]`   | Returns a single patent drawing                  |
| *    | `GET`    | `/docs/[docId]/thumbnails/[n]` | Returns a single patent thumbnail                |
| *    | `PUT`    | `/docs/[docId]`                | Add (or overwrite) a new non-patent document     |
| *    | `PUT`    | `/docs/[docId]/drawings/[n]`   | Add (or overwrite) a new drawing                 |
|      | `DELETE` | `/docs/[docId]`                | Delete an existing document                      |
| *    | `DELETE` | `/docs/[docId]/drawings`       | Delete all drawings of a document                |

*Yet to be implemented

## License

The project is open-source under the MIT license.

## Contribute

We welcome contributions.

To make a contribution, please follow these steps:

1. Fork this repository.
2. Create a new branch with a descriptive name
3. Make copy of env file as .env and docker-compose.dev.yml as docker-compose.yml
4. Bring DB to life `docker-compose up`
5. Make the changes you want and add new tests, if needed
6. Make sure all tests are passing `docker exec -i dev_pqai_db_api python -m unittest discover ./tests/`
7. Commit your changes
8. Submit a pull request

## Support

Please create an issue if you need help.
