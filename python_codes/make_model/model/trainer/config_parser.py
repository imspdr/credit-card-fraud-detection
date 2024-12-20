import ConfigSpace as CS
from .light_gbm_classifier import CustomLightGBMClassifier
from .random_forest_classifier import CustomRandomForestClassifier

'''
config generator for BOHB
'''

# model mapper
model_mapper = {
    "LightGBMClassifier": CustomLightGBMClassifier,
    "RandomForestClassifier": CustomRandomForestClassifier
}
# config space dictionary
model_dict = {
    "LightGBMClassifier": {
        "params": {
            "num_leaves": {"type": 1, "min": 32, "max": 128},
            "learning_rate": {"type": 2, "min": 0.1, "max": 0.3},
        },
    },
    "RandomForestClassifier": {
        "params": {
            "n_estimators": {"type": 1, "min": 100, "max": 200},
            "max_features": {"type": 2, "min": 0.1, "max": 0.8},
        },
    },
}

class ConfigParser:
    def __init__(self, custom_model=model_dict, model_mapper=model_mapper):
        self.custom_model = custom_model
        self.model_mapper = model_mapper

    # build config space from given model dict
    def build_bohb_config(self):
        config_space = CS.ConfigurationSpace()
        hp = CS.CategoricalHyperparameter("model", list(self.custom_model.keys()))
        config_space.add_hyperparameter(hp)
        for model, params in self.custom_model.items():
            for param, param_space in params["params"].items():
                param_type = param_space["type"]
                if param_type in [1, "1"]:
                    hp = CS.UniformIntegerHyperparameter(
                        model + "-" + param, param_space["min"], param_space["max"]
                    )
                    config_space.add_hyperparameter(hp)
                elif param_type in [2, "2"]:
                    hp = CS.UniformFloatHyperparameter(
                        model + "-" + param, param_space["min"], param_space["max"]
                    )
                    config_space.add_hyperparameter(hp)
                else:
                    hp = None

                config_space.add_condition(
                    CS.InCondition(hp, config_space.get_hyperparameter("model"), [model])
                )

        return config_space

    # convert given config space params to dictionary for model runner
    def bohb_config2model_runner(self, conf):
        pipe_param = {}
        pipe_param["params"] = {}
        for key in conf:
            if key == "model":
                pipe_param["name"] = conf[key]
                pipe_param["model"] = self.model_mapper[conf[key]]
            else:
                pipe_param["params"][key.split("-")[1]] = conf[key]

        return pipe_param
