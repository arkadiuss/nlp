import regex.regex
from collections import Counter


class ByPhraseUnitCounter:
    def count_by_regex_total(self, acts, reg) -> Counter:
        p = regex.compile(reg)
        global_counter = Counter()
        for act_name, _, text in acts:
            print(f'Analyzing {act_name}...')
            global_counter += Counter(p.findall(text))
        return global_counter

    def count_additions(self, acts) -> Counter:
        return self.count_by_regex_total(acts, r'dodaje się ([\w§]+)')

    def count_removals(self, acts) -> Counter:
        return self.count_by_regex_total(acts, r'skreśla się ([\w§]+)')

    def count_changes(self, acts) -> Counter:
        return self.count_by_regex_total(acts, r'([\w§]+)\.* \d+ otrzymuje brzmienie')

    def count_by_regex_by_year(self, acts, years, reg) -> {int: Counter}:
        p = regex.compile(reg)
        year_counter = dict([(y, Counter()) for y in years])
        for act_name, year, text in acts:
            print(f'Analyzing {act_name}...')
            year_counter[year] += Counter(p.findall(text))
        return year_counter

    def count_additions_by_year(self, acts, years) -> {int: Counter}:
        return self.count_by_regex_by_year(acts, years, r'dodaje się ([\w§]+)')

    def count_removals_by_year(self, acts, years) -> {int: Counter}:
        return self.count_by_regex_by_year(acts, years, r'skreśla się ([\w§]+)')

    def count_changes_by_year(self, acts, years) -> {int: Counter}:
        return self.count_by_regex_by_year(acts, years, r'([\w§]+)\.* \d+ otrzymuje brzmienie')