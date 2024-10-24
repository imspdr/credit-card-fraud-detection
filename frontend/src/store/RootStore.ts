import { runInAction, makeAutoObservable } from "mobx";
import { DataDistribution, ModelReport, Transaction, UserData } from "./type";
import eval_data from "./eval_data.json";
import fraud_data_dist from "./fraud_data_dist.json";
import not_fraud_data_dist from "./not_fraud_data_dist.json";
import data_dists from "./data_dists.json";
import report from "./report.json";

export class RootStore {
  public fraudDataDist: DataDistribution[];
  public notFraudDataDist: DataDistribution[];
  public perUserDist: UserData[];
  public evalData: Transaction[];
  public report: ModelReport[];

  public sampleData: Transaction[];

  constructor() {
    this.fraudDataDist = fraud_data_dist;
    this.notFraudDataDist = not_fraud_data_dist;
    this.perUserDist = data_dists;
    this.evalData = eval_data;
    this.sampleData = [];
    this.report = report;
    makeAutoObservable(this);
  }
}
