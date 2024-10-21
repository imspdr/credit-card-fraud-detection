import { Card } from "@mui/material";
import { css } from "@emotion/react";
import { Typography } from "@mui/material";
import { Base } from "@src/store/type";
import { ResponsiveBar } from "@nivo/bar";

function SingleBar(props: { value: number; width: number }) {
  return (
    <div
      css={css`
        height: 35px;
        width: ${props.width}px;
      `}
    >
      <ResponsiveBar
        data={[
          {
            label: "value",
            value: props.value,
          },
        ]}
        keys={["value"]}
        indexBy="label"
        layout="horizontal"
        margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
        colors={"#87CEEB"}
        maxValue={1}
        axisTop={null}
        axisRight={null}
        axisBottom={null}
        axisLeft={null}
        labelSkipWidth={12}
        labelSkipHeight={12}
        labelTextColor={"#202020"}
        theme={{
          labels: {
            text: {
              fontSize: "20px", // Set font size for label text
            },
          },
        }}
        animate={true}
        enableGridY={false}
        enableGridX={false}
        isInteractive={true}
        tooltip={() => <></>}
      />
    </div>
  );
}

export default function Evaluate(props: {
  width: number;
  height: number;
  evaluate: Base[] | undefined;
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
        gap: 20px;
      `}
      elevation={0}
    >
      {props.evaluate && (
        <div
          css={css`
            display: flex;
            flex-direction: column;
            gap: 15px;
          `}
        >
          {props.evaluate.map((item: Base) => {
            return (
              <div
                css={css`
                  display: flex;
                  flex-direction: column;
                  gap: 5px;
                `}
              >
                <Typography variant="h6">{item.name}</Typography>
                <SingleBar width={props.width} value={Number(Number(item.value).toFixed(4))} />
              </div>
            );
          })}
        </div>
      )}
    </Card>
  );
}
