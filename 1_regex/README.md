# Solution to NLP labs 1

Task: https://github.com/apohllo/nlp/blob/master/1-regexp.md

## Count amendments by phrase
Amendments are found by specific words that should appear in a text: \
additions regex: `dodaje się ([\w§]+)`
removals regex: `skreśla się ([\w§]+)`
changes regex: `([\w§]+)\.* \d+ otrzymuje brzmienie`

![Types of additions](./img/phrase_counter/by_unit_additions.png)
![Types of removals](./img/phrase_counter/by_unit_removals.png)
![Types of changes](./img/phrase_counter/by_unit_changes.png)

Amendments to "ustęp":
![Types of amendments](./img/phrase_counter/ust_amendments.png)
 