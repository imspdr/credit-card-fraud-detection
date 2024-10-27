import { css } from "@emotion/react";
import { Base, CategoricalDist } from "@src/store/type";
import { ResponsiveBar } from "@nivo/bar";

export default function CategoricalChart(props: {
  width: number;
  height: number;
  dist: CategoricalDist;
}) {
  return (
    <div
      css={css`
        position: relative;
        width: ${props.width}px;
        height: ${props.height}px;
      `}
    >
      <ResponsiveBar
        layout="vertical"
        margin={{ top: 20, right: 30, bottom: 30, left: 30 }}
        data={props.dist.value_count
          .sort((a, b) => {
            if (props.dist.value_count.length > 10) {
              return b.value - a.value;
            } else {
              return a.name.localeCompare(b.name, undefined, { numeric: true });
            }
          })
          .filter((_, i) => i < 10)
          .map((item: Base) => {
            return {
              name: item.name,
              value: item.value,
            };
          })}
        indexBy="name"
        keys={["value"]}
        colors={"#87CEEB"}
        borderColor={{
          from: "color",
          modifiers: [["darker", 2.6]],
        }}
        enableGridY={false}
        enableGridX={false}
        axisLeft={null}
        padding={0}
        labelTextColor={{
          from: "color",
          modifiers: [["darker", 1.4]],
        }}
        isInteractive={true}
        label={(d) => `${d.value}`}
        labelSkipWidth={12}
        labelSkipHeight={12}
        borderWidth={1}
      />
    </div>
  );
}
