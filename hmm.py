from collections import Counter
import pickle, inkml_to_pixels as itop

BEAM_SEARCH_N = 5

class HMM:
    def __init__(self):
        # The key is a tuple of (previous, current)
        self.conditional_probabilities = Counter()

        f = open("svm")
        self.svm = pickle.load(f)

    # The training data is already classified correctly
    def train_hmm(training_data):
        counts = Counter()
        for equation in training_data:
            # Can get pairs by referring to the previous entry
            for i in xrange(1, len(equation)):
                counts[(equation[i-1], equation[i])] += 1

        total_counts = float(sum(counts.values()))
        for key in counts():
            self.conditional_probabilities[key] = counts[key] / total_counts

    # The test data has the symbols in pixels
    def test_hmm(test_data):
        best_candidates = []
        for i, strokes in xrange(1, len(test_data)):
            feature_vector = itop.inkml_to_pixels(strokes)
            feature_vector.append(len(strokes))
            log_ps = self.svm.predict_log_proba(feature_vector)
            