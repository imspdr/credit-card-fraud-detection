import ConfigSpace as CS
from .configuration import model_dict


class ConfigParser:
    def __init__(self, custom_model=model_dict):
        self.custom_model = custom_model

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

    def bohb_config2model_runner(self, conf):
        pipe_param = {}
        pipe_param["params"] = {}
        for key in conf:
            if key == "model":
                pipe_param["name"] = conf[key]
                pipe_param["model"] = self.custom_model[conf[key]]["class"]
            else:
                pipe_param["params"][key.split("-")[1]] = conf[key]

        return pipe_param
