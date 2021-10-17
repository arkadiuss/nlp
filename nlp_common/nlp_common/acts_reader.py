from pathlib import Path
import random


class ActsReader:
    def __init__(self, path='./ustawy'):
        self.path = path

    def all_acts(self):
        for p in Path(self.path).glob('**/*.txt'):
            yield p.name, int(p.name[:4]), p.read_text()

    def acts_from_year(self, year):
        for i, p in enumerate(Path(self.path).glob(f'**/{year}_*.txt')):
            yield p.name, p.read_text()

    def first_n_acts(self, n=10):
        for i, p in enumerate(Path(self.path).glob('**/*.txt')):
            if i >= n:
                break
            yield p.name, int(p.name[:4]), p.read_text()

    def random_n_acts(self, n=10):
        for i, p in random.choices(list(enumerate(Path(self.path).glob('**/*.txt'))), k=n):
            yield p.name, int(p.name[:4]), p.read_text()

    def years(self) -> [int]:
        all_years = {int(p.name[:4]) for p in Path(self.path).glob('**/*.txt')}
        return list(all_years)


if __name__ == '__main__':
    # for name, year, act in ActsReader('../../ustawy').random_n_acts(3):
    #     print(name, year)
    print(ActsReader('../../ustawy').years())
