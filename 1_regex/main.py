from nlp_common.acts_reader import ActsReader
from by_phrase_counter import ByPhraseUnitCounter
from matplotlib import pyplot as plt


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


def plot_amendments(adds, rems, chs):
    plt.pie([adds['ust'], rems['ust'], chs['ust']],
            labels=[f'additions ({adds["ust"]})', f'removals ({rems["ust"]})', f'changes ({chs["ust"]})'],
            autopct='%1.1f%%'
            )
    plt.title('Amendments of "ustęp"')
    plt.savefig('img/phrase_counter/ust_amendments.png')
    plt.clf()


if __name__ == '__main__':
    acts = lambda: ActsReader('../ustawy').all_acts()
    # acts = lambda: ActsReader('../ustawy').first_n_acts(10)
    ctr = ByPhraseUnitCounter()
    adds = ctr.count_additions(acts())
    rems = ctr.count_removals(acts())
    chs = ctr.count_changes(acts())
    units = [
        Unit('ustęp', ['ust', 'ustęp']),
        Unit('paragraf', ['paragraf', '§']),
        Unit('wyraz', ['wyraz', 'wyrazy']),
        Unit('artykuł', ['art', 'artykuł']),
        Unit('punkt', ['pkt', 'punkt']),
        Unit('litera', ['lit', 'litery']),
        Unit('zdanie', ['zdanie', 'zdania']),
    ]

    for data, name in [(adds, 'additions'), (rems, 'removals'), (chs, 'changes')]:
        plot_data = count_by_unit(units, data)
        plot_by_unit(plot_data, f'Types of {name}', f'img/phrase_counter/by_unit_{name}.png')

    plot_amendments(adds, rems, chs)
