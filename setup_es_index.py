import requests
import json
import elasticsearch

INDEX_NAME = 'chat'
INDEX_TEMPLATE = {
    'mappings': {
        '_source': {
            'includes': [
                'id',
                'room_id',
                'content', # TODO remove this
            ]
        },
        'properties': {
            'id': {
                'type': 'long'
            },
            'room_id': {
                'type': 'long'
            },
            'user_name': {
                'type': 'text'
            },
            'content': {
                'type': 'text',
                'fields': {
                    'lang_analyzed': {
                        'type': 'text',
                        'analyzer': 'english'
                    }
                }
            }
        }
    }
}

def main():
    es = elasticsearch.Elasticsearch()
    indexes = elasticsearch.client.IndicesClient(es)

    if indexes.exists(INDEX_NAME):
        return
    print('Creating index')
    indexes.create(index=INDEX_NAME, body=INDEX_TEMPLATE)

main()
