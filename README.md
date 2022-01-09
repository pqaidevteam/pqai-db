# PQAI Database

REST API for storing documents (patents as well as non-patent documents) in various formats (e.g. JSON, XML, PDF) and returning an appropriate version given the document’s identifier

## Routes

| Method | Endpoint                     | Comments                                         |
| ------ | ---------------------------- | ------------------------------------------------ |
| GET    | /docs/[docId]                | Returns a document’s JSON data                   |
| GET    | /docs/[docId]/drawings       | Returns a list of documents drawing identifiers  |
| GET    | /docs/[docId]/drawings/[n]   | Returns a single patent drawing                  |
| GET    | /docs/[docId]/thumbnails/[n] | Returns a single patent thumbnail                |
| POST   | /docs/[docId]                | Add (or overwrite) a new non-patent document     |
| POST   | /docs/[docId]/drawings/[n]   | Add (or overwrite) a new drawing                 |
| DELETE | /docs/[docId]                | Delete an existing document                      |
| DELETE | /docs/[docId]/drawings       | Delete all drawings of a document                |

## License

The project is open-source under the MIT license.

## Contribute

We welcome contributions. Please take a look at our guidelines to understand how you can contribute.

## Support

Please create an issue if you need help.