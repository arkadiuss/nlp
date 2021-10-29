from elasticsearch import Elasticsearch, helpers
from nlp_common.acts_reader import ActsReader

INDEX_NAME = 'polish-bills'

def create_index(client: Elasticsearch):
  if client.indices.exists(INDEX_NAME):
    print(f'Index {INDEX_NAME} already exists. Skipping...')
    return
  
  print(f'Index {INDEX_NAME} doesn\'t exists. Creating...')
  client.indices.create(
      index=INDEX_NAME,
      body={
        'settings': {
          'number_of_shards': 1,
          'number_of_replicas': 0,
          'analysis': {
            'analyzer': {
              'polish-bills-analyzer': {
                'type': 'custom',
                'tokenizer': 'standard',
                'char_filter': [
                  'kodeks_synonyms'
                ],
                'filter': [
                  'morfologik_stem',
                  'lowercase'
                ]
              }
            },
            'char_filter': {
              'kodeks_synonyms': { 
                'type': 'mapping',
                'mappings': [
                  'kpk => kodeks postępowania karnego',
                  'kpc => kodeks postępowania cywilnego',
                  'kk => kodeks karny',
                  'kc => kodeks cywilny'
                ]
              }
            },
          }
        }
      },
    )


def index_bills(client: Elasticsearch):
  if client.indices.stats(INDEX_NAME)['_all']['primaries']['docs']['count'] > 0:
    print('Some docs were already indexed. Skipping...')
    return  
  
  print(f'Indexing bills...')
  reader = ActsReader('../ustawy')
  sources = [ {
    '_index': INDEX_NAME,
    '_source': {
      'name': name, 
      'text': bill
    }
  } for name, _, bill in reader.all_acts() ]
  
  helpers.bulk(client, sources)
    
  print('Indexing completed.')
  

if __name__ == '__main__':

    client = Elasticsearch("http://localhost:9200")

    resp = client.info()

    print("Elastic info")
    print(resp)

    create_index(client)
    index_bills(client)

  

