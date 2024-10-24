import { Card } from "@mui/material";
import { css } from "@emotion/react";
import { Typography } from "@mui/material";

export default function ServingResult(props: { result: number[] }) {
  return (
    <div
      css={css`
        display: flex;
        flex-direction: row;
        gap: 20px;
      `}
    >
      result
    </div>
  );
}
