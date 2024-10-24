import { Card } from "@mui/material";
import { css } from "@emotion/react";
import { Typography } from "@mui/material";
import { Base, ModelReport } from "@src/store/type";
import Evaluate from "./Evaluate";
import ModelTitle from "./ModelTitle";
import FeatureImportance from "./FeatureImportance";

export default function Report(props: { report: ModelReport }) {
  return (
    <div
      css={css`
        display: flex;
        flex-direction: row;
        gap: 20px;
      `}
    >
      <div
        css={css`
          display: flex;
          flex-direction: column;
          gap: 20px;
        `}
      >
        <ModelTitle
          name={`모델 - ${props.report.index}`}
          config={props.report.data.best_config}
          width={400}
          height={150}
        />
        <Evaluate evaluate={props.report.data.best_loss} width={400} height={350} />
      </div>
      <FeatureImportance data={props.report.data.feature_importance} width={700} height={560} />
    </div>
  );
}
