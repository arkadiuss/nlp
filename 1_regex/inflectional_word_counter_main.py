from collections import Counter
import numpy as np
import regex.regex
from nlp_common.acts_reader import ActsReader
from matplotlib import pyplot as plt


def count_by_regex(acts, reg) -> Counter:
    p = regex.compile(reg, regex.IGNORECASE)
    global_counter = Counter()
    for act_name, _, text in acts:
        global_counter += Counter(p.findall(text))
    return global_counter

# function to test if two regexes have a common match (to debug)
def check_by_regex(acts, reg, reg2) -> Counter:
    p = regex.compile(reg, regex.IGNORECASE)
    p2 = regex.compile(reg2, regex.IGNORECASE)
    for act_name, _, text in acts:
        
        test1 = np.array([ m.start(0) for m in p.finditer(text, regex.IGNORECASE) ])
        test2 = np.array([ m.start(0) for m in p2.finditer(text, regex.IGNORECASE) ])
        
        common = np.intersect1d(test1, test2)
        l = len(common)
        if l > 0:
            print(act_name, common[0], text[common[0]:common[0]+20])
    return 0

def plot_ctrs(ctrs: [int]):
    x_pos = np.arange(len(ctrs))
    plt.bar(x_pos, ctrs)
    plt.xticks(x_pos, ['ustaw*', 'ustaw* z dnia', 'ustaw* (~z dnia)', '(~o zmianie) ustaw*'])
    for x, y in zip(x_pos, ctrs):
        plt.text(x - 0.25, 1.01*y, str(y))
    plt.savefig('./img/inflectional_word_counter/word_counts.png')
    plt.clf()


def main():
    acts_reader = ActsReader('../ustawy')
    acts = lambda: acts_reader.all_acts()
    # acts = lambda: acts_reader.random_n_acts(1)

    print('Words with "ustaw" infix:')
    print(count_by_regex(acts(), r'ustaw[\w]*'))

    ustaw_ctr = count_by_regex(acts(), r'(ustaw)(a|ą|ach|ami|ę|ie|om|y)?\b')
    print('All forms from the word "ustawa":')
    print(ustaw_ctr)
    ustaw_total = np.sum(list(ustaw_ctr.values()))
    print(f'Total count: {ustaw_total}')

    # check_by_regex(acts(), r'(ustaw)(a|ą|ach|ami|ę|ie|om|y)?\b+(?=\s+z\s+dnia)', r'(ustaw)(a|ą|ach|ami|ę|ie|om|y)?\b+(?!\s+z\s+dnia)')

    ustaw_followed_by_ctr = count_by_regex(acts(), r'(ustaw)(a|ą|ach|ami|ę|ie|om|y)?\b+(?=\s+z\s+dnia)')
    print('All forms from the word "ustawa" followed by "z dnia":')
    print(ustaw_followed_by_ctr)
    ustaw_followed_by_total = np.sum(list(ustaw_followed_by_ctr.values()))
    print(f'Total count: {ustaw_followed_by_total}')

    ustaw_not_followed_by_ctr = count_by_regex(acts(), r'(ustaw)(a|ą|ach|ami|ę|ie|om|y)?\b+(?!\s+z\s+dnia)')
    print('All forms from the word "ustawa" not followed by "z dnia":')
    print(ustaw_not_followed_by_ctr)
    ustaw_not_followed_by_total = np.sum(list(ustaw_not_followed_by_ctr.values()))
    print(f'Total count: {ustaw_not_followed_by_total}')

    print(f'Check: {ustaw_total} =?= {ustaw_followed_by_total} + {ustaw_not_followed_by_total} = '
          f'{ustaw_followed_by_total + ustaw_not_followed_by_total}')

    ustaw_not_following_ctr = count_by_regex(acts(), r'(?<!o\s+zmianie\s+)(ustaw)(a|ą|ach|ami|ę|ie|om|y)?\b')
    print('All forms from the word "ustawa" not following "o zmianie":')
    print(ustaw_not_following_ctr)
    ustaw_not_following_total = np.sum(list(ustaw_not_following_ctr.values()))
    print(f'Total count: {ustaw_not_following_total}')

    plot_ctrs([ustaw_total, ustaw_followed_by_total, ustaw_not_followed_by_total, ustaw_not_following_total])


if __name__ == '__main__':
    main()
