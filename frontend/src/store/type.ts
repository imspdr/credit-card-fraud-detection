export type Transaction = {
  User: number;
  Card: number;
  Year: number;
  Month: number;
  Day: number;
  Time: string;
  Amount: string;
  "Use Chip": string;
  "Merchant Name": number;
  "Merchant City": string;
  "Merchant State": string | null;
  Zip: number | null;
  MCC: number;
  "Errors?": string | null;
  "Is Fraud?": string;
};

export type UserData = {
  user: number;
  total_debt: number;
  yearly_income: number;
  time_data: TimeData[];
};

export type TimeData = {
  time: string;
  not_fraud_count: number;
  fraud_count: number;
};

export type DataDistribution = {
  col_name: string;
  col_type: string;
  distribution: NumericDist | CategoricalDist | [];
};

export type NumericDist = {
  minmax: {
    min: number;
    max: number;
    sum: number;
    len: number;
  };
  histogram: {
    counts: number[];
    bins: number[];
  };
};

export type CategoricalDist = {
  value_count: Base[];
};

export type Base = {
  name: string;
  value: any;
};

export type Loss = {
  f1: number;
  precision: number;
  recall: number;
  accuracy: number;
};

export type ModelReport = {
  index: number;
  data: {
    best_config: Base[];
    best_loss: Loss;
    feature_importance: {
      label: string[];
      value: number[];
    };
  };
};
