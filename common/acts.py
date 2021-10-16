from pathlib import Path


class Acts:
    def __init__(self, path='./ustawy'):
        self.path = path

    def all_acts(self):
        for p in Path(self.path).glob('**/*.txt'):
            yield p.name, p.read_text()

    def acts_from_year(self, year):
        for i, p in enumerate(Path(self.path).glob(f'**/{year}_*.txt')):
            yield p.name, p.read_text()

    def first_n_acts(self, n=10):
        for i, p in enumerate(Path(self.path).glob('**/*.txt')):
            if i > n:
                break
            yield p.name, p.read_text()


if __name__ == '__main__':
    Acts().first_n_acts(3)
