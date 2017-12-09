from sklearn.base import BaseEstimator, ClassifierMixin
from scipy import sparse


class MeanClassifier(BaseEstimator, ClassifierMixin):
    """
        An example of a classifier
    """

    def __init__(self, intValue=0, stringParam="defaultValue", differentParam=None):
        self.differentParam = differentParam
        self.stringParam = stringParam
        self.intValue = intValue

    def fit(self, X, y=None):
        assert (type(self.intValue) == int), "intValue parameter must be integer"
        assert (type(self.stringParam) == str), "stringValue parameter must be string"
#        assert (len(X) == 20), "X must be list with numerical values"

        self.threshold_ = sum(X) / len(X) + self.intValue

        return self

    def _meaning(self, x):
        return x >= self.threshold_

    def predict(self, X, y=None):
        try:
            getattr(self, "threshold_")
        except AttributeError:
            raise RuntimeError("You must train classifier before predicting data")

        return [self._meaning(x) for x in X]

    def score(self, X, y=None):
        return sum(self.predict(X))


if __name__ == '__main__':
    from sklearn.grid_search import GridSearchCV

    X_train = [i for i in range(0, 100, 5)]
    X_test = [i + 3 for i in range(-5, 95, 5)]
    tuned_params = dict(intValue=[-10, -1, 0, 1, 10])

    gs = GridSearchCV(MeanClassifier(), tuned_params)

    gs.fit(X_test, y=[1 for i in range(20)])
    print("best params: {}".format(gs.best_params_))
