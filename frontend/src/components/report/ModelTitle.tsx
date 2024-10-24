import { Card } from "@mui/material";
import { css } from "@emotion/react";
import { Typography } from "@mui/material";
import { Base } from "@src/store/type";

export default function ModelTitle(props: {
  width: number;
  height: number;
  name: string;
  config: Base[];
}) {
  return (
    <Card
      css={css`
        width: ${props.width}px;
        height: ${props.height}px;
        border-radius: 20px;
        padding: 20px;

        display: flex;
        flex-direction: column;
        gap: 10px;
      `}
      elevation={0}
    >
      <Typography variant="h4">{props.name}</Typography>
      {props.config && (
        <div
          css={css`
            display: flex;
            flex-direction: column;
            gap: 5px;
          `}
        >
          {props.config.map((item) => {
            if (item.name === "model name") {
              return <Typography variant="h6">{item.value}</Typography>;
            }
            return <></>;
          })}
          <div
            css={css`
              display: flex;
              flex-direction: column;
              padding: 10px;
            `}
          >
            {props.config.map((item) => {
              if (item.name !== "model name") {
                return (
                  <div
                    css={css`
                      display: flex;
                      flex-direction: row;
                      justify-content: space-between;
                    `}
                  >
                    <span>{item.name}</span>
                    <span>
                      {Number.isInteger(item.value) ? item.value : Number(item.value).toFixed(4)}
                    </span>
                  </div>
                );
              }
            })}
          </div>
        </div>
      )}
    </Card>
  );
}
