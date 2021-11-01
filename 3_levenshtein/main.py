import csv
from typing import List
from elasticsearch import Elasticsearch, helpers

INDEX_NAME = 'sgjp'

class SGJPDictDefinition:
    def __init__(self, word, base_word, type):
        self.word = word
        self.base_word = base_word
        self.type = type 

def read_sgjp_dict(file_name='sgjp-20211024.tab'):
    print('Reading sgjp dictionary...')
    with open('sgjp-20211024.tab', 'r') as csvfile:
        # skip header
        for line in csvfile:
            if line.startswith('#</COPYRIGHT>'):
                break
        
        # read as csv
        result = []
        dictreader = csv.reader(csvfile, delimiter='\t')
        for i, row in enumerate(dictreader):
            result.append(SGJPDictDefinition(row[0],row[1],row[3]))
        return result

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
          'number_of_replicas': 0
        }
      },
    )

def index_sgjp(client: Elasticsearch, dictionary: List[SGJPDictDefinition]):
  if client.indices.stats(INDEX_NAME)['_all']['primaries']['docs']['count'] > 0:
    print('Some docs were already indexed. Skipping...')
    return  
  
  print(f'Indexing sgjp...')
  sources = [ {
    '_index': INDEX_NAME,
    '_source': {
      'word': term.word, 
      'base_word': term.base_word,
      'type': term.type
    }
  } for term in dictionary ]
  
  helpers.bulk(client, sources)
    
  print('Indexing completed.')
    

if __name__ == '__main__':
    sgjp_dict = read_sgjp_dict()

    client = Elasticsearch("http://localhost:9200")

    resp = client.info()

    print("Elastic info")
    print(resp)

    create_index(client)
    index_sgjp(client, sgjp_dict)