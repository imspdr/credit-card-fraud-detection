from .models.light_gbm_classifier import CustomLightGBMClassifier
from .models.random_forest_classifier import CustomRandomForestClassifier

model_dict = {
    "RandomForestClassifier": {
        "class": CustomRandomForestClassifier,
        "params": {
            "n_estimators": {"type": 1, "min": 50, "max": 200},
            "max_features": {"type": 2, "min": 0.1, "max": 0.9},
        },
    },
    "LightGBMClassifier": {
        "class": CustomLightGBMClassifier,
        "params": {
            "max_depth": {"type": 1, "min": 16, "max": 50},
            "learning_rate": {"type": 2, "min": 0.03, "max": 0.3},
            "n_estimators": {"type": 1, "min": 50, "max": 200},
        },
    },
}
