import { Card } from "@mui/material";
import { css } from "@emotion/react";
import { Typography, Autocomplete, TextField } from "@mui/material";
import { Base, CategoricalDist, DataDistribution, NumericDist } from "@src/store/type";
import { useState } from "react";
import HistogramChart from "./HistogramChart";
import CategoricalChart from "./CategoricalChart";

export default function DataDistributionChart(props: {
  width: number;
  height: number;
  dataDistribution: DataDistribution[] | undefined;
}) {
  const [selectedDist, setSelectedDist] = useState<DataDistribution | undefined>(undefined);
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
        {props.dataDistribution && (
          <Autocomplete
            disablePortal
            options={props.dataDistribution
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
                setSelectedDist(v.data);
              }
            }}
            css={css`
              width: 300px;
            `}
          />
        )}
      </div>
      <div
        css={css`
          display: flex;
          flex-direction: row;
          justify-content: center;
        `}
      >
        {selectedDist && (
          <>
            {selectedDist.col_type === "numeric" ? (
              <HistogramChart
                width={props.width - 10}
                height={props.height * 0.8}
                dist={selectedDist.distribution as NumericDist}
              />
            ) : (
              <CategoricalChart
                width={props.width - 10}
                height={props.height * 0.8}
                dist={selectedDist.distribution as CategoricalDist}
              />
            )}
          </>
        )}
      </div>
    </Card>
  );
}
