from elasticsearch import Elasticsearch

if __name__ == '__main__':

    client = Elasticsearch("http://localhost:9200")

    resp = client.info()

    print("Elastic info")
    print(resp)

    client.indices.create(
      index='polish-bills',
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
