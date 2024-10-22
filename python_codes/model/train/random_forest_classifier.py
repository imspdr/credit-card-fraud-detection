from sklearn.ensemble import RandomForestClassifier

class CustomRandomForestClassifier:
    def __init__(self, n_estimators=20, max_features=0.8):
        self.name = "RandomForestClassifier"
        self.n_estimators = n_estimators
        self.model = RandomForestClassifier(n_estimators=n_estimators, max_features=max_features)
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
