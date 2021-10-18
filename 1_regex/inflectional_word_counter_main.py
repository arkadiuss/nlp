from collections import Counter
import numpy as np
import regex.regex
from nlp_common.acts_reader import ActsReader


def count_by_regex(acts, reg) -> Counter:
    p = regex.compile(reg, regex.IGNORECASE)
    global_counter = Counter()
    for act_name, _, text in acts:
        global_counter += Counter(p.findall(text))
    return global_counter


def main():
    acts_reader = ActsReader('../ustawy')
    acts = lambda: acts_reader.all_acts()
    # acts = lambda: acts_reader.random_n_acts(10)

    print('Words with "ustaw" infix:')
    print(count_by_regex(acts(), r'ustaw[\w]*'))

    ustaw_ctr = count_by_regex(acts(), r'(ustaw)(\b|a|ą|ach|ami|ie|om|y)')
    print('All forms from the word "ustawa":')
    print(ustaw_ctr)
    ustaw_total = np.sum(list(ustaw_ctr.values()))
    print(f'Total count: {ustaw_total}')

    ustaw_followed_by_ctr = count_by_regex(acts(), r'(ustaw)(\b|a|ą|ach|ami|ie|om|y)(?= z dnia)')
    print('All forms from the word "ustawa" followed by "z dnia":')
    print(ustaw_followed_by_ctr)
    ustaw_followed_by_total = np.sum(list(ustaw_followed_by_ctr.values()))
    print(f'Total count: {ustaw_followed_by_total}')

    ustaw_not_followed_by_ctr = count_by_regex(acts(), r'(ustaw)(\b|a|ą|ach|ami|ie|om|y)(?! z dnia)')
    print('All forms from the word "ustawa" not followed by "z dnia":')
    print(ustaw_not_followed_by_ctr)
    ustaw_not_followed_by_total = np.sum(list(ustaw_not_followed_by_ctr.values()))
    print(f'Total count: {ustaw_not_followed_by_total}')

    print(f'Check: {ustaw_total} =?= {ustaw_followed_by_total} + {ustaw_not_followed_by_total} = '
          f'{ustaw_followed_by_total + ustaw_not_followed_by_total}')

    ustaw_not_following_ctr = count_by_regex(acts(), r'(?<!o zmianie )(ustaw)(\b|a|ą|ach|ami|ie|om|y)')
    print('All forms from the word "ustawa" not following "o zmianie":')
    print(ustaw_not_following_ctr)
    ustaw_not_following_total = np.sum(list(ustaw_not_following_ctr.values()))
    print(f'Total count: {ustaw_not_following_total}')


if __name__ == '__main__':
    main()
