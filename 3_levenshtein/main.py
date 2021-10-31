import csv

class SGJPDictDefinition:
    def __init__(self, word, base_word, type):
        self.word = word
        self.base_word = base_word
        self.type = type 

def read_sgjp_dict(file_name='sgjp-20211024.tab'):
    with open('sgjp-20211024.tab') as csvfile:
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

if __name__ == '__main__':
    sgjp_dict = read_sgjp_dict()