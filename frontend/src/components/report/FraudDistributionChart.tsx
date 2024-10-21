import { Card } from "@mui/material";
import { css } from "@emotion/react";
import { Typography, Autocomplete, TextField } from "@mui/material";
import { Base, CategoricalDist, DataDistribution, NumericDist } from "@src/store/type";
import { useState } from "react";
import HistogramChart from "./HistogramChart";
import CategoricalChart from "./CategoricalChart";

export default function FraudDistributionChart(props: {
  width: number;
  height: number;
  label?: string;
  fraud: DataDistribution[];
  notFraud: DataDistribution[];
}) {
  const [selectedFraud, setSelectedFraud] = useState<DataDistribution | undefined>(props.fraud[0]);
  const [selectedNotFraud, setSelectedNotFraud] = useState<DataDistribution | undefined>(
    props.notFraud[0]
  );
  return (
    <Card
      css={css`
        width: ${props.width}px;
        height: ${props.height}px;
        border-radius: 20px;
        padding: 20px;

        display: flex;
        flex-direction: column;
        gap: 20px;
      `}
      elevation={0}
    >
      <div
        css={css`
          display: flex;
          flex-direction: row;
          justify-content: space-between;
        `}
      >
        <Typography variant="h6">{"데이터 분포"}</Typography>
        <Autocomplete
          disablePortal
          options={props.fraud
            .filter((dist) => dist.col_type === "numeric" || dist.col_type === "categorical")
            .map((dist) => {
              return {
                label: dist.col_name,
                id: String(dist.col_name),
                data: dist,
              };
            })}
          sx={{ width: 300, height: 60 }}
          renderInput={(params) => <TextField {...params} label="칼럼 선택" />}
          onChange={(e, v) => {
            if (v && v.id) {
              setSelectedFraud(v.data);
              const notFraud = props.notFraud.find((dd) => dd.col_name == v.label);
              setSelectedNotFraud(notFraud);
            }
          }}
          css={css`
            width: 300px;
          `}
        />
      </div>
      <div
        css={css`
          display: flex;
          flex-direction: column;
          justify-content: center;
          gap: 10px;
        `}
      >
        <Typography>Fraud</Typography>
        {selectedFraud && (
          <>
            {selectedFraud.col_type === "numeric" ? (
              <HistogramChart
                width={props.width - 10}
                height={props.height * 0.4}
                dist={selectedFraud.distribution as NumericDist}
              />
            ) : (
              <CategoricalChart
                width={props.width - 10}
                height={props.height * 0.4}
                dist={selectedFraud.distribution as CategoricalDist}
              />
            )}
          </>
        )}
        <Typography>Not Fraud</Typography>
        {selectedNotFraud && (
          <>
            {selectedNotFraud.col_type === "numeric" ? (
              <HistogramChart
                width={props.width - 10}
                height={props.height / 2 - 100}
                dist={selectedNotFraud.distribution as NumericDist}
              />
            ) : (
              <CategoricalChart
                width={props.width - 10}
                height={props.height / 2 - 100}
                dist={selectedNotFraud.distribution as CategoricalDist}
              />
            )}
          </>
        )}
      </div>
    </Card>
  );
}
