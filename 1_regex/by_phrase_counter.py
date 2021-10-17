import regex.regex
from collections import Counter


class ByPhraseUnitCounter:
    def count_by_regex(self, acts, reg) -> Counter:
        p = regex.compile(reg)
        global_counter = Counter()
        for act_name, text in acts:
            print(f'Analyzing {act_name}...')
            global_counter += Counter(p.findall(text))
        return global_counter

    def count_additions(self, acts) -> Counter:
        return self.count_by_regex(acts, r'dodaje się ([\w§]+)')

    def count_removals(self, acts) -> Counter:
        return self.count_by_regex(acts, r'skreśla się ([\w§]+)')

    def count_changes(self, acts) -> Counter:
        return self.count_by_regex(acts, r'([\w§]+)\.* \d+ otrzymuje brzmienie')

