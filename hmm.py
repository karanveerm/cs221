from collections import Counter
import pickle, random, copy
import create_equation_binary_data as cebd
import create_equation_unary_data as ceud

class HMM:
    def __init__(self):
        # The key is a tuple of (previous, current)
        self.conditional_probabilities = Counter()

        # SVM
        f = open('svm24px')
        self.svm = pickle.load(f)

        # Set of all the possible labelings
        self.labels = self.svm.classes_

        self.BEGIN_TAG = 'BEGIN'

    # The training data is already classified correctly
    def train(self, training_data):
        counts = Counter()
        for equation in training_data:
            # Can get pairs by referring to the previous entry
            counts[(self.BEGIN_TAG, equation[0])] += 1
            for i in xrange(1, len(equation)):
                counts[(equation[i-1], equation[i])] += 1

        # # Laplace smoothing
        # for prev_label in self.labels:
        #     for next_label in self.labels:
        #         counts[(prev_label, next_label)] += 1

        # Get the total counts of each previous symbol
        totals = Counter()
        for key in counts:
            totals[key[0]] += counts[key]

        for key in counts:
            self.conditional_probabilities[key] = counts[key] / float(totals[key[0]])

    def multinomial(self, pdf):
        assert( abs( sum(pdf) - 1. ) < 1e-4 )

        cdf = [0.] * len(pdf)
        for i in xrange(len(pdf)):
            cdf[i] = cdf[i-1] + pdf[i] # Being clever in using cdf[-1] = 0.
        rnd = random.random()
        for i in xrange(len(cdf)):
            if rnd < cdf[i]: 
                return i
        else:
            return len(cdf) - 1

    def choose_gibbs(self, labeling, equation, index, memoized_probabilities):
        # print index, equation, len(equation)
        # print equation[index][0]
        # print self.svm.predict_proba(equation[index][0]).tolist()
        if index not in memoized_probabilities:
            memoized_probabilities[index] = self.svm.predict_proba(equation[index][0]).tolist()[0]
        p = list()
        for i, label in enumerate(self.labels):
            if index == 0:
                p.append(self.conditional_probabilities[(self.BEGIN_TAG, label)] * memoized_probabilities[index][i])
            else:
                p.append(self.conditional_probabilities[(labeling[index - 1], label)] * memoized_probabilities[index][i])
        p = [x/sum(p) for x in p]
        new_label_index = self.multinomial(p)
        labeling[index] = self.labels[new_label_index]

    # Solve using Gibbs
    def compute_best_sequence(self, equation, num_samples = 500):
        num_symbols = len(equation)
        memoized_probabilities = dict()

        # Burn in is the number iterations to run from the initial labels chosen
        # before generating the samples. It prevents bias from starting labels.
        BURN_IN = 100
        labeling = [random.choice(self.labels) for _ in xrange(len(equation))]
        for _ in xrange(BURN_IN):
            index = random.randint(0, num_symbols - 1)
            self.choose_gibbs(labeling, equation, index, memoized_probabilities)

        # Now, generate the samples
        samples = []
        for _ in xrange(num_samples):
            index = random.randint(0, num_symbols - 1)
            self.choose_gibbs(labeling, equation, index, memoized_probabilities)
            samples.append(copy.deepcopy(labeling))

        # print samples

        # Finally, calculate the most common occurrence in the samples
        result_counter = Counter()
        for sample in samples:
            result_counter[tuple(sample,)] += 1

        # Returns the results as a tuple
        return result_counter.most_common(1)[0][0]

def num_differ(result, equation, num_differ_counter, num_same_counter):
    if len(result) != len(equation):
        print len(result)
        print len(equation)
        print 'NOT THE SAME LENGTH'
        return
    num_different = 0
    for i, label in enumerate(result):
        if label != equation[i][1]:
            num_differ_counter[equation[i][1]] += 1
        else:
            num_same_counter[equation[i][1]] += 1

hmm_instance = HMM()
hmm_instance.train(cebd.getTrainData())
test_data = ceud.getTestData()

num_differ_counter = Counter()
num_same_counter = Counter()
for equation in test_data:
    result = hmm_instance.compute_best_sequence(equation)
    print 'result is', result
    num_differ(result, equation, num_differ_counter, num_same_counter)

for symbol in num_same_counter:
    print symbol, 'accuracy:', num_same_counter[symbol] / float(num_same_counter[symbol] + num_differ_counter[symbol])

for symbol in num_differ_counter:
    if symbol not in num_same_counter:
        print symbol, 'accuracy: 0'