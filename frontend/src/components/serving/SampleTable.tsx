import { Card } from "@mui/material";
import { css } from "@emotion/react";
import { Typography } from "@mui/material";
import { Base, ModelReport, Transaction } from "@src/store/type";

export default function SampleTable(props: { data: Transaction[] }) {
  return (
    <div
      css={css`
        display: flex;
        flex-direction: row;
        gap: 20px;
      `}
    >
      datatable
    </div>
  );
}
