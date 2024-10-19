import { runInAction, makeAutoObservable } from "mobx";
import { DataDistribution } from "./type";
import fraud_data_dist from "./fraud_data_dist.json";
import not_fraud_data_dist from "./not_fraud_data_dist.json";

export class RootStore {
  public fraudDataDist: DataDistribution[];
  public notFraudDataDist: DataDistribution[];
  constructor() {
    this.fraudDataDist = fraud_data_dist;
    this.notFraudDataDist = not_fraud_data_dist;
    makeAutoObservable(this);
  }
}
