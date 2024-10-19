import axios from "axios";

const namespace = "TOENVNAMESPACE";
const backend = "/api";

const rainHost = `rain-multi-model.${namespace}.example.com`;

export const rainAPI = {
  kserve: {
    inference: async (day: string, modelname: string) => {
      const rainURL = `/kserve/v1/models/${modelname}:predict`;
      const ret = await axios
        .post(
          rainURL,
          {
            instances: [day],
          },
          {
            headers: {
              "Content-Type": "application/json",
              "Kserve-Host": rainHost,
            },
          }
        )
        .then((data: any) => {
          return data.data;
        })
        .catch((e) => {
          return {
            predictions: [
              {
                y_hat: [],
                y_true: [],
                y_proba: [],
              },
            ],
          };
        });
      return ret;
    },
  },
};
