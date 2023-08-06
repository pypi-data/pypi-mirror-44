import numpy as np
class PrecisionRecallTuner:
    def __init__(self):
        pass

    def _tune(self, clf, X, threshold, class_index, threshold_lower_bound, threshold_upper_bound):
        if threshold < threshold_lower_bound or threshold_upper_bound < threshold:
            raise Exception("""threshold must be between {} and {} 
                               for precision tuning""".format(
                                       threshold_lower_bound,
                                       threshold_upper_bound))
        probabilities = clf.predict_proba(X)
        return np.array([1 if probability[class_index] >= threshold else 0
                         for probability in probabilities])

    def tune_precision(self, clf, X, threshold, class_index):
        threshold_lower_bound = 0.5
        threshold_upper_bound = 1.0
        return self._tune(clf, X, threshold,
                          class_index,
                          threshold_lower_bound,
                          threshold_upper_bound)
        
    def tune_recall(self, clf, X, threshold, class_index):
        threshold_lower_bound = 0.01
        threshold_upper_bound = 0.5
        return self._tune(clf, X, threshold,
                          class_index,
                          threshold_lower_bound,
                          threshold_upper_bound)
        
        
