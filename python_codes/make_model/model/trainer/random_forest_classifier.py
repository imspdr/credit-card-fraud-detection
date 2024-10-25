from sklearn.ensemble import RandomForestClassifier

'''
custom random forest classifier 
implement additive training by extending estimators for full train near 24million rows data
'''

class CustomRandomForestClassifier:
    def __init__(self, **kwargs):
        self.name = "RandomForestClassifier"
        self.n_estimators = kwargs["n_estimators"]
        self.model = RandomForestClassifier(**kwargs)
        self.col_names = None

    def fit(self, X, y, col_names):
        self.model.fit(X, y)
        self.col_names = col_names
        return self

    def additive_fit(self, X, y):
        self.model.set_params(
            warm_start=True,
            n_estimators=self.model.n_estimators + self.n_estimators
        )
        self.model.fit(X, y)
        return self

    def predict(self, X):
        return self.model.predict(X)

    def predict_proba(self, X):
        return self.model.predict_proba(X)

    def feature_importance(self):
        return {"value": list(self.model.feature_importances_.round(4)), "label": self.col_names}
