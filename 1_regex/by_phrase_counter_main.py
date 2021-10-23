from collections import Counter

from nlp_common.acts_reader import ActsReader
from by_phrase_counter import ByPhraseUnitCounter
from matplotlib import pyplot as plt
import numpy as np


class Unit:
    def __init__(self, name, aliases):
        self.name = name
        self.aliases = aliases


def count_by_unit(units, amendments) -> dict:
    res = {}
    for unit in units:
        c = 0
        for alias in unit.aliases:
            c += amendments[alias]
        res[unit.name] = c
    return res


def plot_by_unit(amendment_plot_data, name, path):
    plt.pie([x for x in amendment_plot_data.values()],
            labels=[f'{x} ({y})' for x, y in amendment_plot_data.items()],
            autopct='%1.1f%%'
            )
    plt.title(name)
    plt.savefig(path)
    plt.clf()


def sum_for_unit(amendments: Counter, unit: Unit):
    c = 0
    for alias in unit.aliases:
        c += amendments[alias]
    return c


def sum_for_units(amendments: Counter, units: [Unit]):
    c = 0
    for unit in units:
        c += sum_for_unit(amendments, unit)
    return c


def plot_amendments(countable_units, adds, rems, chs):
    ys = [sum_for_units(x, countable_units) for x in [adds, rems, chs]]
    plt.pie(ys,
            labels=[f'additions ({ys[0]})', f'removals ({ys[1]})', f'changes ({ys[2]})'],
            autopct='%1.1f%%'
            )
    plt.title('Amendments of units')
    plt.savefig('img/phrase_counter/amendments_by_type.png')
    plt.clf()


def plot_by_year(years, countable_units, adds_by_year, rems_by_year, chs_by_year):
    X_axis = np.arange(len(years))
    plt.xticks(X_axis, years)
    width = 0.2
    cwidth = -width
    for amendments_by_year, label in [(adds_by_year, 'additions'), (rems_by_year, 'removals'), (chs_by_year, 'changes')]:
        ys = [sum_for_units(amendments_by_year[y], countable_units) for y in years]
        plt.bar(X_axis + cwidth, ys, width=width, label=label)
        cwidth += width
    plt.legend()
    plt.title('Amendments of units by year')
    plt.savefig('img/phrase_counter/amendments_by_type_by_year.png')
    plt.clf()


def main():
    acts_reader = ActsReader('../ustawy')
    acts = lambda: acts_reader.all_acts()
    # acts = lambda: acts_reader.random_n_acts(10)

    units = [
        Unit('ustęp', ['ust', 'ustęp']),
        Unit('paragraf', ['paragraf', '§']),
        Unit('artykuł', ['art', 'artykuł']),
        Unit('punkt', ['pkt', 'punkt']),
        Unit('litera', ['lit', 'litery']),
        Unit('wyraz', ['wyraz', 'wyrazy']),
        Unit('zdanie', ['zdanie', 'zdania']),
    ]
    countable_units = units[:5]
    ctr = ByPhraseUnitCounter()
    adds = ctr.count_additions(acts())
    rems = ctr.count_removals(acts())
    chs = ctr.count_changes(acts())
    for data, name in [(adds, 'additions'), (rems, 'removals'), (chs, 'changes')]:
        plot_data = count_by_unit(units, data)
        plot_by_unit(plot_data, f'Types of {name}', f'img/phrase_counter/by_unit_{name}.png')

    plot_amendments(countable_units, adds, rems, chs)

    years = acts_reader.years()
    adds_by_year = ctr.count_additions_by_year(acts(), years)
    rems_by_year = ctr.count_removals_by_year(acts(), years)
    chs_by_year = ctr.count_changes_by_year(acts(), years)
    plot_by_year(years, countable_units, adds_by_year, rems_by_year, chs_by_year)


if __name__ == '__main__':
    main()
