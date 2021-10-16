from common.acts import Acts
import regex.regex


def count_additions(acts):
    p = regex.compile(r'w art. [0-9]+ .* dodaje się ust. [0-9]+', regex.MULTILINE)
    for act_name, text in acts:
        print(f'Analyzing {act_name}...')
        print(p.findall(text))


if __name__ == '__main__':
    count_additions(Acts('../ustawy').first_n_acts(2))
