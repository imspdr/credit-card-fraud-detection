import { css } from "@emotion/react";
import { NumericDist } from "@src/store/type";
import { ResponsiveBar } from "@nivo/bar";

export default function HistogramChart(props: {
  width: number;
  height: number;
  dist: NumericDist;
}) {
  const newData = [];
  for (let i = 0; i < props.dist.histogram.counts.length; i++) {
    newData.push({
      id: `~ ${Number(props.dist.histogram.bins[i + 1]).toFixed(0)}`,
      count: Number(props.dist.histogram.counts[i]),
    });
  }
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
        margin={{ top: 70, right: 30, bottom: 30, left: 30 }}
        data={newData}
        indexBy="id"
        keys={["count"]}
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
        labelSkipWidth={12}
        labelSkipHeight={12}
        borderWidth={1}
      />
      <svg
        css={css`
          position: absolute;
          top: 0px;
          left: 0px;
          width: 100%;
          height: 100%;
        `}
      >
        <text x={50} y={20} fill="#202020" fontSize={12}>
          {`Max : ${props.dist.minmax.max.toFixed(4)}`}
        </text>
        <text x={50} y={40} fill="#202020" fontSize={12}>
          {`Mean : ${props.dist.minmax.mean.toFixed(4)}`}
        </text>
        <text x={50} y={60} fill="#202020" fontSize={12}>
          {`Min : ${props.dist.minmax.min.toFixed(4)}`}
        </text>
      </svg>
    </div>
  );
}
