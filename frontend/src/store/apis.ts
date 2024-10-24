import axios from "axios";
import { Transaction } from "./type";

export const inference = async (transactions: Transaction[]) => {
  const url = `/api/inference`;
  const ret = await axios
    .post(
      url,
      {
        instances: transactions,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    )
    .then((data: any) => {
      return data.data;
    })
    .catch((e) => {
      return {
        predictions: [],
      };
    });
  return ret.predictions;
};
