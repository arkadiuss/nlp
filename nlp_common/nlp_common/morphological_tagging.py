import requests
import os

def tag_morphologically(bills):
    file_name = "tags_response.txt"
    if os.path.exists(file_name):
        print("Reading cached response")
        with open(file_name, "r") as f:
            return split_tagged_response(f.read())
    else:
        with open(file_name, "w") as f:
            for i, bill in enumerate(bills):
                tagged_response = requests.post('http://localhost:9200', bill.encode(encoding='utf-8'))
                f.write(tagged_response.text)
                print(f"Processed: {i+1}/{len(bills)}")
        return tag_morphologically(bills)

def split_tagged_response(tagged_corpus):
    splitted = [ l for l in tagged_corpus.split('\n') if l != '']
    unigrams = []
    for i in range(0, len(splitted), 2):
        if splitted[i].startswith('\t') or not splitted[i+1].startswith('\t'):
            raise Exception("Wrong assumption")
          
        tagging =  splitted[i+1].split('\t')
        tags = tagging[2].split(':')
        unigrams.append((splitted[i], tagging[1], tags))
    
    return unigrams
    