import time
from itertools import islice
from collections import defaultdict, Counter
from collections import defaultdict

line = "bonjour tout le monde"
test = line.split()

counts = Counter()


counts.update(test)
counts.update(["le"])

res = [item[0] for item in counts.most_common(2)]
print(set(res))