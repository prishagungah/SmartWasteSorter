BIN_RULES = {
    "bottle": "Plastic",
    "cup" : "Paper",
    "book" : "Paper",
    "banana" : "Organic",
    "apple" : "Organic",
    "toothbrush" : "Plastic",
}
REJECT_BIN = "Reject"
THRESHOLD = 0.5
class Sorter:
    def _init_(self, threshold=THRESHOLD):
        self.threshold = threshold
        self.counters = {name:0 for name in set(BIN_RULES.values())}
        self.counters[REJECT_BIN] = 0
        self.scores = {name: [] for name in set(BIN_RULES.values())}
    def sort(self, item):
        label = item.category.lower()

        if label not in BIN_RULES:
            self.counters[REJECT_BIN] += 1
            return REJECT_BIN
        elif item.score < self.threshold:
            bin_name = REJECT_BIN
        else:
            bin_name = BIN_RULES[label]

        self.counters[bin_name] += 1
        self.scores[bin_name].append(item.score)
        return bin_name
    def message(self, item):
        bin_name = self.sort(item)
        return f"This waste is a {item.category} and will be sorted in bin {bin_name}."
    def get_counters(self):
        return dict(self.counters)
    def get_scores(self):
        return {name:list(vals) for name, vals in self.scores.items()}
