class ModelRunner:
    '''
    Bohb configuration 정보로부터 모델 생성
    '''
    def __init__(self, **conf):
        self.configuration = conf
        self.col_names = None
        self.model_name = conf["name"]
        self.model = conf["model"](**conf["params"])

    def train(self, X, y, col_names):
        self.model.fit(X, y, col_names)
        return self

    def inference(self, X):
        return self.model.predict(X)

    def inference_proba(self, X):
        return self.model.predict_proba(X)

    def get_model(self):
        return self.model

    def get_col_names(self):
        return self.col_names

    def get_config(self):
        ret_dict = []
        ret_dict.append({"name": "model name", "value" : self.model_name})
        for key, value in self.configuration["params"].items():
            ret_dict.append({"name": key, "value": value})
        return ret_dict
