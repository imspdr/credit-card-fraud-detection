import { css } from "@emotion/react";
import { UserData, TimeData } from "@src/store/type";
import { ResponsiveBar } from "@nivo/bar";

export default function TimeChart(props: { width: number; height: number; data: UserData }) {
  return (
    <div>
      <div
        css={css`
          position: relative;
          width: ${props.width}px;
          height: ${props.height / 2}px;
        `}
      >
        <svg
          css={css`
            position: absolute;
            top: 0px;
            left: 0px;
            width: 100%;
            height: 100%;
          `}
        >
          <text x={50} y={40} fill="#202020" fontSize={12}>
            {`total debt : ${props.data.total_debt.toFixed(4)}`}
          </text>
          <text x={50} y={60} fill="#202020" fontSize={12}>
            {`yearly income : ${props.data.yearly_income.toFixed(4)}`}
          </text>
        </svg>
        <ResponsiveBar
          layout="vertical"
          margin={{ top: 70, right: 30, bottom: 30, left: 30 }}
          data={props.data.time_data
            .sort((a, b) => {
              return a.time.localeCompare(b.time, undefined, { numeric: true });
            })
            .map((item: TimeData) => {
              return {
                name: item.time,
                value: Number(item.fraud_count.toFixed(2)),
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
      <div
        css={css`
          position: relative;
          width: ${props.width}px;
          height: ${props.height / 2}px;
        `}
      >
        <ResponsiveBar
          layout="vertical"
          margin={{ top: 20, right: 30, bottom: 30, left: 30 }}
          data={props.data.time_data
            .sort((a, b) => {
              return a.time.localeCompare(b.time, undefined, { numeric: true });
            })
            .map((item: TimeData) => {
              return {
                name: item.time,
                value: Number(item.not_fraud_count.toFixed(2)),
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
    </div>
  );
}
