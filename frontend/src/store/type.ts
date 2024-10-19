export type DataDistribution = {
  col_name: string;
  col_type: string;
  distribution: NumericDist | CategoricalDist | [];
};

export type NumericDist = {
  minmax: {
    min: number;
    max: number;
    mean: number;
  };
  histogram: {
    counts: number[];
    bins: number[];
  };
};

export type Base = {
  name: string;
  value: number;
};

export type BaseString = {
  name: string;
  value: string;
};

export type CategoricalDist = {
  value_percentage: Base[];
};
