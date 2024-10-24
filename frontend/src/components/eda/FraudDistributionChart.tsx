import { Card } from "@mui/material";
import { css } from "@emotion/react";
import { Typography } from "@mui/material";
import { CategoricalDist, DataDistribution, NumericDist } from "@src/store/type";
import { useEffect, useState } from "react";
import HistogramChart from "./HistogramChart";
import CategoricalChart from "./CategoricalChart";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";

export default function FraudDistributionChart(props: {
  width: number;
  height: number;
  label?: string;
  fraud: DataDistribution[];
  notFraud: DataDistribution[];
}) {
  const [selectedColumn, setSelectedColumn] = useState(props.fraud[0]!.col_name);
  const [selectedFraud, setSelectedFraud] = useState<DataDistribution>(props.fraud[0]!);
  const [selectedNotFraud, setSelectedNotFraud] = useState<DataDistribution>(props.notFraud[0]!);
  useEffect(() => {
    setSelectedFraud(props.fraud.find((item) => item.col_name == selectedColumn)!);
    setSelectedNotFraud(props.notFraud.find((item) => item.col_name == selectedColumn)!);
  }, [selectedColumn]);
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
        <Typography variant="h6">{"FRAUD 데이터 분포 비교"}</Typography>
        <Select
          value={selectedColumn}
          onChange={(e) => setSelectedColumn(e.target.value)}
          css={css`
            width: 200px;
          `}
        >
          {props.fraud.map((item) => (
            <MenuItem value={String(item.col_name)}>{item.col_name}</MenuItem>
          ))}
        </Select>
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
